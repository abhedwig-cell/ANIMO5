from __future__ import annotations

import hashlib
import importlib.util
import unittest
from pathlib import Path


TOOL = Path(__file__).parents[2] / "tools" / "make_prep10_sdomin_activation.py"
spec = importlib.util.spec_from_file_location("prep10_activation", TOOL)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fixture() -> bytes:
    return (
        b"header\r\n"
        b">sdomin:\r\n"
        b"    0.000000E+00    0.000000E+00    0.000000E+00    0.000000E+00\r\n"
        b"    0.000000E+00    0.000000E+00    0.000000E+00    0.000000E+00\r\n"
        b"    0.000000E+00    0.000000E+00    0.000000E+00    0.000000E+00\r\n"
        b">next:\r\n"
    )


class StableDomActivationTransformTests(unittest.TestCase):
    def test_controlled_transform_is_length_preserving_and_hashes_descendant(self):
        parent = fixture()
        descendant, manifest = module.transform(
            parent,
            expected_parent_sha256=sha256(parent),
            indices=[0, 1, 2],
        )
        self.assertEqual(len(descendant), len(parent))
        self.assertEqual(manifest["parent_sha256"], sha256(parent))
        self.assertEqual(manifest["descendant_sha256"], sha256(descendant))
        self.assertFalse(manifest["b0_modified"])
        self.assertIn(b"1.000000E-04", descendant)
        self.assertIn(b"1.000000E-05", descendant)
        self.assertIn(b"1.000000E-06", descendant)

    def test_parent_hash_mismatch_fails_closed(self):
        parent = fixture()
        with self.assertRaisesRegex(ValueError, "parent SHA-256 mismatch"):
            module.transform(
                parent,
                expected_parent_sha256="0" * 64,
                indices=[0, 1, 2],
            )

    def test_nonzero_selected_parent_token_is_rejected(self):
        parent = fixture().replace(b"0.000000E+00", b"2.000000E-03", 1)
        with self.assertRaisesRegex(ValueError, "is not zero"):
            module.transform(
                parent,
                expected_parent_sha256=sha256(parent),
                indices=[0, 1, 2],
            )

    def test_duplicate_indices_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "unique"):
            module.parse_indices("0,1,1")


if __name__ == "__main__":
    unittest.main()
