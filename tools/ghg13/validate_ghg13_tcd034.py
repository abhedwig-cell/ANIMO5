import csv
import json
import math
import subprocess
from pathlib import Path

BASE = 'b4a3c603743a2e3ba62fdf69f0879975a3b4f14a'
DECISION = 'QUALIFIED_TCD034_MODEL_EVOLUTION_PLANT_TRANSFER_SOURCE_LEDGER_COMPATIBILITY_V1'
ECLASS = 'BOUNDED_SOURCE_LEDGER_COMPATIBILITY_MODEL_EVOLUTION_NOT_B2'
EXPECTED_SOURCE = {
    'ANIMO_4.1.5.53/ghg_ch4.for': '00dcc298436488beea059e6c776f09feb3a59c9ea331c235b8b5334b65874f98',
    'ANIMO_4.1.5.53/ghgtransport.for': 'd86e420952c43aaa6e730235f5820802310dd14a0019dc890537d9acd95fcff6',
    'ANIMO_4.1.5.53/ghgtranssub.for': '48d5e45d0b68b87c1d32bc16a867fe36f2f440e0d2c0ca8c95bf605f9f24ea6c',
}
ALLOWED = (
    '.github/workflows/animo-ghg13-tcd034.yml',
    'docs/ghg/TCD034_PLANT_TRANSFER_SOURCE_LEDGER.md',
    'integration/animo-ghg/GHG13_TCD034_PLANT_TRANSFER_LEDGER_CONTRACT.json',
    'integration/animo-ghg/GHG13_TCD034_PLANT_TRANSFER_LEDGER_ORACLES.json',
    'integration/animo-ghg/ANIMO-GHG13_AUTHORING_FREEZE.json',
    'integration/animo-ghg/ANIMO-GHG13_INTERNAL_ADVERSARIAL_REVIEW.json',
    'integration/animo-ghg/ANIMO-GHG13_STATUS.json',
    'tools/ghg13/',
)

def load(path):
    return json.loads(Path(path).read_text())

def close(a, b, tol=1e-12):
    return math.isclose(float(a), float(b), rel_tol=0.0, abs_tol=tol)

def manifest_map(path):
    with open(path, newline='', encoding='utf-8-sig') as handle:
        return {row['path']: row['sha256'] for row in csv.DictReader(handle)}

def changed_files():
    out = subprocess.check_output(['git', 'diff', '--name-only', f'{BASE}..HEAD'], text=True)
    return [line.strip() for line in out.splitlines() if line.strip()]

def allowed(path):
    return any(path == item or (item.endswith('/') and path.startswith(item)) for item in ALLOWED)

def centers(he):
    z = []
    bottom = 0.0
    for thickness in he:
        bottom += thickness
        z.append(bottom - 0.5 * thickness)
    return z

def t50(he, te):
    z = centers(he)
    target = 0.5
    if target < z[0] or target > z[-1]:
        return None
    for zi, ti in zip(z, te):
        if target == zi:
            return ti
    for i in range(len(z) - 1):
        if z[i] < target < z[i + 1]:
            w = (target - z[i]) / (z[i + 1] - z[i])
            return (1.0 - w) * te[i] + w * te[i + 1]
    raise AssertionError('no unique T50 bracket')

def fgrow(temp, tegr):
    if temp <= tegr:
        return 0.0
    if temp >= tegr + 10.0:
        return 4.0
    return 4.0 * (1.0 - ((tegr + 10.0 - temp) / 10.0) ** 2)

