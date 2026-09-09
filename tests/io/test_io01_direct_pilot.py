import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / 'tools' / 'io01_direct_pilot.py'
MATERIALIZER_PATH = ROOT / 'tools' / 'materialize_ttutil427.py'
spec = importlib.util.spec_from_file_location('io01_direct_pilot', MODULE_PATH)
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)

mat_spec = importlib.util.spec_from_file_location('materialize_ttutil427', MATERIALIZER_PATH)
mat = importlib.util.module_from_spec(mat_spec)
sys.modules[mat_spec.name] = mat
mat_spec.loader.exec_module(mat)


BASE = '''Animo41
GEN="general.Inp"
MAT="material.Inp"
PLA="plant.Inp"
SOI="soil.Inp"
BOU="boundary.Inp"
INI="initial.Inp"
MAN="management.Inp"
SWU="swatre.Inp"
WAI="watbal.Inp"
WAU="watbal.Unf"
CHE="chempar.Inp"
INO="initial.Out"
CRU="crop_ext.Inp"
STE="SoilTemperature.inp"
MES="message.Out"
END
'''


class TestLegacyDirectPilot(unittest.TestCase):
    def test_positive(self):
        out = m.parse_legacy_direct_text(BASE)
        self.assertEqual(out['animo_version'], 41)
        self.assertEqual(out['bindings']['GEN']['value'], 'general.Inp')
        self.assertEqual(out['bindings']['STE']['value'], 'SoilTemperature.inp')
        self.assertTrue(out['flags']['chempar_selector_present'])
        self.assertTrue(out['flags']['soil_temperature_selector_present'])
        self.assertEqual(out['message_output']['value'], 'message.Out')
        self.assertEqual(out['message_output']['presence'], 'EXPLICIT')
        self.assertEqual(out['diagnostics']['terminated_by'], 'END')

    def test_header_exact_first_seven(self):
        self.assertEqual(
            m.parse_legacy_direct_text(BASE.replace('Animo41', 'Animo41 extra', 1))['animo_version'],
            41,
        )
        with self.assertRaises(m.LegacyDirectParseError) as cm:
            m.parse_legacy_direct_text(BASE.replace('Animo41', 'animo41', 1))
        self.assertEqual(cm.exception.code, 12345)

    def test_missing_mes_defaults(self):
        out = m.parse_legacy_direct_text(BASE.replace('MES="message.Out"\n', ''))
        self.assertEqual(out['message_output']['value'], 'message.Out')
        self.assertEqual(out['message_output']['presence'], 'DEFAULTED')
        self.assertEqual(out['message_output']['default_rule_id'], m.MESSAGE_DEFAULT_RULE)

    def test_empty_quoted_mes_is_explicit_legacy_ub_exclusion(self):
        with self.assertRaises(m.LegacyDirectUndefinedBehavior):
            m.parse_legacy_direct_text(BASE.replace('MES="message.Out"', 'MES=""'))

    def test_blank_unquoted_mes_reaches_legacy_1016(self):
        text = BASE.replace('MES="message.Out"', 'MES=')
        with self.assertRaises(m.LegacyDirectParseError) as cm:
            m.parse_legacy_direct_text(text)
        self.assertEqual(cm.exception.code, 1016)

    def test_unquoted_filename_becomes_blank_and_gen_rejected(self):
        with self.assertRaises(m.LegacyDirectParseError) as cm:
            m.parse_legacy_direct_text(BASE.replace('GEN="general.Inp"', 'GEN=general.Inp'))
        self.assertEqual(cm.exception.code, 1001)

    def test_strip_uses_last_quote(self):
        self.assertEqual(m.legacy_strip('"abc"junk"'), 'abc"junk')

    def test_unknown_selector_ignored_with_diagnostic(self):
        text = BASE.replace('MAT="material.Inp"\n', 'ZZZ="ignored"\nMAT="material.Inp"\n')
        out = m.parse_legacy_direct_text(text)
        self.assertEqual(out['bindings']['MAT']['value'], 'material.Inp')
        self.assertEqual(out['diagnostics']['unknown_selectors'][0]['selector'], 'ZZZ=')

    def test_duplicate_last_assignment_wins(self):
        text = BASE.replace('MAT="material.Inp"\n', 'MAT="first.inp"\nMAT="second.inp"\n')
        out = m.parse_legacy_direct_text(text)
        self.assertEqual(out['bindings']['MAT']['value'], 'second.inp')
        self.assertEqual(
            out['diagnostics']['duplicate_selectors'][0]['rule'],
            'LAST_ASSIGNMENT_WINS',
        )

    def test_missing_gen_rejected(self):
        with self.assertRaises(m.LegacyDirectParseError) as cm:
            m.parse_legacy_direct_text(BASE.replace('GEN="general.Inp"\n', ''))
        self.assertEqual(cm.exception.code, 1001)

    def test_eof_without_end_is_accepted_at_direct_stage(self):
        out = m.parse_legacy_direct_text(BASE.replace('END\n', ''))
        self.assertEqual(out['diagnostics']['terminated_by'], 'EOF')

    def test_probe_output_normalizes_to_same_semantic_projection(self):
        legacy = m.parse_legacy_direct_text(BASE)
        lines = [
            'schema=LegacyInputBinding/v1',
            'adapter_id=TTUTILNativeTextAdapter/v1',
            'animo_version=41',
        ]
        for field in m.BINDING_FIELDS:
            item = legacy['bindings'][field]
            lines.append(f"binding.{field}.presence={item['presence']}")
            lines.append(f"binding.{field}.value={item['value'] or ''}")
        lines.extend(
            [
                'message_output.presence=EXPLICIT',
                'message_output.value=message.Out',
                'flag.chempar_selector_present=true',
                'flag.soil_temperature_selector_present=true',
            ]
        )
        native = m.parse_native_probe_output('\n'.join(lines) + '\n')
        self.assertEqual(m.semantic_projection(legacy), m.semantic_projection(native))


