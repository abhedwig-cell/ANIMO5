from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any
import re


TOP_LEVEL_LABEL_CALL_ORDER = [
    ">simopt:",
    ">simtim:",
    ">outscr:",
    ">outbal:",
    ">outsel:",
    ">outtot:",
]

OUTSEL_GROUPS = [
    (
        "Hydrology",
        [
            ("MoistureFraction=", 6),
            ("VerticalFlux=", 72),
            ("DrainFlux3=", 31),
            ("DrainFlux2=", 32),
            ("DrainFlux1=", 33),
            ("SoilTemperature=", 71),
        ],
    ),
    (
        "Nitrogen",
        [
            ("Nitrate=", 1),
            ("Ammonium=", 2),
            ("SorbedNH4=", 7),
            ("MineralN=", 8),
            ("TotalN=", 10),
            ("SolidOrgN=", 9),
            ("DissOrgN=", 3),
            ("SorbedDON=", 60),
            ("TotalDON=", 61),
            ("StableDissOrgN=", 62),
            ("SorbedStableDON=", 63),
            ("TotalSorbedDON=", 64),
            ("TimeAveLiquidN=", 38),
        ],
    ),
    (
        "Phosphorus",
        [
            ("orthoP=", 4),
            ("DissOrgP=", 5),
            ("SorbedDOP=", 65),
            ("TotalDOP=", 66),
            ("StableDissOrgP=", 67),
            ("SorbedStableDOP=", 68),
            ("TotalSorbedDOP=", 69),
            ("SolidOrgP=", 14),
            ("SorbedP=", 11),
            ("Sorbed_LiquidP=", 12),
            ("PrecipitatedP=", 13),
            ("TotalP=", 15),
            ("Pw-number=", 16),
            ("PAL-number=", 17),
            ("P-oxalate-extr=", 20),
            ("Psaturationdegree=", 75),
            ("PsorpEquiPool_1=", 21),
            ("PsorpEquiPool_2=", 22),
            ("PsorpEquiPool_3=", 23),
            ("PsorpRatePool_1=", 24),
            ("PsorpRatePool_2=", 25),
            ("PsorpRatePool_3=", 26),
            ("PsorpRatePoolSum=", 27),
            ("Pdischarge3=", 28),
            ("Pdischarge2=", 29),
            ("Pdischarge1=", 30),
            ("TimeAveLiquidP=", 39),
        ],
    ),
    (
        "OrganicMatter",
        [
            ("Ratio_CN=", 18),
            ("Ratio_CP=", 19),
            ("DissOrgMat=", 40),
            ("SorbedDOM=", 55),
            ("TotalDOM=", 56),
            ("StableDissOrgMat=", 57),
            ("SorbedStableDOM=", 58),
            ("TotalStableDOM=", 59),
            ("LiquidDOM_SDO=", 70),
        ],
    ),
    (
        "Aeration",
        [
            ("O2_content=", 34),
            ("AerationFrac=", 35),
            ("PotDenitrif=", 74),
            ("ActDenitrif=", 36),
            ("SoilRespiration=", 73),
        ],
    ),
    (
        "GreenHouseGasses",
        [
            ("CO2emission=", 41),
            ("SoilSubsidence=", 42),
            ("CH4_SoilConc=", 44),
            ("CH4_WaterConc=", 45),
            ("CH4production=", 46),
            ("CH4oxidation=", 47),
            ("N2O_SoilConc=", 49),
            ("N2O_WaterConc=", 50),
            ("N2Oprod_denitr=", 51),
            ("N2Oprod_nitrif=", 52),
            ("N2Oreduction=", 53),
        ],
    ),
    (
        "WholeProfile",
        [
            ("Disch+Transport=", 37),
            ("CH4emission=", 43),
            ("N2Oemission=", 48),
            ("AnnualGHG=", 54),
            ("Grassland=", None),
            ("DetailedCycles=", None),
            ("SoilScheme=", 76),
            ("AnnDOMNtotNO3_1mGWL=", 77),
            ("DOMNtotNO3_1mGWL=", 78),
        ],
    ),
]