def evaluate(inp):
    temp = t50(inp['He_m'], inp['Te_degC'])
    if temp is None:
        return None
    grow = fgrow(temp, inp['Tegr_degC'])
    nroot = inp['Nuroup']
    if nroot <= 0:
        return {'T50_degC': temp, 'fGrow': grow, 'Qplant_total_kgC_m2_d': 0.0, 'Mplant_sink_total_kgC_m2': 0.0}
    ro = inp['Ro']
    he = inp['He_m']
    total_root_mass = sum(ro[:nroot])
    root_depth = sum(he[:nroot])
    froot = [ro[i] / total_root_mass * root_depth / he[i] for i in range(nroot)]
    kraw = [0.24 * inp['FvegCH4'] * froot[i] * grow for i in range(nroot)]
    phase = inp['phase_factor']
    kplant = [kraw[i] * phase[i] for i in range(nroot)]
    avco = inp['AvCoCH4_kgC_m3']
    qlayer = [kplant[i] * avco[i] * he[i] for i in range(nroot)]
    qtotal = sum(qlayer)
    st = inp['St_d']
    sink = qtotal * st
    ox = inp['PvCH4Ox'] * sink
    em = (1.0 - inp['PvCH4Ox']) * sink
    return {
        'T50_degC': temp,
        'fGrow': grow,
        'fRoot': froot,
        'Kraw_d_minus_1': kraw,
        'Kplant_d_minus_1': kplant,
        'Qplant_total_kgC_m2_d': qtotal,
        'Mplant_sink_total_kgC_m2': sink,
        'Mplant_oxidation_total_kgC_m2': ox,
        'Mplant_emission_total_kgC_m2': em,
        'ledger_residual_kgC_m2': sink - ox - em,
    }

def assert_expected(actual, expected):
    for key, value in expected.items():
        if isinstance(value, list):
            assert len(actual[key]) == len(value)
            assert all(close(a, b) for a, b in zip(actual[key], value)), (key, actual[key], value)
        else:
            assert close(actual[key], value), (key, actual[key], value)

