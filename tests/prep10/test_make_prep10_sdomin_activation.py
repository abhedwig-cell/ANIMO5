from __future__ import annotations

import hashlib
import importlib.util
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


def test_controlled_transform_is_length_preserving_and_hashes_descendant():
    parent = fixture()
    descendant, manifest = module.transform(
        parent,
        expected_parent_sha256=sha256(parent),
        indices=[0, 1, 2],
    )
    assert len(descendant) == len(parent)
    assert manifest["parent_sha256"] == sha256(parent)
    assert manifest["descendant_sha256"] == sha256(descendant)
    assert manifest["b0_modified"] is False
    assert b"1.000000E-04" in descendant
    assert b"1.000000E-05" in descendant
    assert b"1.000000E-06" in descendant


def test_parent_hash_mismatch_fails_closed():
    parent = fixture()
    try:
        module.transform(
            parent,
            expected_parent_sha256="0" * 64,
            indices=[0, 1, 2],
        )
    except ValueError as exc:
        assert "parent SHA-256 mismatch" in str(exc)
    else:
        raise AssertionError("hash mismatch was not rejected")


def test_nonzero_selected_parent_token_is_rejected():
    parent = fixture().replace(b"0.000000E+00", b"2.000000E-03", 1)
    try:
        module.transform(
            parent,
            expected_parent_sha256=sha256(parent),
            indices=[0, 1, 2],
        )
    except ValueError as exc:
        assert "is not zero" in str(exc)
    else:
        raise AssertionError("nonzero parent token was not rejected")


def test_duplicate_indices_are_rejected():
    try:
        module.parse_indices("0,1,1")
    except ValueError as exc:
        assert "unique" in str(exc)
    else:
        raise AssertionError("duplicate indices were not rejected")
