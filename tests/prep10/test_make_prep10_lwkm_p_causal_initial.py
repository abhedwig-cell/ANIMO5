import importlib.util
import pathlib
import unittest


TOOL = pathlib.Path(__file__).resolve().parents[2] / "tools" / "make_prep10_lwkm_p_causal_initial.py"
spec = importlib.util.spec_from_file_location("make_prep10_lwkm_p_causal_initial", TOOL)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def fixture() -> bytes:
    row = "    " + "    ".join(["0.000000E+00"] * 31) + "\r\n"
    return ("header\r\n>sdomin:\r\n" + row + row + row + "tail\r\n").encode("latin1")


class LwkmPhosphorusCausalTransformTests(unittest.TestCase):
    def test_changes_only_stable_dop_indices_one_and_two(self):
        out = module.transform_initial(fixture())
        lines = out.decode("latin1").splitlines()
        dom = lines[2].split()
        don = lines[3].split()
        dop = lines[4].split()
        self.assertTrue(all(value == "0.000000E+00" for value in dom))
        self.assertTrue(all(value == "0.000000E+00" for value in don))
        self.assertEqual(dop[1], "1.000000E-04")
        self.assertEqual(dop[2], "1.000000E-04")
        self.assertEqual(dop[0], "0.000000E+00")
        self.assertTrue(all(value == "0.000000E+00" for value in dop[3:]))

    def test_preserves_crlf(self):
        raw = fixture()
        out = module.transform_initial(raw)
        self.assertEqual(out.count(b"\r\n"), raw.count(b"\r\n"))
        self.assertNotIn(b"\n", out.replace(b"\r\n", b""))

    def test_fails_closed_when_target_is_not_frozen_zero(self):
        raw = fixture().replace(
            b"0.000000E+00    0.000000E+00    0.000000E+00",
            b"0.000000E+00    1.000000E-05    0.000000E+00",
            1,
        )
        # The first replacement is in the DOM row, so move the nonzero token into DOP.
        lines = raw.decode("latin1").splitlines(keepends=True)
        dop = lines[4].split()
        dop[1] = "1.000000E-05"
        lines[4] = "    " + "    ".join(dop) + "\r\n"
        with self.assertRaises(ValueError):
            module.transform_initial("".join(lines).encode("latin1"))


if __name__ == "__main__":
    unittest.main()