def main():
    contract = load('integration/animo-ghg/GHG13_TCD034_PLANT_TRANSFER_LEDGER_CONTRACT.json')
    oracles = load('integration/animo-ghg/GHG13_TCD034_PLANT_TRANSFER_LEDGER_ORACLES.json')
    freeze = load('integration/animo-ghg/ANIMO-GHG13_AUTHORING_FREEZE.json')
    status = load('integration/animo-ghg/ANIMO-GHG13_STATUS.json')
    predecessor = load('integration/animo-ghg/ANIMO-GHG12_STATUS.json')
    ghg07 = load('integration/animo-ghg/GHG07_TCD034_ACTIVE_PLANT_CH4_CONTRACT.json')

    assert contract['work_unit'] == oracles['work_unit'] == freeze['work_unit'] == status['work_unit'] == 'ANIMO-GHG13'
    assert contract['target'] == oracles['target'] == freeze['target'] == status['target'] == 'TCD-034'
    assert freeze['base_head'] == BASE
    assert contract['predecessor'] == status['base_predecessor'] == f'ANIMO-GHG12@{BASE}'
    assert predecessor['primary_disposition'] == 'QUALIFIED_TCD034_PUBLIC_VALIDATION_DATASET_CANDIDATE_STACK_IDENTIFIED_DETAILED_JOINABILITY_EXTRACTION_REQUIRED_V1'
    assert predecessor['work_status']['qualified'] is True and predecessor['work_status']['reviewed'] is True
    assert ghg07['decision'] == 'QUALIFIED_TCD034_MODEL_EVOLUTION_ACTIVE_PLANT_CH4_REACHABILITY_AND_PARTITION_V1'
    assert contract['active_path_authority'] == 'ANIMO-GHG07@f8969334f648ca28ceb93a2a55bb4eedd478e1dc'
    assert contract['evidence_class'] == status['evidence_class'] == ECLASS
    assert contract['decision'] == oracles['decision'] == status['primary_disposition'] == DECISION

    source = manifest_map('reference/source/source_manifest.csv')
    for path, sha in EXPECTED_SOURCE.items():
        assert source.get(path) == sha, (path, source.get(path), sha)
        assert contract['source_manifest'][path] == sha

    assert contract['source_semantics']['transport_mass_balance_plant_term'] == 'Mplant_sink=AvCo*K1plant*He*St'
    assert contract['qualified_invariants']['layerwise_time_integrated_ledger'] == 'St*(Qox_i+Qem_i)=Mplant_sink_i'
    assert contract['qualified_invariants']['profile_time_integrated_ledger'] == 'St*(sum(Qox)+sum(Qem))=sum(Mplant_sink)'

    oracle_map = {item['id']: item for item in oracles['oracles']}
    for oid in ['GHG13-O01_GHG07_PRINCIPAL_WITH_HALF_DAY_LEDGER', 'GHG13-O02_NONUNIFORM_ROOT_PHASE_QUARTER_DAY']:
        actual = evaluate(oracle_map[oid]['inputs'])
        assert actual is not None
        assert_expected(actual, oracle_map[oid]['expected'])
        assert abs(actual['ledger_residual_kgC_m2']) <= 1e-15

    o1 = evaluate(oracle_map['GHG13-O01_GHG07_PRINCIPAL_WITH_HALF_DAY_LEDGER']['inputs'])
    assert close(o1['Mplant_oxidation_total_kgC_m2'] + o1['Mplant_emission_total_kgC_m2'], o1['Mplant_sink_total_kgC_m2'])

    base = dict(oracle_map['GHG13-O01_GHG07_PRINCIPAL_WITH_HALF_DAY_LEDGER']['inputs'])
    for pv in (0.0, 1.0):
        test = dict(base)
        test['PvCH4Ox'] = pv
        out = evaluate(test)
        if pv == 0.0:
            assert close(out['Mplant_oxidation_total_kgC_m2'], 0.0)
            assert close(out['Mplant_emission_total_kgC_m2'], out['Mplant_sink_total_kgC_m2'])
        else:
            assert close(out['Mplant_oxidation_total_kgC_m2'], out['Mplant_sink_total_kgC_m2'])
            assert close(out['Mplant_emission_total_kgC_m2'], 0.0)

    veg_off = dict(base)
    veg_off['FvegCH4'] = 0.0
    out = evaluate(veg_off)
    assert close(out['Mplant_sink_total_kgC_m2'], 0.0)

    growth_off = dict(base)
    growth_off['Te_degC'] = [4.0, 6.0, 7.0, 8.0]
    out = evaluate(growth_off)
    assert out['T50_degC'] <= growth_off['Tegr_degC']
    assert close(out['Mplant_sink_total_kgC_m2'], 0.0)

    unavailable = dict(base)
    unavailable['He_m'] = [0.1, 0.1, 0.1]
    unavailable['Te_degC'] = [8.0, 10.0, 12.0]
    assert evaluate(unavailable) is None

    nonclaims = contract['non_claims']
    assert all(value is False for value in nonclaims.values())
    assert status['whole_model_ch4_balance_qualified'] is False
    assert status['production_executable_selector_connection_qualified'] is False
    assert status['class_f_admission_ready'] is False
    assert status['b3_admission_performed'] is False
    assert status['class_f_admission_performed'] is False
    assert status['production_authorized'] is False

    bad = [path for path in changed_files() if not allowed(path)]
    assert not bad, f'scope guard failed: {bad}'

    review_path = Path('integration/animo-ghg/ANIMO-GHG13_INTERNAL_ADVERSARIAL_REVIEW.json')
    if review_path.exists():
        review = load(review_path)
        assert review['same_agent'] is True
        assert review['genuinely_independent'] is False
        assert review['independence_claimed'] is False
        assert review['decision'] == 'PASS_TCD034_MODEL_EVOLUTION_PLANT_TRANSFER_SOURCE_LEDGER_COMPATIBILITY_V1'
        assert status['review']['completed'] is True
        assert status['work_status']['qualified'] is True
        assert status['work_status']['workunit_complete'] is True

    print('GHG13 TCD034 plant-transfer source-ledger compatibility PASS')

if __name__ == '__main__':
    main()
