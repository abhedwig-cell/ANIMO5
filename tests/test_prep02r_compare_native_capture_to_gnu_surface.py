import importlib.util
import tempfile
import unittest
from pathlib import Path

TOOL = (
    Path(__file__).resolve().parents[1]
    / "tools"
    / "prep02r_compare_native_capture_to_gnu_surface.py"
)
spec = importlib.util.spec_from_file_location("prep02r_cross_runtime_surface", TOOL)
cross = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cross)


class FakeComparator:
    def normalize_legacy_text(self, data):
        text = data.decode("latin1")
        import re

        text, count = re.subn(
            r" File created on [^\n]+",
            " File created on <VOLATILE_TIMESTAMP>.",
            text,
        )
        return text.encode("latin1"), {"file_creation_timestamp": count}


class FakeValidator:
    @staticmethod
    def inventory(root):
        records = []
        for path in sorted(p for p in root.rglob("*") if p.is_file()):
            data = path.read_bytes()
            records.append(
                {
                    "path": path.relative_to(root).as_posix(),
                    "size": len(data),
                    "sha256": cross.sha256_bytes(data),
                }
            )
        return records

    @staticmethod
    def delta(baseline, post):
        before = {item["path"]: item for item in baseline}
        after = {item["path"]: item for item in post}
        changed = [
            item
            for item in post
            if item["path"] not in before
            or item["sha256"] != before[item["path"]]["sha256"]
        ]
        deleted = [item for item in baseline if item["path"] not in after]
        return changed, deleted


def make_surface(files):
    rows = []
    comparator = FakeComparator()
    for path, data in files.items():
        normalized, _ = comparator.normalize_legacy_text(data)
        rows.append(
            {
                "path": path,
                "normalized_size": len(normalized),
                "normalized_sha256": cross.sha256_bytes(normalized),
            }
        )
    rows.sort(key=lambda item: item["path"])
    return {
        "schema": cross.EXPECTED_SURFACE_SCHEMA,
        "evidence_class": cross.EXPECTED_SURFACE_CLASS,
        "work_unit": "ANIMO-PREP02R",
        "case": "RuurloGrass",
        "source_zip_sha256": cross.EXPECTED_SOURCE_SHA256,
        "testbank_zip_sha256": cross.EXPECTED_TESTBANK_SHA256,
        "gnu_diagnostic_executable_sha256": cross.EXPECTED_GNU_EXE_SHA256,
        "historical_reference_admitted": False,
        "normal_B2_reference_available": False,
        "volatile_normalization": {
            "scientific_numeric_tolerance_applied": False
        },
        "files": rows,
        "surface_definition": {
            "changed_or_new_file_count": len(rows),
            "normalized_surface_content_set_sha256": cross._content_set_sha256(rows),
        },
    }


class TestCrossRuntimeSurface(unittest.TestCase):
    def test_surface_validation_recomputes_content_set(self):
        surface = make_surface({"x.out": b"value 1\n"})
        self.assertEqual(cross.validate_surface(surface), [])
        surface["files"][0]["normalized_sha256"] = "0" * 64
        self.assertTrue(cross.validate_surface(surface))

    def test_declared_volatile_difference_matches(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "x.out").write_bytes(
                b" File created on B\nvalue 1\n"
            )
            surface = make_surface(
                {"x.out": b" File created on A\nvalue 1\n"}
            )
            report = cross.compare_case_to_surface(
                root,
                [],
                surface,
                FakeComparator(),
                FakeValidator(),
            )
            self.assertEqual(report["decision"], "MATCH_EXPLICIT_GNU_SURFACE")
            self.assertFalse(report["scientific_numeric_tolerance_applied"])

    def test_numeric_difference_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "x.out").write_bytes(b"value 2\n")
            surface = make_surface({"x.out": b"value 1\n"})
            report = cross.compare_case_to_surface(
                root,
                [],
                surface,
                FakeComparator(),
                FakeValidator(),
            )
            self.assertEqual(report["decision"], "DIFFERENT_FAIL_CLOSED")
            self.assertEqual(report["different_normalized_files"], ["x.out"])

    def test_extra_file_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "x.out").write_bytes(b"value 1\n")
            (root / "extra.out").write_bytes(b"e\n")
            surface = make_surface({"x.out": b"value 1\n"})
            report = cross.compare_case_to_surface(
                root,
                [],
                surface,
                FakeComparator(),
                FakeValidator(),
            )
            self.assertEqual(report["decision"], "DIFFERENT_FAIL_CLOSED")
            self.assertEqual(report["extra_native_paths"], ["extra.out"])

    def test_missing_file_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            surface = make_surface({"x.out": b"value 1\n"})
            report = cross.compare_case_to_surface(
                root,
                [],
                surface,
                FakeComparator(),
                FakeValidator(),
            )
            self.assertEqual(report["decision"], "DIFFERENT_FAIL_CLOSED")
            self.assertEqual(report["missing_expected_paths"], ["x.out"])


if __name__ == "__main__":
    unittest.main()