OPTIONAL_READTS_DEFAULT_KEYS = {
    "AnnDOMNtotNO3_1mGWL=",
    "DOMNtotNO3_1mGWL=",
}

WHOLE_PROFILE_IDUM_KEYS = {
    "Disch+Transport=",
    "CH4emission=",
    "N2Oemission=",
    "AnnualGHG=",
    "Grassland=",
    "DetailedCycles=",
}


class LegacyGrammarError(ValueError):
    def __init__(self, code: str, message: str, line: int | None = None):
        self.code = code
        self.line = line
        super().__init__(message)


@dataclass
class Record:
    field_id: str
    normalized_name: str
    value: Any
    value_type: str
    target_object: str
    target_path: str
    section: str
    sequence_index: int
    source_line: int | None
    lexical_form: str | None
    presence: str = "EXPLICIT"
    default_rule_id: str | None = None
    feature_condition: str | None = None
    repeat_index: int | None = None
    legacy_parser_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class Cursor:
    def __init__(self, lines: list[str], pos: int):
        self.lines = lines
        self.pos = pos

    def next(self) -> tuple[int, str]:
        if self.pos >= len(self.lines):
            raise LegacyGrammarError("EOF", "unexpected EOF", len(self.lines) + 1)
        i = self.pos
        self.pos += 1
        return i + 1, self.lines[i]


