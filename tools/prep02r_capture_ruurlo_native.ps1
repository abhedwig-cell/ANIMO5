param(
    [Parameter(Mandatory=$true)][string]$ExecutablePath,
    [Parameter(Mandatory=$true)][string]$TestbankZip,
    [Parameter(Mandatory=$true)][string]$CaptureRoot
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$ExpectedExeSha256 = '40e29853a0431cc7e2b787dfeb1870f44e1ff402b5aaebd6f56c8365fc5b178d'
$ExpectedTestbankSha256 = '44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84'
$ExpectedCaseContentSet = '0f12d19f74e6640b6d17f8f401ac9c294e35ae13064205ed4d1821d6a15c9ac9'
$ExpectedHydrologySha256 = '36d8dbeee7a46c769026c7441ea607160a715768571ba3e048b32ee2ace74d13'

function Get-Sha256([string]$Path) {
    return (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash.ToLowerInvariant()
}

function Assert-Hash([string]$Path, [string]$Expected, [string]$Label) {
    $actual = Get-Sha256 $Path
    if ($actual -ne $Expected.ToLowerInvariant()) {
        throw "$Label SHA-256 mismatch. Expected $Expected, got $actual"
    }
    return $actual
}

function Get-RelativePathCompat([string]$Root, [string]$Path) {
    $rootFull = [IO.Path]::GetFullPath($Root).TrimEnd([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar)
    $pathFull = [IO.Path]::GetFullPath($Path)
    if (-not $pathFull.StartsWith($rootFull, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Path is outside root: $Path"
    }
    return $pathFull.Substring($rootFull.Length).TrimStart([IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar).Replace('\','/')
}

function Get-PathSortKey([string]$Path) {
    # Fixed-width lowercase hex preserves UTF-8 byte-wise lexical ordering and
    # avoids culture/case ordering differences between Windows hosts.
    return ([BitConverter]::ToString([Text.Encoding]::UTF8.GetBytes($Path))).Replace('-','').ToLowerInvariant()
}

function Get-Inventory([string]$Root) {
    $items = @()
    Get-ChildItem -LiteralPath $Root -Recurse -File | ForEach-Object {
        $relative = Get-RelativePathCompat $Root $_.FullName
        $items += [pscustomobject]@{
            path = $relative
            size = $_.Length
            sha256 = Get-Sha256 $_.FullName
            sort_key = Get-PathSortKey $relative
        }
    }
    $sorted = @($items | Sort-Object sort_key)
    return ,@($sorted | Select-Object path,size,sha256)
}

function Get-ContentSetSha256($Inventory) {
    $builder = New-Object System.Text.StringBuilder
    foreach ($item in $Inventory) {
        [void]$builder.Append($item.path)
        [void]$builder.Append([char]0)
        [void]$builder.Append([string]$item.size)
        [void]$builder.Append([char]0)
        [void]$builder.Append($item.sha256)
        [void]$builder.Append("`n")
    }
    $bytes = [Text.Encoding]::UTF8.GetBytes($builder.ToString())
    $sha = [Security.Cryptography.SHA256]::Create()
    try {
        return ([BitConverter]::ToString($sha.ComputeHash($bytes))).Replace('-','').ToLowerInvariant()
    } finally {
        $sha.Dispose()
    }
}

function Inventory-ToMap($Inventory) {
    $map = @{}
    foreach ($item in $Inventory) { $map[$item.path] = $item }
    return $map
}

function Get-ChangedOrNew($Before, $After) {
    $beforeMap = Inventory-ToMap $Before
    $result = @()
    foreach ($item in $After) {
        if (-not $beforeMap.ContainsKey($item.path) -or $beforeMap[$item.path].sha256 -ne $item.sha256) {
            $result += $item
        }
    }
    return ,$result
}

function Get-Deleted($Before, $After) {
    $afterMap = Inventory-ToMap $After
    $result = @()
    foreach ($item in $Before) {
        if (-not $afterMap.ContainsKey($item.path)) {
            $result += $item
        }
    }
    return ,$result
}

$ExecutablePath = (Resolve-Path -LiteralPath $ExecutablePath).Path
$TestbankZip = (Resolve-Path -LiteralPath $TestbankZip).Path
$CaptureRoot = [IO.Path]::GetFullPath($CaptureRoot)

$exeHash = Assert-Hash $ExecutablePath $ExpectedExeSha256 'animo41.exe'
$testbankHash = Assert-Hash $TestbankZip $ExpectedTestbankSha256 'ANIMO_testbank.zip'

if (Test-Path -LiteralPath $CaptureRoot) {
    throw "CaptureRoot already exists. Use a new empty path: $CaptureRoot"
}
New-Item -ItemType Directory -Path $CaptureRoot | Out-Null

$extractRoot = Join-Path $CaptureRoot '_frozen_testbank_extract'
Expand-Archive -LiteralPath $TestbankZip -DestinationPath $extractRoot
$sourceCase = Join-Path $extractRoot 'ANIMO_testbank\RuurloGrass'
if (-not (Test-Path -LiteralPath $sourceCase -PathType Container)) { throw 'RuurloGrass not found after archive extraction' }

$sourceInventory = Get-Inventory $sourceCase
$sourceContentSet = Get-ContentSetSha256 $sourceInventory
if ($sourceContentSet -ne $ExpectedCaseContentSet) {
    throw "Frozen RuurloGrass case content-set mismatch. Expected $ExpectedCaseContentSet, got $sourceContentSet"
}
$sourceHydrology = Join-Path $sourceCase 'Input\SWATRE.UNF'
Assert-Hash $sourceHydrology $ExpectedHydrologySha256 'RuurloGrass SWATRE.UNF' | Out-Null

$runRecords = @()
for ($run = 1; $run -le 2; $run++) {
    $runRoot = Join-Path $CaptureRoot ("run{0}" -f $run)
    $caseRoot = Join-Path $runRoot 'RuurloGrass'
    New-Item -ItemType Directory -Path $runRoot | Out-Null
    Copy-Item -LiteralPath $sourceCase -Destination $caseRoot -Recurse
    $stagedExe = Join-Path $runRoot 'animo41.exe'
    Copy-Item -LiteralPath $ExecutablePath -Destination $stagedExe
    if ((Get-Sha256 $stagedExe) -ne $ExpectedExeSha256) { throw "Run $run executable staging hash mismatch" }

    $preInventory = Get-Inventory $caseRoot
    $preContentSet = Get-ContentSetSha256 $preInventory
    if ($preContentSet -ne $ExpectedCaseContentSet) { throw "Run $run staging mutated frozen case bytes" }

    $stdoutPath = Join-Path $runRoot 'stdout.txt'
    $stderrPath = Join-Path $runRoot 'stderr.txt'
    $started = [DateTime]::UtcNow.ToString('o')
    $sw = [Diagnostics.Stopwatch]::StartNew()
    try {
        # Start-Process redirects the native process handles directly to files,
        # avoiding PowerShell pipeline text re-encoding of stdout/stderr.
        $process = Start-Process -FilePath $stagedExe -ArgumentList @('Animo.ini') `
            -WorkingDirectory $caseRoot -RedirectStandardOutput $stdoutPath `
            -RedirectStandardError $stderrPath -NoNewWindow -Wait -PassThru
        $exitCode = $process.ExitCode
    } finally {
        $sw.Stop()
    }
    $ended = [DateTime]::UtcNow.ToString('o')

    $postInventory = Get-Inventory $caseRoot
    $postContentSet = Get-ContentSetSha256 $postInventory
    $changed = Get-ChangedOrNew $preInventory $postInventory
    $deleted = Get-Deleted $preInventory $postInventory
    $changedContentSet = Get-ContentSetSha256 $changed
    $deletedContentSet = Get-ContentSetSha256 $deleted

    $runRecords += [pscustomobject]@{
        run = $run
        started_at_utc = $started
        ended_at_utc = $ended
        runtime_seconds = [Math]::Round($sw.Elapsed.TotalSeconds, 6)
        exit_status = $exitCode
        command = '..\animo41.exe Animo.ini'
        input_content_transformed = $false
        pre_case_file_count = $preInventory.Count
        pre_case_content_set_sha256 = $preContentSet
        post_case_file_count = $postInventory.Count
        post_case_content_set_sha256 = $postContentSet
        stdout_size = (Get-Item -LiteralPath $stdoutPath).Length
        stdout_sha256 = Get-Sha256 $stdoutPath
        stderr_size = (Get-Item -LiteralPath $stderrPath).Length
        stderr_sha256 = Get-Sha256 $stderrPath
        changed_or_new_case_files = $changed
        changed_or_new_content_set_sha256 = $changedContentSet
        deleted_case_files = $deleted
        deleted_content_set_sha256 = $deletedContentSet
    }

    # Preserve only hashes/provenance in the transferable capture bundle.
    # The supplied executable itself is deliberately removed to avoid redistribution.
    Remove-Item -LiteralPath $stagedExe -Force
}

$repeatClass = if (
    $runRecords[0].post_case_content_set_sha256 -eq $runRecords[1].post_case_content_set_sha256 -and
    $runRecords[0].stdout_sha256 -eq $runRecords[1].stdout_sha256 -and
    $runRecords[0].stderr_sha256 -eq $runRecords[1].stderr_sha256
) {
    'NATIVE_REPEAT_EXACT_RAW'
} else {
    'NATIVE_REPEAT_DIFFERENT_REQUIRES_DECLARED_VOLATILE_CLASSIFICATION'
}

$codePage = (& cmd /c chcp 2>&1 | Out-String).Trim()
$manifest = [ordered]@{
    schema = 'animo-prep02r-native-run-capture-v2'
    evidence_class = 'CROSS_RUNTIME_DIAGNOSTIC_NATIVE_NOT_REFERENCE_ADMISSION'
    work_unit = 'ANIMO-PREP02R'
    case = 'RuurloGrass'
    capture_created_at_utc = [DateTime]::UtcNow.ToString('o')
    executable = [ordered]@{
        filename = 'animo41.exe'
        sha256 = $exeHash
        classification = 'MODERN_NATIVE_REBUILD_NOT_HISTORICAL_REFERENCE'
        bytes_in_transfer_bundle = $false
        native_execution_attempt_admitted = $true
        historical_reference_admitted = $false
    }
    input = [ordered]@{
        testbank_zip_sha256 = $testbankHash
        case_content_set_sha256 = $sourceContentSet
        input_content_transformed = $false
        hydrology_path = 'Input/SWATRE.UNF'
        hydrology_sha256 = $ExpectedHydrologySha256
    }
    runtime_environment = [ordered]@{
        os_version = [Environment]::OSVersion.VersionString
        is_64bit_operating_system = [Environment]::Is64BitOperatingSystem
        is_64bit_process = [Environment]::Is64BitProcess
        machine_name = $env:COMPUTERNAME
        powershell_version = $PSVersionTable.PSVersion.ToString()
        culture = [Globalization.CultureInfo]::CurrentCulture.Name
        ui_culture = [Globalization.CultureInfo]::CurrentUICulture.Name
        timezone = [TimeZoneInfo]::Local.Id
        code_page = $codePage
    }
    runs = $runRecords
    repeat_determinism = [ordered]@{
        repeat_run_performed = $true
        classification = $repeatClass
        downstream_declared_volatile_recheck_required_if_not_raw_exact = ($repeatClass -ne 'NATIVE_REPEAT_EXACT_RAW')
        scientific_numeric_tolerance_applied = $false
    }
    reference_admission = [ordered]@{
        historical_reference_environment_qualified = $false
        normal_B2_reference_available = $false
        decision = 'NOT_A_REFERENCE_ADMISSION_ACTION'
    }
    production_migration_admitted = $false
}

$manifestPath = Join-Path $CaptureRoot 'PREP02R_RUURLO_NATIVE_CAPTURE.json'
$manifest | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $manifestPath -Encoding UTF8

# The temporary extraction copy is not part of the transfer artifact.
Remove-Item -LiteralPath $extractRoot -Recurse -Force

$archivePath = "$CaptureRoot.zip"
Compress-Archive -Path (Join-Path $CaptureRoot '*') -DestinationPath $archivePath
$archiveHash = Get-Sha256 $archivePath
$sidecarPath = "$archivePath.sha256.txt"
("{0}  {1}" -f $archiveHash, [IO.Path]::GetFileName($archivePath)) | Set-Content -LiteralPath $sidecarPath -Encoding ASCII

Write-Host "Capture complete."
Write-Host "Manifest: $manifestPath"
Write-Host "Archive:  $archivePath"
Write-Host "Archive SHA-256: $archiveHash"
Write-Host "SHA sidecar: $sidecarPath"
Write-Host "Repeat classification: $repeatClass"