class TestNativeSchemaSurface(unittest.TestCase):
    GOOD = '''SchemaVersion = 'ANIMO5_TTUTIL_DIRECT_V1'
AnimoVersion = 41
GEN = 'general.Inp'
MAT = 'material.Inp'
MES = 'message.Out'
'''

    def test_good_surface(self):
        keys = m.validate_native_direct_schema(self.GOOD)
        self.assertEqual(keys[:3], ['SchemaVersion', 'AnimoVersion', 'GEN'])

    def test_unknown_rejected(self):
        with self.assertRaises(m.NativeDirectSchemaError):
            m.validate_native_direct_schema(self.GOOD + "Mystery = 1\n")

    def test_duplicate_rejected(self):
        with self.assertRaises(m.NativeDirectSchemaError):
            m.validate_native_direct_schema(self.GOOD + "GEN = 'other.inp'\n")

    def test_mandatory_missing_rejected(self):
        with self.assertRaises(m.NativeDirectSchemaError):
            m.validate_native_direct_schema(
                "SchemaVersion='ANIMO5_TTUTIL_DIRECT_V1'\nAnimoVersion=41\n"
            )


class TestTTUTILMaterializerContract(unittest.TestCase):
    def test_pinned_source_identities(self):
        self.assertEqual(
            mat.SWAP431_SHA256,
            '2b48353db6cdf00246a1e5c0dcaafc2c61858729fad18446a1dc66359ec2a360',
        )
        self.assertEqual(
            mat.TTUTIL427_ZIP_SHA256,
            'ee40b4bc20b158163318a4a77a1294e0d9430f5cb73641fcf4a2f3c773d01193',
        )
        self.assertEqual(mat.EXPECTED_VERSION, '4.27')

    def test_member_path_fails_closed(self):
        self.assertEqual(mat.safe_member_name('TTUTIL/rdinit.for'), 'rdinit.for')
        for bad in (
            '../rdinit.for',
            'TTUTIL/../rdinit.for',
            '/TTUTIL/rdinit.for',
            'other/rdinit.for',
        ):
            with self.assertRaises(ValueError):
                mat.safe_member_name(bad)

    def test_committed_qualification_evidence(self):
        path = ROOT / 'integration' / 'animo-io' / 'DIRECT-PILOT-QUALIFICATION.json'
        if not path.exists():
            self.skipTest('qualification evidence not yet committed')
        import json

        data = json.loads(path.read_text(encoding='utf-8'))
        self.assertEqual(data['schema'], 'ANIMO-IO01/DIRECTPilotQualification/v2')
        self.assertEqual(data['result'], 'PASS')
        self.assertEqual(data['cases'], 10)
        self.assertEqual(data['field_exact_equivalence_pass'], 10)
        self.assertEqual(data['source_identity']['ttutil_files_verified'], 168)
        self.assertEqual(data['source_identity']['ttutil_fortran_objects_built'], 153)
        self.assertEqual(
            data['legacy_undefined_behavior_exclusion'][
                'revision53_strip_empty_or_whitespace_only_quoted_payload'
            ],
            'FAIL_CLOSED_NOT_NORMALIZED',
        )


if __name__ == '__main__':
    unittest.main()