class General41Parser:
    """Bounded revision-53 GENERAL.INP representation observer.

    This is qualification tooling, not a production parser. It preserves the admitted
    source ordering and default rules and fails closed on source hazards for which IO02
    does not claim a deterministic normalized meaning. GHG `>outGHG:` payload is routed
    but never admitted by this parser.
    """

    def __init__(self, text: str, manl: int = 200, maba: int = 10):
        self.lines = text.splitlines()
        self.manl = manl
        self.maba = maba
        self.records: list[Record] = []
        self.meta: dict[str, Any] = {
            "consumed_separators": [],
            "source_defaults": [],
            "routes": [],
            "legacy_storage_hazards": [
                "OUTSEL_WHOLE_PROFILE_OUTSELN_37_43_48_54_NOT_ASSIGNED_BEFORE_GLOBAL_RANGE_CHECK",
                "OPTIONAL_OUTSEL_77_78_OMISSION_LEAVES_OUTSELN_UNASSIGNED",
                "READTS_LATE_OPTIONAL_MISMATCH_CAN_CLEAR_PRIOR_ERROR_9871",
            ],
        }
        self._seq: dict[str, int] = {}

    def _add(
        self,
        section: str,
        field_id: str,
        value: Any,
        value_type: str,
        target_object: str,
        target_path: str,
        line: int | None,
        lexical: str | None,
        *,
        presence: str = "EXPLICIT",
        default_rule_id: str | None = None,
        feature_condition: str | None = None,
        repeat_index: int | None = None,
        parser_path: str | None = None,
    ) -> None:
        idx = self._seq.get(section, 0) + 1
        self._seq[section] = idx
        self.records.append(
            Record(
                field_id,
                field_id.rstrip("="),
                value,
                value_type,
                target_object,
                target_path,
                section,
                idx,
                line,
                lexical,
                presence,
                default_rule_id,
                feature_condition,
                repeat_index,
                parser_path,
            )
        )

    def _find(self, label: str) -> Cursor:
        # Findadr rewinds on every call and compares exactly A8.
        for i, line in enumerate(self.lines):
            if line[:8] == label:
                return Cursor(self.lines, i + 1)
        raise LegacyGrammarError("1995", f"label {label!r} not found")

    @staticmethod
    def _eq_pos(line: str) -> int:
        return line.find("=")

    @staticmethod
    def _bang_pos(line: str) -> int:
        return line.find("!")

    def _read_op(self, c: Cursor, key: str) -> tuple[int, int, str]:
        try:
            ln, line = c.next()
        except LegacyGrammarError as exc:
            if exc.code == "EOF":
                raise LegacyGrammarError(
                    "9870", f"EOF while ordered key {key} was required", exc.line
                ) from exc
            raise
        eq = self._eq_pos(line)
        if eq < 0 or line[: eq + 1] != key[: eq + 1]:
            raise LegacyGrammarError(
                "9870", f"expected ordered key {key}, got {line!r}", ln
            )
        bang = self._bang_pos(line)
        if bang < 0:
            raise LegacyGrammarError(
                "LEXICAL_NO_BANG",
                f"ReadOp requires bounded value before ! for admitted representation: {key}",
                ln,
            )
        token = line[eq + 1 : bang].strip()
        try:
            value = int(token.split()[0])
        except Exception as exc:
            raise LegacyGrammarError(
                "LEXICAL_INT", f"invalid integer for {key}: {token!r}", ln
            ) from exc
        return ln, value, line

    def _read_op_default_on_mismatch(
        self, c: Cursor, key: str, default: int, rule: str
    ) -> tuple[int | None, int, str | None, str]:
        # Exact source path consumes one record via ReadOp, then the caller clears
        # Error and assigns the compatibility default.
        saved_pos = c.pos
        try:
            ln, value, line = self._read_op(c, key)
            return ln, value, line, "EXPLICIT"
        except LegacyGrammarError as exc:
            if exc.code != "9870":
                raise
            consumed_line = (
                self.lines[saved_pos] if saved_pos < len(self.lines) else None
            )
            self.meta["source_defaults"].append(
                {
                    "key": key,
                    "rule": rule,
                    "consumed_line": saved_pos + 1 if consumed_line is not None else None,
                }
            )
            return None, default, None, "DEFAULTED"

    def _read_ints(
        self, c: Cursor, key: str, dim: int
    ) -> tuple[int, list[int], str]:
        try:
            ln, line = c.next()
        except LegacyGrammarError as exc:
            if exc.code == "EOF":
                raise LegacyGrammarError(
                    "9870",
                    f"EOF while ordered integer array {key} was required",
                    exc.line,
                ) from exc
            raise
        eq, bang = self._eq_pos(line), self._bang_pos(line)
        if eq < 0 or line[: eq + 1] != key[: eq + 1]:
            raise LegacyGrammarError(
                "9870", f"expected ordered key {key}, got {line!r}", ln
            )
        if dim == 0:
            # Source still issues the internal read for a zero-size section. The
            # normalized cardinality is zero and no numeric value is admitted.
            return ln, [], line
        if bang < 0:
            raise LegacyGrammarError(
                "LEXICAL_NO_BANG",
                f"Readints requires ! terminator for positive cardinality: {key}",
                ln,
            )
        toks = line[eq + 1 : bang].replace(",", " ").split()
        if len(toks) < dim:
            raise LegacyGrammarError(
                "LEXICAL_CARDINALITY",
                f"{key} expected {dim} ints, got {len(toks)}",
                ln,
            )
        try:
            vals = [int(x) for x in toks[:dim]]
        except Exception as exc:
            raise LegacyGrammarError(
                "LEXICAL_INT", f"invalid integer array for {key}", ln
            ) from exc
        return ln, vals, line

    def _read_reals(
        self, c: Cursor, key: str, dim: int
    ) -> tuple[int, list[float], list[str], str]:
        try:
            ln, line = c.next()
        except LegacyGrammarError as exc:
            if exc.code == "EOF":
                raise LegacyGrammarError(
                    "9870",
                    f"EOF while ordered real array {key} was required",
                    exc.line,
                ) from exc
            raise
        eq, bang = self._eq_pos(line), self._bang_pos(line)
        if eq < 0 or line[: eq + 1] != key[: eq + 1]:
            raise LegacyGrammarError(
                "9870", f"expected ordered key {key}, got {line!r}", ln
            )
        if dim <= 0:
            return ln, [], [], line
        if bang < 0:
            raise LegacyGrammarError(
                "LEXICAL_NO_BANG",
                f"Readvals requires ! terminator for positive cardinality: {key}",
                ln,
            )
        toks = line[eq + 1 : bang].replace(",", " ").split()
        if len(toks) < dim:
            raise LegacyGrammarError(
                "LEXICAL_CARDINALITY",
                f"{key} expected {dim} reals, got {len(toks)}",
                ln,
            )
        vals: list[float] = []
        for token in toks[:dim]:
            try:
                # Python float is IEEE binary64. The supplied Intel project uses
                # RealKIND=realKIND8, so this is the admitted executable build kind.
                vals.append(float(token.replace("D", "E").replace("d", "e")))
            except Exception as exc:
                raise LegacyGrammarError(
                    "LEXICAL_REAL", f"invalid real {token!r} for {key}", ln
                ) from exc
        return ln, vals, toks[:dim], line

    def _read_ts(
        self, c: Cursor, key: str
    ) -> tuple[int | None, int, int | None, str | None, str]:
        try:
            ln, line = c.next()
        except LegacyGrammarError as exc:
            if exc.code != "EOF":
                raise
            if key in OPTIONAL_READTS_DEFAULT_KEYS:
                self.meta["source_defaults"].append(
                    {
                        "key": key,
                        "rule": "READTS_OPTIONAL_OUTPUT_DEFAULT_DISABLED",
                        "consumed_line": None,
                    }
                )
                return (
                    None,
                    0,
                    None,
                    None,
                    "DEFAULTED_LEGACY_LINE_SELECTOR_UNDEFINED",
                )
            raise LegacyGrammarError(
                "9871",
                f"EOF while ordered output selector {key} was required",
                exc.line,
            ) from exc

        eq = self._eq_pos(line)
        if eq < 0:
            # Exact zero-length substring behavior for L1=0 is not widened into
            # the admitted malformed grammar.
            if key in OPTIONAL_READTS_DEFAULT_KEYS:
                self.meta["source_defaults"].append(
                    {
                        "key": key,
                        "rule": "READTS_OPTIONAL_OUTPUT_DEFAULT_DISABLED",
                        "consumed_line": ln,
                    }
                )
                return (
                    None,
                    0,
                    None,
                    None,
                    "DEFAULTED_LEGACY_LINE_SELECTOR_UNDEFINED",
                )
            raise LegacyGrammarError(
                "UNADMITTED_READTS_NO_EQUALS",
                f"no = in ordered output selector record for {key}",
                ln,
            )

        if line[: eq + 1] != key[: eq + 1]:
            if key in OPTIONAL_READTS_DEFAULT_KEYS:
                # Source sets jout=0 and Error=0 but leaves ioutLn untouched.
                self.meta["source_defaults"].append(
                    {
                        "key": key,
                        "rule": "READTS_OPTIONAL_OUTPUT_DEFAULT_DISABLED",
                        "consumed_line": ln,
                    }
                )
                return (
                    None,
                    0,
                    None,
                    None,
                    "DEFAULTED_LEGACY_LINE_SELECTOR_UNDEFINED",
                )
            raise LegacyGrammarError(
                "9871", f"expected ordered output selector {key}, got {line!r}", ln
            )

        # ReadTs is not conventional integer conversion. It scans every character
        # after '=' through column 132 and takes the first digit 0, 1, 2 or 3.
        for ch in line[eq + 1 :]:
            if ch in "0123":
                code = int(ch)
                jout = 1 if code in (1, 3) else 0
                outln = 1 if code in (2, 3) else 0
                return ln, jout, outln, line, "EXPLICIT"
        raise LegacyGrammarError(
            "9871", f"no selector digit 0..3 found for {key}", ln
        )

    @staticmethod
    def _parse_date_record(line: str, ln: int) -> tuple[str, tuple[int, int, int]]:
        # Revision-53 does not validate StartDate=/EndDate= names. It derives
        # L3beg from fixed substring positions and then reads fixed YYYY/MM/DD
        # offsets. All admitted natural files use the canonical layout with the
        # date at columns 21..30 and '!' at column 31. IO02 qualifies that
        # bounded layout only instead of broadening the grammar.
        if len(line) < 31 or line[30] != "!":
            raise LegacyGrammarError(
                "UNADMITTED_DATE_LAYOUT",
                "bounded revision-53 date record requires ! at column 31",
                ln,
            )
        token = line[20:30]
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", token):
            raise LegacyGrammarError(
                "UNADMITTED_DATE_LAYOUT",
                f"bounded revision-53 date token at columns 21..30 is invalid: {token!r}",
                ln,
            )
        year, month, day = map(int, token.split("-"))
        return token, (year, month, day)

    def parse(self) -> dict[str, Any]:
        c = self._find(">simopt:")
        opts = [
            ("HydrologicInput=", "hydrology_input", 1, 2),
            ("PhosphorusCycle=", "phosphorus_cycle", 0, 1),
            ("SulphateSimulation=", "sulphate_simulation", 0, 1),
            ("AerationModel=", "aeration_model", 0, 2),
            ("CropUptakeModel=", "crop_uptake_model", 0, 1),
            ("MacroPoreOption=", "macropore_option", 0, 1),
            ("GreenHouseGasOption=", "greenhouse_gas_option", 0, 2),
            ("SoilTempFile=", "soil_temperature_file", 0, 1),
        ]
        values: dict[str, int] = {}
        for key, path, low, high in opts:
            ln, value, lexical = self._read_op(c, key)
            if not low <= value <= high:
                raise LegacyGrammarError(
                    "1990/1991", f"{key}={value} outside {low}..{high}", ln
                )
            values[key] = value
            self._add(
                "simopt",
                key,
                value,
                "INTEGER",
                "ModelConfiguration",
                path,
                ln,
                lexical,
                parser_path="Findadr>ReadOp",
            )

        ln, value, lexical, presence = self._read_op_default_on_mismatch(
            c, "PClassOption=", 0, "GEN-DEF-PCLASSOPTION-0"
        )
        if not 0 <= value <= 1:
            raise LegacyGrammarError(
                "1990/1991", f"PClassOption={value} outside 0..1", ln
            )
        values["PClassOption="] = value
        self._add(
            "simopt",
            "PClassOption=",
            value,
            "INTEGER",
            "ModelConfiguration",
            "p_class.option",
            ln,
            lexical,
            presence=presence,
            default_rule_id=(
                None if presence == "EXPLICIT" else "GEN-DEF-PCLASSOPTION-0"
            ),
            parser_path="ReadOp + caller error clear/default",
        )

        if value == 1:
            ln, year_switch, lexical = self._read_op(c, "PClassYearSwitch=")
            self._add(
                "simopt",
                "PClassYearSwitch=",
                year_switch,
                "INTEGER",
                "ModelConfiguration",
                "p_class.year_switch",
                ln,
                lexical,
                feature_condition="PClassOption=1",
                parser_path="ReadOp",
            )
            ln, pclass, lexical = self._read_op(c, "PClass=")
            if not 1 <= pclass <= 3:
                raise LegacyGrammarError(
                    "1990/1991", f"PClass={pclass} outside 1..3", ln
                )
            self._add(
                "simopt",
                "PClass=",
                pclass,
                "INTEGER",
                "ModelConfiguration",
                "p_class.class",
                ln,
                lexical,
                feature_condition="PClassOption=1",
                parser_path="ReadOp",
            )
        else:
            self._add(
                "simopt",
                "PClassYearSwitch=",
                0,
                "INTEGER",
                "ModelConfiguration",
                "p_class.year_switch",
                None,
                None,
                presence="DEFAULTED",
                default_rule_id="GEN-DEF-PCLASSYEARSWITCH-0",
                feature_condition="PClassOption!=1",
                parser_path="caller else assignment",
            )
            self._add(
                "simopt",
                "PClass=",
                None,
                "INTEGER",
                "ModelConfiguration",
                "p_class.class",
                None,
                None,
                presence="INACTIVE_NULL",
                feature_condition="PClassOption!=1",
                parser_path="not read",
            )

        c = self._find(">simtim:")
        ln1, line1 = c.next()
        start_token, _ = self._parse_date_record(line1, ln1)
        ln2, line2 = c.next()
        end_token, _ = self._parse_date_record(line2, ln2)
        self._add(
            "simtim",
            "StartDateRecord",
            start_token,
            "DATE",
            "SimulationWindow",
            "start_date",
            ln1,
            line1,
            parser_path="raw A256 fixed-position date record",
        )
        self._add(
            "simtim",
            "EndDateRecord",
            end_token,
            "DATE",
            "SimulationWindow",
            "end_date",
            ln2,
            line2,
            parser_path="raw A256 fixed-position date record",
        )
        ln, hydro_year, lexical, presence = self._read_op_default_on_mismatch(
            c, "HydroYearSwitch=", 0, "GEN-DEF-HYDROYRSWITCH-0"
        )
        self._add(
            "simtim",
            "HydroYearSwitch=",
            hydro_year,
            "INTEGER",
            "ModelConfiguration",
            "hydrology.year_switch",
            ln,
            lexical,
            presence=presence,
            default_rule_id=(
                None if presence == "EXPLICIT" else "GEN-DEF-HYDROYRSWITCH-0"
            ),
            parser_path=(
                "ReadOp + caller error clear/default; source checks IoptPCl "
                "instead of HydrYrSw"
            ),
        )

        c = self._find(">outscr:")
        ln, outsc, lexical = self._read_op(c, "ProgressToScreen=")
        if not 0 <= outsc <= 3:
            raise LegacyGrammarError(
                "1990/1991", f"ProgressToScreen={outsc} outside 0..3", ln
            )
        self._add(
            "outscr",
            "ProgressToScreen=",
            outsc,
            "INTEGER",
            "DiagnosticsConfiguration",
            "progress_to_screen",
            ln,
            lexical,
            parser_path="Findadr>ReadOp",
        )

        c = self._find(">outbal:")
        ln, nubase, lexical = self._read_op(c, "NumberOfPrintBal=")
        if not 0 <= nubase <= self.maba:
            raise LegacyGrammarError(
                "1990/1991",
                f"NumberOfPrintBal={nubase} outside 0..{self.maba}",
                ln,
            )
        self._add(
            "outbal",
            "NumberOfPrintBal=",
            nubase,
            "INTEGER",
            "DiagnosticsConfiguration",
            "balances.count",
            ln,
            lexical,
            parser_path="Findadr>ReadOp",
        )

        for balance_index in range(1, nubase + 1):
            ln, line = c.next()
            eq = line.find("=")
            if eq < 0 or line[: eq + 1] != "PrintBalLabel=":
                raise LegacyGrammarError(
                    "RETURN_WITHOUT_ERROR",
                    "PrintBalLabel mismatch causes Input1 RETURN without assigning Error",
                    ln,
                )
            rhs = line[eq + 1 :]
            token = rhs.split("!")[0].strip()
            if len(token) >= 2 and token[0] in "'\"" and token[-1] == token[0]:
                token = token[1:-1]
            label = token[:2]
            self._add(
                "outbal",
                "PrintBalLabel=",
                label,
                "CHARACTER(2)",
                "DiagnosticsConfiguration",
                f"balances[{balance_index}].label",
                ln,
                line,
                repeat_index=balance_index,
                parser_path="manual A256 positional read",
            )

            balance: dict[str, int] = {}
            for key, path in [
                ("PrintBalWater=", "water"),
                ("PrintBalOrgMat=", "organic_matter"),
                ("PrintBalNitrogen=", "nitrogen"),
                ("PrintBalPhosphor=", "phosphorus"),
                ("PrintBalSulphate=", "sulphate"),
                ("PrintBalTopLay=", "top_layer"),
                ("PrintBalBotLay=", "bottom_layer"),
                ("PrintBalNoUpd=", "update_count"),
            ]:
                ln, field_value, lexical = self._read_op(c, key)
                balance[path] = field_value
                self._add(
                    "outbal",
                    key,
                    field_value,
                    "INTEGER",
                    "DiagnosticsConfiguration",
                    f"balances[{balance_index}].{path}",
                    ln,
                    lexical,
                    repeat_index=balance_index,
                    parser_path="ReadOp",
                )

            if (
                balance["top_layer"] < 0
                or balance["top_layer"] > balance["bottom_layer"]
            ):
                raise LegacyGrammarError(
                    "1990/1991", "PrintBalTopLay outside source check"
                )
            if (
                balance["bottom_layer"] < balance["top_layer"]
                or balance["bottom_layer"] > self.manl
            ):
                raise LegacyGrammarError(
                    "1990/1991", "PrintBalBotLay outside source check"
                )
            if balance["update_count"] > 100:
                raise LegacyGrammarError("1991", "PrintBalNoUpd > 100")
            if balance["update_count"] < -1:
                # Checkint accepts these because Low=999 is its no-lower-bound
                # sentinel. Negative repeat cardinality other than -1 is not given a
                # normalized meaning by IO02.
                raise LegacyGrammarError(
                    "UNADMITTED_NEGATIVE_CARDINALITY",
                    "source range check admits negative count other than -1; repeat semantics not admitted",
                )

            if balance["update_count"] not in (-1, 0):
                ln, dates, _tokens, lexical = self._read_reals(
                    c, "PrintBalUpdDate=", balance["update_count"]
                )
                if any(not 1.0 <= value <= 365.0 for value in dates):
                    raise LegacyGrammarError(
                        "1992/1993", "PrintBalUpdDate outside 1..365", ln
                    )
                # Input1 sorts the array in place. The supplied Intel Visual
                # Fortran project uses RealKIND=realKIND8, so default REAL is
                # binary64 in the admitted executable build context.
                dates_sorted = sorted(dates)
                self._add(
                    "outbal",
                    "PrintBalUpdDate=",
                    dates_sorted,
                    "REAL(8)_ARRAY",
                    "DiagnosticsConfiguration",
                    f"balances[{balance_index}].update_dates",
                    ln,
                    lexical,
                    repeat_index=balance_index,
                    feature_condition="PrintBalNoUpd not in {-1,0}",
                    parser_path="Readvals>sort>Checkrea",
                )
            else:
                self._add(
                    "outbal",
                    "PrintBalUpdDate=",
                    None,
                    "REAL(8)_ARRAY",
                    "DiagnosticsConfiguration",
                    f"balances[{balance_index}].update_dates",
                    None,
                    None,
                    presence="INACTIVE_NULL",
                    repeat_index=balance_index,
                    feature_condition="PrintBalNoUpd in {-1,0}",
                    parser_path="not read",
                )

        c = self._find(">outsel:")
        ln, selected_count, lexical = self._read_op(c, "SelectedComp=")
        if not 0 <= selected_count <= self.manl:
            raise LegacyGrammarError(
                "1990/1991",
                f"SelectedComp={selected_count} outside 0..{self.manl}",
                ln,
            )
        self._add(
            "outsel",
            "SelectedComp=",
            selected_count,
            "INTEGER",
            "DiagnosticsConfiguration",
            "selected_compartments.count",
            ln,
            lexical,
            parser_path="Findadr>ReadOp",
        )
        if selected_count >= 1:
            ln, compartments, lexical = self._read_ints(
                c, "CompartmentNo=", selected_count
            )
            if any(not 0 <= value <= self.manl for value in compartments):
                raise LegacyGrammarError(
                    "1990/1991", "CompartmentNo outside source check", ln
                )
            self._add(
                "outsel",
                "CompartmentNo=",
                compartments,
                "INTEGER_ARRAY",
                "DiagnosticsConfiguration",
                "selected_compartments.indices",
                ln,
                lexical,
                feature_condition="SelectedComp>=1",
                parser_path="Readints",
            )
        else:
            self._add(
                "outsel",
                "CompartmentNo=",
                None,
                "INTEGER_ARRAY",
                "DiagnosticsConfiguration",
                "selected_compartments.indices",
                None,
                None,
                presence="INACTIVE_NULL",
                feature_condition="SelectedComp<1",
                parser_path="not read",
            )

        for group, fields in OUTSEL_GROUPS:
            ln_sep, separator = c.next()
            self.meta["consumed_separators"].append(
                {"group": group, "line": ln_sep, "lexical_form": separator}
            )
            for key, _index in fields:
                ln, jout, outln, line, presence = self._read_ts(c, key)
                value: dict[str, Any] = {
                    "file_output": jout,
                    "selected_compartment_output": outln,
                }
                if group == "WholeProfile" and key in WHOLE_PROFILE_IDUM_KEYS:
                    value = {
                        "file_output": jout,
                        "selected_compartment_output": "NOT_APPLICABLE_DISCARDED_TO_IDUM",
                    }
                if key in OPTIONAL_READTS_DEFAULT_KEYS and presence.startswith(
                    "DEFAULTED"
                ):
                    value = {
                        "file_output": 0,
                        "selected_compartment_output": "LEGACY_UNDEFINED_IF_OMITTED",
                    }
                self._add(
                    "outsel",
                    key,
                    value,
                    "OUTPUT_SELECTOR",
                    "DiagnosticsConfiguration",
                    f"outputs.{key.rstrip('=')}",
                    ln,
                    line,
                    presence=presence,
                    default_rule_id=(
                        "GEN-DEF-OPTIONAL-OUTPUT-0"
                        if presence.startswith("DEFAULTED")
                        else None
                    ),
                    parser_path="ReadTs",
                )

        c = self._find(">outtot:")
        ln, each_timestep, lexical = self._read_op(c, "IntMedOutputTS=")
        if not 0 <= each_timestep <= 1:
            raise LegacyGrammarError(
                "1990/1991", "IntMedOutputTS outside 0..1", ln
            )
        self._add(
            "outtot",
            "IntMedOutputTS=",
            each_timestep,
            "INTEGER",
            "DiagnosticsConfiguration",
            "intermediate.each_timestep",
            ln,
            lexical,
            parser_path="Findadr>ReadOp",
        )
        if each_timestep == 0:
            ln, count, lexical = self._read_op(c, "NumIntMedOutputTS=")
            if not 0 <= count <= 52:
                raise LegacyGrammarError(
                    "1990/1991", "NumIntMedOutputTS outside 0..52", ln
                )
            self._add(
                "outtot",
                "NumIntMedOutputTS=",
                count,
                "INTEGER",
                "DiagnosticsConfiguration",
                "intermediate.count",
                ln,
                lexical,
                feature_condition="IntMedOutputTS=0",
                parser_path="ReadOp",
            )
            ln, intmed_values, lexical = self._read_ints(
                c, "IntMedOutFromStart=", count
            )
            if any(not 0 <= value <= 9999 for value in intmed_values):
                raise LegacyGrammarError(
                    "1990/1991", "IntMedOutFromStart outside 0..9999", ln
                )
            self._add(
                "outtot",
                "IntMedOutFromStart=",
                intmed_values,
                "INTEGER_ARRAY",
                "DiagnosticsConfiguration",
                "intermediate.from_start",
                ln,
                lexical,
                feature_condition="IntMedOutputTS=0",
                parser_path="Readints",
            )
        else:
            self._add(
                "outtot",
                "NumIntMedOutputTS=",
                None,
                "INTEGER",
                "DiagnosticsConfiguration",
                "intermediate.count",
                None,
                None,
                presence="INACTIVE_NULL",
                feature_condition="IntMedOutputTS=1",
                parser_path="not read",
            )
            self._add(
                "outtot",
                "IntMedOutFromStart=",
                None,
                "INTEGER_ARRAY",
                "DiagnosticsConfiguration",
                "intermediate.from_start",
                None,
                None,
                presence="INACTIVE_NULL",
                feature_condition="IntMedOutputTS=1",
                parser_path="not read",
            )

        ghg_option = values["GreenHouseGasOption="]
        if ghg_option >= 1:
            self._find(">outGHG:")
            self.meta["routes"].append(
                {
                    "condition": "GreenHouseGasOption>=1",
                    "route": "GHG_SCHEMA_LINEAGE_UNRESOLVED",
                    "status": "NOT_ADMITTED",
                }
            )
        else:
            self.meta["routes"].append(
                {
                    "condition": "GreenHouseGasOption<1",
                    "route": "outGHG not read",
                    "status": "INACTIVE",
                }
            )

        return {
            "schema": "General41NormalizedRepresentation/v1",
            "records": [record.to_dict() for record in self.records],
            "meta": self.meta,
            "projection": {
                "model_configuration": {
                    record.target_path: record.value
                    for record in self.records
                    if record.target_object == "ModelConfiguration"
                },
                "simulation_window": {
                    record.target_path: record.value
                    for record in self.records
                    if record.target_object == "SimulationWindow"
                },
                "diagnostics_configuration": {
                    record.target_path: record.value
                    for record in self.records
                    if record.target_object == "DiagnosticsConfiguration"
                },
            },
        }
