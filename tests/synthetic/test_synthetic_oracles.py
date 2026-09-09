import importlib.util
from decimal import Decimal as D
from pathlib import Path
import sys
import unittest

MODULE = Path(__file__).resolve().parents[2] / "tools" / "reference" / "synthetic_oracles.py"
spec = importlib.util.spec_from_file_location("synthetic_oracles", MODULE)
so = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules[spec.name] = so
spec.loader.exec_module(so)


class SyntheticOracleTests(unittest.TestCase):
    def test_complete_self_test(self):
        results = so.self_test()
        self.assertTrue(results)
        self.assertTrue(all(v == "PASS" for v in results.values()))

    def test_tcd015_mutation_discriminator(self):
        c = so.No3ClippingCase(D("0.2"), D("0.1"), D("2"), D("0.1"))
        self.assertEqual(c.duplicated_storage_term(), D("0.004"))
        self.assertNotEqual(c.duplicated_storage_term(), c.conservative_residual())

    def test_tcd017_internal_transfer_exact(self):
        r = so.Redistribution(D("0.31"), (D("0.12"), D("0.19")))
        self.assertEqual(r.internal_ledger_sum(), D("0"))

    def test_tcd018_interception_exact(self):
        c = so.InterceptionCase(D("0.06"), D("0.10"), D("0.04"), D("0.08"), D("0.04"))
        self.assertEqual(c.residual(), D("0"))

    def test_tcd023_species_permutation(self):
        conc = (D("2.0"), D("0.2"), D("0.05"))
        common = (D("0.35"), D("0.08"), D("0.2"), D("0.3"))
        expected = so.species_partition_vector(conc, *common)
        order = (2, 0, 1)
        got = so.species_partition_vector(so.permute(conc, order), *common)
        self.assertEqual(got, so.permute(expected, order))

    def test_tcd024_unequal_site_mutation_detected(self):
        sites = (
            so.SlowLangmuirSite(D("0.30"), D("2"), D("0.010"), D("0.20"), D("0.02")),
            so.SlowLangmuirSite(D("0.90"), D("40"), D("0.020"), D("0.07"), D("0.01")),
            so.SlowLangmuirSite(D("0.12"), D("600"), D("0.005"), D("0.015"), D("0.003")),
        )
        correct = so.slow_langmuir_sites(sites, D("0.04"), D("1"), D("1.5"))
        mutant = so.slow_langmuir_wrong_selector_mutant(sites, D("0.04"), D("1"), D("1.5"), 0)
        self.assertNotEqual(correct, mutant)

    def test_tcd025_transfer_and_external_drain(self):
        c = so.MacroporeLedgerCase(D("1"), D("0.4"), D("0.15"), D("0.05"))
        self.assertEqual(c.internal_transfer_sum(), D("0"))
        self.assertEqual(c.whole_control_volume_residual(), D("0"))

    def test_tcd019_high_precision_root(self):
        M, theta, qmax, k = D("0.19"), D("0.35"), D("0.24"), D("125")
        rb, width, _ = so.langmuir_bisection_root(M, theta, qmax, k, 80)
        re = so.langmuir_exact_positive_root(M, theta, qmax, k)
        self.assertLessEqual(abs(rb - re), width)
        residual = abs(so.langmuir_storage(rb, theta, qmax, k) - M)
        self.assertLessEqual(residual, (theta + qmax * k) * width)

    def test_temporal_endpoints(self):
        events = (D("0"), D("0.5"), D("1"))
        self.assertEqual(so.management_events(events, D("0"), D("1")), (D("0.5"), D("1")))
        self.assertEqual(so.harvest_events(events, D("0"), D("1")), (D("0"), D("0.5")))

    def test_limiting_cases(self):
        self.assertTrue(all(so.limiting_case_results().values()))


if __name__ == "__main__":
    unittest.main()
