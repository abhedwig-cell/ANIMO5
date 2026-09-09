import importlib.util
import pathlib
import unittest


TOOL = pathlib.Path(__file__).resolve().parents[2] / "tools" / "make_prep10_causal_initial.py"
spec = importlib.util.spec_from_file_location("make_prep10_causal_initial", TOOL)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def fixture() -> bytes:
    row = "    " + "    ".join(["0.000000E+00"] * 23) + "\r\n"
    return (
        "header\r\n"
        ">sdomin:\r\n"
        + row
        + row
        + row
        + "tail\r\n"
    ).encode("latin1")


class CausalInitialTransformTests(unittest.TestCase):
    def test_changes_only_indices_one_and_two_per_species_row(self):
        out = module.transform_initial(fixture(), (1e-2, 1e-3, 1e-4))
        lines = out.decode("latin1").splitlines()
        rows = [lines[2].split(), lines[3].split(), lines[4].split()]
        expected = ["1.000000E-02", "1.000000E-03", "1.000000E-04"]
        for tokens, value in zip(rows, expected):
            self.assertEqual(len(tokens), 23)
            self.assertEqual(tokens[0], "0.000000E+00")
            self.assertEqual(tokens[1], value)
            self.assertEqual(tokens[2], value)
            self.assertTrue(all(token == "0.000000E+00" for token in tokens[3:]))

    def test_preserves_crlf_line_endings(self):
        raw = fixture()
        out = module.transform_initial(raw, (1e-2, 0.0, 0.0))
        self.assertEqual(out.count(b"\r\n"), raw.count(b"\r\n"))
        self.assertNotIn(b"\n", out.replace(b"\r\n", b""))

    def test_fails_closed_on_ambiguous_marker(self):
        raw = fixture() + fixture()
        with self.assertRaises(ValueError):
            module.transform_initial(raw, (1e-2, 0.0, 0.0))


if __name__ == "__main__":
    unittest.main()
