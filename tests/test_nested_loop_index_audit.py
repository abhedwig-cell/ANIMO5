import importlib.util
import unittest
from pathlib import Path


TOOL = Path(__file__).parents[1] / "tools" / "audit_nested_loop_indices.py"
SPEC = importlib.util.spec_from_file_location("audit_nested_loop_indices", TOOL)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class NestedLoopIndexAuditTest(unittest.TestCase):
    def test_same_position_outer_index_is_flagged(self):
        source = """
      Do 100 I=1,20
        Do 200 J=1,3
          X = A(1,J)
          Y = A(2,J)
          Z = A(3,I)
 200    Continue
 100  Continue
"""
        findings = MODULE.scan_text("synthetic.for", source)
        self.assertEqual(len(findings), 1)
        finding = findings[0]
        self.assertEqual(finding["array"], "a")
        self.assertEqual(finding["argument_position"], 2)
        self.assertEqual(finding["inner_loop"]["variable"], "J")
        self.assertEqual(finding["outer_loop_variable"], "I")

    def test_different_array_positions_are_not_flagged(self):
        source = """
      Do 100 I=1,20
        Do 200 J=1,3
          X = A(I,J)
          Y = A(I,J)
 200    Continue
 100  Continue
"""
        self.assertEqual(MODULE.scan_text("synthetic.for", source), [])

    def test_comments_do_not_create_candidates(self):
        source = """
      Do 100 I=1,20
        Do 200 J=1,3
          X = A(1,J)
!         Z = A(3,I)
 200    Continue
 100  Continue
"""
        self.assertEqual(MODULE.scan_text("synthetic.for", source), [])


if __name__ == "__main__":
    unittest.main()
