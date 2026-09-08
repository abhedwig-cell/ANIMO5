#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, zipfile
from pathlib import Path

EXPECTED_SOURCE_SHA256 = "183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566"

CHECKS = {
    "Init.for": [
        "Mofro(Ln) = Mofrt(Ln)", "Sic = Sict", "Pn = Pnt", "Wale = Walet",
        "Conh(Ln) = Rsconh(Ln)", "Cxnh(Ln) = Rscxnh(Ln)", "Coni(Ln) = Rsconi(Ln)",
        "Codiorma(Ln) = Rscodiorma(Ln)", "Codiorni(Ln) = Rscodiorni(Ln)", "Codiorpo(Ln) = Rscodiorpo(Ln)",
        "CoStdiorma(Ln) = RscoStdiorma(Ln)", "CoStdiorni(Ln) = RscoStdiorni(Ln)", "CoStdiorpo(Ln) = RscoStdiorpo(Ln)",
        "Ex(Ln) = Rsex(Ln)", "Huex(Ln) = Rshuex(Ln)", "Huos(Ln) = Rshuos(Ln)", "Os(Ln,Fn) = Rsos(Ln,Fn)",
        "Copo(Ln) = Rscopo(Ln)", "Ampopr(Ln) = Rsampopr(Ln)",
        "Amcxfa(I,Ln) = Rsamcxfa(I,Ln)", "Amcxsl(I,Ln) = Rsamcxsl(I,Ln)",
        "SrWaMpOld(Dn)= SrWaMp(Dn)", "CoMpDiorMa(Dn) = RsCoMpDiorMa(Dn)",
        "CoMpNh(Dn)     = RsCoMpNh(Dn)", "CoMpNi(Dn)     = RsCoMpNi(Dn)"
    ],
    "Outbal_Init.for": [
        "Bawa(Stsm_b,Ly) = Bawa(Stsm_b,Ly) + He(Ln) * Mofro(Ln) * P",
        "( Mofro(Ln) + Rhbd(Ln)*SocfDOM(Ln) ) * Codiorma(Ln)",
        "( Mofro(Ln) + Rhbd(Ln)*SocfSDO(Ln) ) * CoStdiorma(Ln)",
        "Banh(Inip_l,Ly)=banh(Inip_l,Ly)+Conh(Ln) *He(Ln)*Mofro(Ln) * P",
        "Bani(Inip_l,Ly)=bani(Inip_l,Ly)+Coni(Ln) *He(Ln)*Mofro(Ln) * P",
        "Banh(Inip_x,Ly)    = Banh(Inip_x,Ly)+Cxnh(Ln)     * P",
        "Bapp(Inip_l,Ly) = Bapp(Inip_l,Ly) + Copo(Ln)",
        "Bapp(Inip_x,Ly) = Bapp(Inip_x,Ly) + Toamcxfa(Ln)*He(Ln) * P",
        "Bapp(Inip_x,Ly) = Bapp(Inip_x,Ly) + Toamcxsl(Ln)*He(Ln) * P",
        "Bapp(Inip_p,Ly) = Bapp(Inip_p,Ly) + Ampopr(Ln)*He(Ln)   * P"
    ],
    "MAPOHYDRO.FOR": [
        "Badev= Badev - FlMpOuDrTo * St",
        "Badev= Badev + FlMpInPr(Dn) * St - (SrWaMp(Dn)-SrWaMpOld(Dn))",
        "MpDev = (FlMpInTo - FlMpOuTo) * St",
        "MpDev = MpDev - (SrWaMp(Dn) - SrWaMpOld(Dn))"
    ],
    "MAPOTRANSPORT.FOR": [
        "SrAmMp    = SrAmMp    + SrWaMp(Dn)    * RsCoMP(Dn)",
        "SrAmMpOld = SrAmMpOld + SrWaMpOld(Dn) * CoMp(Dn)",
        "BaDev = ToInMp + SrAmMpOld - (ToOuMp + SrAmMp)"
    ],
    "Outbal_calc.for": [
        "!             Bawa(Dra(Drn),Ly) = Bawa(Dra(Drn),Ly) +",
        "!             Bdom(Dra4,Ly) = Bdom(Dra4,Ly) + AvcoMpdiorma(1) * Dum",
        "Banh(Dra4,Ly) = Banh(Dra4,Ly) + AvcoMpnh(1) * Dum",
        "Bani(Dra4,Ly) = Bani(Dra4,Ly) + AvcoMpni(1) * Dum",
        "Bano(Dra4,Ly) = Bano(Dra4,Ly) + AvcoMpdiorni(1) * Dum"
    ]
}

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def norm(text: str) -> str:
    return " ".join(text.replace("&", " ").split()).lower()

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_zip", type=Path)
    parser.add_argument("--testbank-zip", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    actual = sha256(args.source_zip)
    if actual != EXPECTED_SOURCE_SHA256:
        raise SystemExit(f"source SHA-256 mismatch: {actual}")

    with zipfile.ZipFile(args.source_zip) as archive:
        members = {Path(name).name: name for name in archive.namelist() if not name.endswith("/")}
        result = {
            "source_sha256": actual,
            "evidence_class": "SOURCE_BOUND_STATIC_AUDIT_NOT_REFERENCE",
            "files": {}, "checks_passed": 0, "checks_total": 0
        }
        for filename, fragments in CHECKS.items():
            if filename not in members:
                raise SystemExit(f"missing source file: {filename}")
            text = archive.read(members[filename]).decode("latin1")
            normalized = norm(text)
            checks = []
            for fragment in fragments:
                present = norm(fragment) in normalized
                checks.append({"fragment": fragment, "present": present})
                result["checks_total"] += 1
                result["checks_passed"] += int(present)
            result["files"][filename] = checks

        outbal = archive.read(members["Outbal_calc.for"]).decode("latin1")
        header = outbal.lower().split("implicit none")[0]
        result["macropore_main_ledger_interface"] = {
            "outbal_calc_receives_SrWaMp": "srwamp" in header,
            "outbal_calc_receives_RsCoMp": "rscomp" in header,
            "ddev_formula_mentions_Dra4": any(
                "ddev" in line.lower() and "dra4" in line.lower() and not line.lstrip().startswith("!")
                for line in outbal.splitlines()
            ),
            "active_direct_drainage_terms": {
                key: any(key.lower() in line.lower() and not line.lstrip().startswith("!") for line in outbal.splitlines())
                for key in ["Banh(Dra4", "Bani(Dra4", "Bano(Dra4", "Bdom(Dra4", "Bapp(Dra4", "Bapo(Dra4"]
            }
        }

        if args.testbank_zip:
            with zipfile.ZipFile(args.testbank_zip) as testbank:
                values = []
                for name in testbank.namelist():
                    if name.endswith("/") or "general" not in Path(name).name.lower():
                        continue
                    text = testbank.read(name).decode("latin1")
                    for line in text.splitlines():
                        if "macroporeoption" in line.lower():
                            rhs = line.split("=", 1)[1] if "=" in line else ""
                            value = rhs.split("!", 1)[0].strip()
                            values.append({"file": name, "value": value})
                result["testbank_macropore_option_occurrences"] = values
                result["testbank_macropore_active_occurrences"] = sum(
                    1 for item in values if item["value"] not in ("0", "0.0", "")
                )

        result["all_checks_passed"] = result["checks_passed"] == result["checks_total"]
        payload = json.dumps(result, indent=2) + "\n"
        if args.output:
            args.output.write_text(payload, encoding="utf-8")
        print(payload, end="")
        return 0 if result["all_checks_passed"] else 2

if __name__ == "__main__":
    raise SystemExit(main())
