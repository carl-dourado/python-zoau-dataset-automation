import tempfile
import unittest
from pathlib import Path

from mainframe_dataset_automation.errors import explain_iebcopy_error


class ErrorParserTests(unittest.TestCase):
    def write_cp1047(self, text: str) -> Path:
        temp = tempfile.NamedTemporaryFile(delete=False)
        path = Path(temp.name)
        temp.close()
        path.write_text(text, encoding="cp037")
        return path

    def test_bad_member_message(self):
        syprint = self.write_cp1047("IEB177I MEMBER5 WAS NOT FOUND\n")

        self.assertEqual(
            explain_iebcopy_error(syprint, "ZXP.PUBLIC.J2PDATA", "Z49216.OUTPUT"),
            "Member MEMBER5 is not in dataset ZXP.PUBLIC.J2PDATA.",
        )

    def test_missing_syprint_is_unchecked(self):
        message = explain_iebcopy_error("/tmp/not-a-real-syprint-file", "A.B", "C.D")

        self.assertIn("z/OS unchecked error", message)


if __name__ == "__main__":
    unittest.main()
