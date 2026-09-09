import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from io01_material_pilot import (
    LegacyMaterialParseError,
    NativeMaterialSchemaError,
    NATIVE_KEYS,
    dense_native_fixture,
    parse_legacy_material_text,
    validate_native_material_schema,
)

FIXTURE = """header text
>defmat:
2
1 1 0.1 0.2 0.3 999
2 2 0.4 0.5 0.6 888
>orgcom:
0.58
>deffra:
3
1 1.0 0.75 1.0 0.25 0.07 777
2 0.6 0.75 1.0 0.25 0.05 666
3 0.12 0.75 1.0 0.25 0.01 555
>defexu:
365 1 0.25 0.025 0
>defdom:
30 1 0.25
>defsdo:
1 1
>defhum:
0.02 0 0.25 0.048 0
>defntr:
100
>defden:
0.01 0.5
>matfra:
1 2 1 0.6 0.1
    3 0.4 0
2 1 2 1.0 0.2
"""


class MaterialPilotTests(unittest.TestCase):
    def test_sparse_zero_fill_and_ipo0_residue(self):
        obj = parse_legacy_material_text(FIXTURE)
        self.assertEqual(obj["dimensions"], {"Nm": 2, "Nf": 3})
        self.assertEqual(obj["allocation"]["fr"], [[0.6, 0.0, 0.4], [0.0, 1.0, 0.0]])
        self.assertEqual(obj["allocation"]["frca"], [[0.1, 0.0, 0.0], [0.0, 0.2, 0.0]])
        self.assertIsNone(obj["materials"][0]["frpo"])
        self.assertIsNone(obj["fractions"][0]["pofr"])
        self.assertEqual(obj["legacy_lexical_residue"]["defmat"][0]["tokens"], ["999"])
        self.assertEqual(obj["legacy_lexical_residue"]["deffra"][0]["tokens"], ["777"])

    def test_findadr_first_duplicate_section_wins(self):
        text = FIXTURE.replace(">orgcom:\n0.58", ">orgcom:\n0.60\n>orgcom:\n0.58")
        obj = parse_legacy_material_text(text)
        self.assertEqual(obj["cfracom"], 0.6)

    def test_incomplete_material_index_fails_closed(self):
        text = FIXTURE.replace("2 2 0.4 0.5 0.6 888", "2 1 0.4 0.5 0.6 888")
        with self.assertRaises(LegacyMaterialParseError):
            parse_legacy_material_text(text)

    def test_native_fixture_passes_strict_key_prevalidation(self):
        obj = parse_legacy_material_text(FIXTURE)
        native = dense_native_fixture(obj)
        keys = validate_native_material_schema(native)
        self.assertEqual(set(keys), set(NATIVE_KEYS))

    def test_native_unknown_duplicate_and_missing_rejected(self):
        obj = parse_legacy_material_text(FIXTURE)
        native = dense_native_fixture(obj)
        with self.assertRaises(NativeMaterialSchemaError):
            validate_native_material_schema(native + "Unknown = 1\n")
        with self.assertRaises(NativeMaterialSchemaError):
            validate_native_material_schema(native + "Nm = 2\n")
        with self.assertRaises(NativeMaterialSchemaError):
            validate_native_material_schema(native.replace("Frhetero = '0.5'\n", ""))

    def test_feature_scope_is_fail_closed(self):
        for kwargs in ({"ipo": 1}, {"ioptae": 1}, {"ioptghg": 1}):
            with self.assertRaises(LegacyMaterialParseError):
                parse_legacy_material_text(FIXTURE, **kwargs)


if __name__ == "__main__":
    unittest.main()
