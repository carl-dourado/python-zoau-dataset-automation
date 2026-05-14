import tempfile
import unittest
from pathlib import Path

from mainframe_dataset_automation.core import CopyRequest
from mainframe_dataset_automation.mock_runner import MockDatasetRunner


class MockRunnerTests(unittest.TestCase):
    def test_mock_copy_creates_output_members(self):
        with tempfile.TemporaryDirectory() as root:
            root_path = Path(root)
            source = root_path / "ZXP.PUBLIC.J2PDATA"
            source.mkdir(parents=True)
            (source / "MEMBER1").write_text("one\n", encoding="utf-8")
            (source / "MEMBER6").write_text("six\n", encoding="utf-8")

            request = CopyRequest.from_values("ZXP.PUBLIC.J2PDATA", "Z49216.OUTPUT", ["MEMBER1", "MEMBER6"])
            result = MockDatasetRunner(root_path).copy_members(request)

            self.assertTrue(result.ok)
            self.assertEqual(result.copied_members, ("MEMBER1", "MEMBER6"))
            self.assertEqual((root_path / "Z49216.OUTPUT" / "MEMBER1").read_text(encoding="utf-8"), "one\n")

    def test_mock_copy_reports_missing_member(self):
        with tempfile.TemporaryDirectory() as root:
            source = Path(root) / "ZXP.PUBLIC.J2PDATA"
            source.mkdir(parents=True)
            request = CopyRequest.from_values("ZXP.PUBLIC.J2PDATA", "Z49216.OUTPUT", ["MEMBER5"])
            result = MockDatasetRunner(root).copy_members(request)

            self.assertEqual(result.rc, 12)
            self.assertIn("MEMBER5", result.message)


if __name__ == "__main__":
    unittest.main()
