#!/usr/bin/env python3
"""Fail-closed source-bound transfer-edge and species-identity audit for ANIMO PREP07."""
import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

SOURCE_SHA = '183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566'
TESTBANK_SHA = '44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84'


def sha256(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def read_member(zip_path, basename):
    with zipfile.ZipFile(zip_path) as archive:
        hits = [name for name in archive.namelist() if Path(name).name.lower() == basename.lower()]
        if len(hits) != 1:
            raise RuntimeError(f'{basename}: expected one member, got {hits}')
        return archive.read(hits[0]).decode('latin1')


def occurrences(text, needle):
    return text.count(needle)


def testbank_ncxfa(zip_path):
    values = []
    pattern = re.compile(r'^\s*(\d+)\s*!\s*ncxfa\b', re.I | re.M)
    with zipfile.ZipFile(zip_path) as archive:
        for name in archive.namelist():
            if name.endswith('/'):
                continue
            try:
                text = archive.read(name).decode('latin1')
            except Exception:
                continue
            for match in pattern.finditer(text):
                values.append({'file': name, 'value': int(match.group(1))})
    return values


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source_zip')
    parser.add_argument('testbank_zip')
    parser.add_argument('--json')
    args = parser.parse_args()

    source_sha = sha256(args.source_zip)
    testbank_sha = sha256(args.testbank_zip)
    if source_sha != SOURCE_SHA:
        raise SystemExit(f'source sha mismatch {source_sha}')
    if testbank_sha != TESTBANK_SHA:
        raise SystemExit(f'testbank sha mismatch {testbank_sha}')

    addit = read_member(args.source_zip, 'Addit.for')
    outbal = read_member(args.source_zip, 'Outbal_calc.for')
    resp = read_member(args.source_zip, 'resp_miner.for')
    inicalc = read_member(args.source_zip, 'Inicalc.for')
    input1 = read_member(args.source_zip, 'input1.for')
    transorp = read_member(args.source_zip, 'Transorp.for')

    checks = {}

    def check(name, condition, detail=None):
        checks[name] = {'pass': bool(condition)}
        if detail is not None:
            checks[name]['detail'] = detail

    # Guard an already-qualified species mismatch so later edits cannot hide the audit context.
    check('resp_miner_case2_p_from_n_19',
          'Transfop(19,Ln) = (1.0-AsfaSDO) * Transfon(17,Ln)' in resp)
    check('resp_miner_case2_p_from_n_20',
          'Transfop(20,Ln) = AsfaSDO * Transfon(17,Ln)' in resp)

    # Exudate-humus ploughing ledger family.
    check('addit_adhuex_old_subtract',
          'Adhuexpl(I,Ln) = Adhuexpl(I,Ln) - Huex(Ln)' in addit)
    check('addit_adhuex_first_new_add',
          'Adhuexpl(I,Ln) = Adhuexpl(I,Ln) + Huex(Ln)' in addit)
    check('addit_adhuex_second_new_add',
          'Adhuexpl(I,Ln)   = Adhuexpl(I,Ln) + huex(Ln)' in addit)
    check('addit_adhuex_n_explicit',
          'Adhuexnipl(I,Ln) = Adhuexnipl(I,Ln) + huex(Ln)*Nifrhu(Ln)' in addit)
    check('addit_adhuex_p_explicit',
          'Adhuexpopl(I,Ln) = Adhuexpopl(I,Ln) + huex(Ln)*Pofrhu(Ln)' in addit)
    check('outbal_c_consumes_adhuexpl',
          'Bahu(Redi,Ly) =bahu(Redi,Ly)  +Adhuexpl(I,Ln)* Z' in outbal)
    check('outbal_n_reconstructs_from_c',
          'Dum = Adhuexpl(I,Ln) * Nifrhu(Ln) * Z' in outbal)
    check('outbal_p_reconstructs_from_c',
          'Dum = Adhuexpl(I,Ln) * Pofrhu(Ln) * Z' in outbal)
    check('outbal_n_explicit_array_not_consumed', occurrences(outbal, 'Adhuexnipl(I,Ln)') == 0,
          occurrences(outbal, 'Adhuexnipl(I,Ln)'))
    check('outbal_p_explicit_array_not_consumed', occurrences(outbal, 'Adhuexpopl(I,Ln)') == 0,
          occurrences(outbal, 'Adhuexpopl(I,Ln)'))

    # Multi-site fast-sorption management seam.
    check('parser_admits_ncxfa_1_to_3',
          "Call Checkint(Uoer,Error,Label,'Ncxfa',Ncxfa,1,3)" in input1)
    check('transorp_declares_site_fractions',
          'NCXFA                  number of fractions used to describe the' in transorp)
    check('transorp_fast_loops_ncxfa', 'Do 210 I=1,Ncxfa' in transorp)
    check('inicalc_site_helper_only_single_site',
          'If (Optcxfa.Eq.2 .And. Ncxfa.Eq.1) Then' in inicalc)
    check('inicalc_ampoma_site1', 'Ampoma(Ln) = Pacxfaln(2,1,Ln)' in inicalc)
    check('inicalc_socfpo_site1', 'Socfpo(Ln) = Pacxfaln(3,1,Ln)' in inicalc)
    check('addit_uses_single_site_ampoma', occurrences(addit, 'Ampoma(Ln)') >= 4,
          occurrences(addit, 'Ampoma(Ln)'))
    check('addit_uses_single_site_socfpo', occurrences(addit, 'Socfpo(Ln)') >= 6,
          occurrences(addit, 'Socfpo(Ln)'))
    check('addit_writes_amcxfa_site1', occurrences(addit, 'Amcxfa(1,Ln)') >= 5,
          occurrences(addit, 'Amcxfa(1,Ln)'))
    check('addit_never_uses_parcxfa', 'Parcxfa' not in addit)

    values = testbank_ncxfa(args.testbank_zip)
    check('testbank_has_ncxfa_evidence', len(values) > 0, len(values))
    check('testbank_ncxfa_all_one', len(values) > 0 and all(item['value'] == 1 for item in values),
          [item['value'] for item in values])

    # Exact algebraic consequence of the duplicated carbon-ledger update.
    old_state, new_state = 2.0, 3.0
    expected = -old_state + new_state
    legacy = -old_state + new_state + new_state
    algebra = {
        'old': old_state,
        'new': new_state,
        'expected_net': expected,
        'legacy_net': legacy,
        'excess': legacy - expected,
    }
    check('duplicate_adhuex_algebra_excess_equals_new',
          abs((legacy - expected) - new_state) < 1e-15, algebra)

    result = {
        'evidence_class': 'SOURCE_BOUND_STATIC_TRANSFER_EDGE_AUDIT',
        'source_sha256': source_sha,
        'testbank_sha256': testbank_sha,
        'checks_passed': sum(value['pass'] for value in checks.values()),
        'checks_total': len(checks),
        'checks': checks,
        'testbank_ncxfa': values,
        'findings': {
            'exudate_humus_ledger': {
                'candidate_id': 'TCD-028',
                'summary': 'Adhuexpl gets old-state subtraction plus two identical new-state additions; C ledger consumes Adhuexpl directly while N/P reconstruct from it despite explicit species arrays.',
                'classification': 'SOURCE_CONFIRMED_EXUDATE_HUMUS_PLOUGHING_LEDGER_DOUBLE_COUNT_AND_SPECIES_RECONSTRUCTION_GAP',
            },
            'multisite_fast_sorption_management': {
                'candidate_id': 'TCD-029',
                'summary': 'Parser and transport admit NCXFA up to 3, but management/addition code relies on single-site helper parameters populated only when NCXFA=1 and updates Amcxfa(1) only.',
                'classification': 'SOURCE_CONFIRMED_MULTISITE_FAST_SORPTION_MANAGEMENT_INTEGRATION_GAP_TESTBANK_UNEXERCISED',
            },
        },
    }
    if not all(value['pass'] for value in checks.values()):
        print(json.dumps(result, indent=2))
        raise SystemExit(1)
    text = json.dumps(result, indent=2)
    if args.json:
        Path(args.json).write_text(text + '\n')
    print(text)


if __name__ == '__main__':
    main()
