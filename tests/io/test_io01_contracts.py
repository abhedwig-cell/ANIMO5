import csv, json, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

class IO01ContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with (ROOT / 'integration/animo-io/ANIMO_INPUT_CONTRACT_MATRIX.csv').open(encoding='utf-8', newline='') as f:
            cls.rows = list(csv.DictReader(f))
        cls.by = {r['family']: r for r in cls.rows}
        cls.cases = json.loads((ROOT / 'integration/animo-io/TTUTIL_EQUIVALENCE_CASES.json').read_text())
        cls.status = json.loads((ROOT / 'integration/animo-io/ANIMO-IO01_STATUS.json').read_text())

    def test_no_binary_ttutil_admission(self):
        self.assertEqual(self.by['HYDRO_BINARY']['ttutil_suitability'], 'BINARY_OR_RUNTIME_FORMAT_NOT_TTUTIL')

    def test_ghg_lineage_fails_closed(self):
        self.assertEqual(self.by['GHG_SCHEMA']['ttutil_suitability'], 'LINEAGE_UNRESOLVED')
        ghg = [c for c in self.cases['negative_cases'] if c['family'] == 'GHG_SCHEMA']
        self.assertTrue(ghg)
        self.assertTrue(all(c['expected'] == 'LINEAGE_UNRESOLVED_REJECT' for c in ghg))

    def test_state_and_runtime_streams_specialized(self):
        for fam in ['INI','MAN','CROP_EXT','SOIL_TEMP','WATBAL_CFG','RESTART']:
            self.assertEqual(self.by[fam]['ttutil_suitability'], 'KEEP_SPECIALIZED_ADAPTER')

    def test_negative_parser_classes(self):
        required = {'omitted_mandatory_field','duplicate_field','malformed_number','malformed_table','wrong_count','missing_column','empty_value','comment_whitespace_variant','repeated_section_legacy_quirk'}
        observed = {c['class'] for c in self.cases['negative_cases']}
        self.assertTrue(required <= observed)

    def test_non_admissions(self):
        self.assertTrue(all(v is False for v in self.status['non_admissions'].values()))

if __name__ == '__main__':
    unittest.main()
