import unittest

from mainframe_dataset_automation.core import (
    CopyRequest,
    ValidationError,
    build_iebcopy_control_cards,
    build_tk5_iebcopy_jcl,
)


class CoreTests(unittest.TestCase):
    def test_request_normalizes_values(self):
        request = CopyRequest.from_values("zxp.public.j2pdata", "z49216.output", ["member1", "member6"])

        self.assertEqual(request.input_dataset, "ZXP.PUBLIC.J2PDATA")
        self.assertEqual(request.output_dataset, "Z49216.OUTPUT")
        self.assertEqual(request.members, ("MEMBER1", "MEMBER6"))

    def test_invalid_member_is_rejected(self):
        with self.assertRaises(ValidationError):
            CopyRequest.from_values("ZXP.PUBLIC.J2PDATA", "Z49216.OUTPUT", ["member-name-too-long"])

    def test_control_cards_match_iebcopy_shape(self):
        self.assertEqual(
            build_iebcopy_control_cards(["member1", "member6"]),
            [" COPY OUTDD=OUTDS,INDD=INDS", " SELECT MEMBER=(MEMBER1,MEMBER6)"],
        )

    def test_tk5_jcl_contains_dataset_dds_and_control_cards(self):
        request = CopyRequest.from_values("ZXP.PUBLIC.J2PDATA", "Z49216.OUTPUT", ["MEMBER1", "MEMBER6"])

        jcl = build_tk5_iebcopy_jcl(request, "cpyj2p1")

        self.assertIn("//CPYJ2P1  JOB (TK5),'IEBCOPY DEMO'", jcl)
        self.assertIn("//COPY     EXEC PGM=IEBCOPY", jcl)
        self.assertIn("//INDS     DD DSN=ZXP.PUBLIC.J2PDATA,DISP=SHR", jcl)
        self.assertIn("//OUTDS    DD DSN=Z49216.OUTPUT,DISP=OLD", jcl)
        self.assertIn(" SELECT MEMBER=(MEMBER1,MEMBER6)", jcl)


if __name__ == "__main__":
    unittest.main()
