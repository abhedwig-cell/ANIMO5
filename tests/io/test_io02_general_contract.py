import unittest

from tools.io02_general_contract import (
    General41Parser,
    LegacyGrammarError,
    OUTSEL_GROUPS,
)


def make_general(*, pclass_line=True, hydro_year=0, balance_dates=None, ghg=0):
    lines = [
        ">simopt:",
        "HydrologicInput=       2!",
        "PhosphorusCycle=       0!",
        "SulphateSimulation=    0!",
        "AerationModel=         0!",
        "CropUptakeModel=       0!",
        "MacroPoreOption=       0!",
        f"GreenHouseGasOption=   {ghg}!",
        "SoilTempFile=          0!",
    ]
    if pclass_line:
        lines.append("PClassOption=          0!")
    lines.extend(
        [
            ">simtim:",
            "StartDate=          2000-01-01!",
            "EndDate=            2001-12-31!",
            f"HydroYearSwitch=     {hydro_year}!",
            ">outscr:",
            "ProgressToScreen=     1!",
            ">outbal:",
            "NumberOfPrintBal=      1!",
            "PrintBalLabel= 'AA'!",
            "PrintBalWater=         1!",
            "PrintBalOrgMat=        1!",
            "PrintBalNitrogen=      1!",
            "PrintBalPhosphor=      0!",
            "PrintBalSulphate=      0!",
            "PrintBalTopLay=        0!",
            "PrintBalBotLay=        3!",
        ]
    )
    if balance_dates is None:
        lines.append("PrintBalNoUpd=        -1!")
    else:
        lines.append(f"PrintBalNoUpd=         {len(balance_dates)}!")
        lines.append(
            "PrintBalUpdDate= " + " ".join(str(x) for x in balance_dates) + "!"
        )
    lines.extend([">outsel:", "SelectedComp=           0!"])
    for group, fields in OUTSEL_GROUPS:
        lines.append(f"[{group}]")
        for key, _ in fields:
            lines.append(f"{key} 0!")
    lines.extend(
        [
            ">outtot:",
            "IntMedOutputTS=        0!",
            "NumIntMedOutputTS=     0!",
            "IntMedOutFromStart=",
        ]
    )
    if ghg >= 1:
        lines.extend([">outGHG:", "payload deliberately not parsed by IO02"])
    return "\n".join(lines) + "\n"


def record(parsed, field_id):
    return next(r for r in parsed["records"] if r["field_id"] == field_id)


class General41ContractTests(unittest.TestCase):
    def test_valid_bounded_fixture_projects_to_typed_targets(self):
        parsed = General41Parser(make_general()).parse()
        self.assertEqual(
            parsed["projection"]["model_configuration"]["hydrology_input"], 2
        )
        self.assertEqual(
            parsed["projection"]["simulation_window"]["start_date"], "2000-01-01"
        )
        self.assertEqual(
            parsed["projection"]["diagnostics_configuration"]["balances.count"], 1
        )

    def test_key_order_inside_simopt_is_strict(self):
        text = make_general()
        text = text.replace(
            "HydrologicInput=       2!\nPhosphorusCycle=       0!",
            "PhosphorusCycle=       0!\nHydrologicInput=       2!",
            1,
        )
        with self.assertRaises(LegacyGrammarError) as caught:
            General41Parser(text).parse()
        self.assertEqual(caught.exception.code, "9870")

    def test_label_is_exact_first_eight_characters(self):
        text = make_general().replace(">outscr:", ">outsXX:", 1)
        with self.assertRaises(LegacyGrammarError) as caught:
            General41Parser(text).parse()
        self.assertEqual(caught.exception.code, "1995")

    def test_pclass_omission_is_explicit_legacy_default(self):
        parsed = General41Parser(make_general(pclass_line=False)).parse()
        item = record(parsed, "PClassOption=")
        self.assertEqual(item["value"], 0)
        self.assertEqual(item["presence"], "DEFAULTED")
        self.assertEqual(item["default_rule_id"], "GEN-DEF-PCLASSOPTION-0")

    def test_hydro_year_switch_negative_value_is_preserved(self):
        parsed = General41Parser(make_general(hydro_year=-30)).parse()
        self.assertEqual(record(parsed, "HydroYearSwitch=")["value"], -30)

    def test_readts_scans_comment_not_numeric_token(self):
        text = make_general().replace(
            "Nitrate= 0!", "Nitrate= nonsense! comment selector 3", 1
        )
        parsed = General41Parser(text).parse()
        self.assertEqual(
            record(parsed, "Nitrate=")["value"],
            {"file_output": 1, "selected_compartment_output": 1},
        )

    def test_balance_update_dates_are_post_parser_sorted(self):
        parsed = General41Parser(make_general(balance_dates=[300.0, 100.0])).parse()
        item = record(parsed, "PrintBalUpdDate=")
        self.assertEqual(item["value"], [100.0, 300.0])
        self.assertEqual(item["value_type"], "REAL(8)_ARRAY")

    def test_optional_last_outputs_do_not_get_fabricated_line_flag(self):
        text = make_general()
        text = text.replace("AnnDOMNtotNO3_1mGWL= 0!\n", "", 1)
        text = text.replace("DOMNtotNO3_1mGWL= 0!\n", "", 1)
        parsed = General41Parser(text).parse()
        for key in ("AnnDOMNtotNO3_1mGWL=", "DOMNtotNO3_1mGWL="):
            item = record(parsed, key)
            self.assertEqual(item["value"]["file_output"], 0)
            self.assertEqual(
                item["value"]["selected_compartment_output"],
                "LEGACY_UNDEFINED_IF_OMITTED",
            )

    def test_whole_profile_second_selector_bit_is_discarded_to_idum(self):
        text = make_general().replace("Disch+Transport= 0!", "Disch+Transport= 3!", 1)
        parsed = General41Parser(text).parse()
        self.assertEqual(
            record(parsed, "Disch+Transport=")["value"],
            {
                "file_output": 1,
                "selected_compartment_output": "NOT_APPLICABLE_DISCARDED_TO_IDUM",
            },
        )

    def test_date_record_key_name_is_not_normalized_as_source_semantics(self):
        baseline = General41Parser(make_general()).parse()["projection"]
        renamed = make_general().replace(
            "StartDate=          2000-01-01!",
            "NotAStart=          2000-01-01!",
            1,
        )
        self.assertEqual(General41Parser(renamed).parse()["projection"], baseline)

    def test_ghg_is_routed_but_payload_not_admitted(self):
        parsed = General41Parser(make_general(ghg=1)).parse()
        self.assertEqual(
            parsed["meta"]["routes"][0]["status"], "NOT_ADMITTED"
        )
        self.assertEqual(
            parsed["meta"]["routes"][0]["route"], "GHG_SCHEMA_LINEAGE_UNRESOLVED"
        )


if __name__ == "__main__":
    unittest.main()
