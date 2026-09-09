# ANIMO-TIME02 concrete time representation

Status: `QUALIFIED_CONCRETE_TIME_REPRESENTATION_CANDIDATE_CANONICAL_TIME_ADMISSION_PENDING`.

`canonical_time_admitted=false`.

## 1. Decision

TIME02 selects a **normalized exact rational civil-day coordinate** as the candidate semantic representation for ANIMO5 time. Floating point is not the canonical time identity. A fixed integer tick is not selected because the frozen revision-53 interfaces do not establish one uniform minimum quantum for all legacy time-bearing values.

The candidate coordinate is:

```text
TimeCoordinate = {
  calendar_contract_id,
  day_index,
  subday_numerator,
  subday_denominator
}
```

with these invariants:

- `day_index` is the signed count of proleptic-Gregorian civil days from `0001-01-01T00:00:00`, where that date has `day_index=0`;
- `0 <= subday_numerator < subday_denominator`;
- `subday_denominator > 0`;
- `gcd(subday_numerator, subday_denominator)=1`;
- the fraction is an exact fraction of one 86,400-second civil day;
- integer fields are mathematical integers. The canonical JSON form serializes them as decimal strings so JSON implementation limits cannot change identity.

The equivalent absolute rational day is `day_index + subday_numerator/subday_denominator`.

This is a candidate semantic representation, not a production scheduler implementation.

## 2. Why this representation is selected

TIME01 requires exact total ordering, lossless serialization and comparisons without hidden tolerance. It deliberately left the storage type open. TS01 shows that revision 53 uses exact source predicates on several time-like values and that event classes have different endpoint rules.

Four representation families were assessed.

| Candidate | Finding | Disposition |
| --- | --- | --- |
| fixed-width integer ticks | attractive for comparison and serialization, but no single source-proven tick quantum covers all `REAL`/`REAL(4)` time interfaces without an additional admission restriction | not selected as canonical semantics |
| exact rational/fixed-resolution day | exact ordering, exact endpoint membership, exact import of finite binary or decimal producer values, no epsilon | **selected**, using normalized rational rather than a fixed denominator |
| floating point | legacy-compatible as an adapter input, but equality and cross-platform identity depend on numeric/build semantics; cannot define calendar/event identity without tolerance hazards | adapter-only comparison candidate, rejected as canonical identity |
| date/calendar plus subday | useful user/adapter view, but a date plus fixed-resolution subday reintroduces the unresolved quantum question | retained as a derived view of the selected rational coordinate |

The selected representation does not imply that every arbitrary sub-second input is scientifically meaningful. It only prevents the canonical identity layer from inventing a tolerance or silently collapsing two distinct imported coordinates.

## 3. Source and testbank time inventory

Evidence is from the hash-pinned ANIMO 4.1.5 revision-53 source and supplied testbank. The source archive SHA-256 is `183c20eb75b6e9f02d33b54aa96fd1537519966401b6b41b9b6b108d98445566`; the testbank SHA-256 is `44e375510150ff4e9c4f94d81a3b0872aa1c964fefd3a10571c0c2a12b98bb84`.

### Internal revision-53 values

`Animo.inc` declares `St`, `Tima`, `Timi`, `Tinead`, `Tito`, `Tiwa`, `Tiyr`, `Juda`, `Judama`, `Judami` and `Judayr` as default `REAL`. The historical Intel build contract is not directly available. PREP01 found eight-byte default REAL to be a strongly supported build hypothesis, not historically proven fact. TIME02 therefore does not turn the source declaration into a canonical binary-float contract.

`func_julianday.f90` accepts integer year/month/day/hour/minute/second and maps them to a Julian-day `REAL`. `gregoriandate.f90` maps a Julian-day `REAL` back to integer civil fields. `Nudayr` and `Fdateyr` implement the Gregorian divisibility rule for leap years: divisible by 4, except centuries unless divisible by 400.

The main loop uses different roles that must remain distinct:

- `Juda`: current interval end coordinate in the main legacy loop;
- `Juda-St`: source expression for the interval start in event predicates;
- `Tito`: cumulative simulation time advanced by `St`;
- `Tiyr`: time relative to the start of the current calendar year;
- `Tiwa`: hydrology-producer time value read from the external record;
- `St`: current hydrology/model interval length.

TIME02 does **not** declare these values semantically interchangeable.

### General simulation period

For ANIMO 4.1 input, `StartDate=YYYY-MM-DD` maps to 00:00 at the start date. `EndDate=YYYY-MM-DD` maps to 24:00 of that date, i.e. 00:00 of the following civil day. The effective simulation envelope is therefore bounded by exact midnights.

The ANIMO 4.0 path uses integer years plus real day numbers. The 4.0 user guide documents an end-year limit of 3000. Revision 53 still contains `Many=60`, documented in `Param.inc` as the maximum number of years, and allocates multiple arrays as `Many` or `Many*366`. The 4.1 date parser computes `Nuyr = Yrmaan - Yrmian + 1` without an equivalent explicit fail-closed `Nuyr <= Many` check. TIME02 treats this as a range-safety constraint, not permission to exceed 60 calendar-year slots.

### Management and crop dates

Revision 53 reads management `Tinead` as a real cumulative day value and converts it to the absolute legacy axis as:

```text
Tinead_absolute = Tinead_input + Judami - 0.5 day
```

Thus an integer management day number maps to noon relative to a midnight `Judami`. The 4.1 management-period date fields (`Tiso`, `Tiup1`, `Tiha`) are explicitly converted from `YYYY-MM-DD` to `julianDay_date(...,12,0,0)`, also noon.

The supplied management files predominantly use integer cumulative addition-day values. Non-integer standalone values observed at the end of several files (`9999.9` or `99999.9`) are terminal/sentinel-style values and are not evidence for a physical subday event quantum.

External crop input uses integer `YEAR MONTH DAY` records. Those records are frame/date labels. TIME02 does not assign a universal event endpoint rule to them.

### Hydrology

Dynamic SWAP/WATBAL time fields are read from unformatted records as `REAL(4)` values (`STiwa`, and where variable step size is present, `SSt`) and passed through `Dble_trunc`. The producer time value and the ANIMO main-loop coordinate are therefore different source objects even when they describe the same intended frame boundary.

Direct decoding of the hash-pinned PowerStation-format hydrology payloads found these supplied testbank step lengths:

- daily: `1.0 d`;
- decade-style: `8.0`, `9.0`, `10.0`, `11.0 d`.

All decoded dynamic `TIWA` values in the nine supplied hydrology files are integral day values. This is testbank B0 artifact evidence only. It does not prove a general one-day ANIMO time quantum.

The LWKM case is also evidence that raw hydrology calendar years need not equal the ANIMO simulation years: the ANIMO period is 2021-2045, the hydrology header is 1971-2020, and `HydroYearSwitch=-30` is used to rebind the requested period into the producer chronology. Raw producer year labels therefore cannot be copied into canonical interval identity without an explicit mapping contract.

## 4. Smallest required temporal resolution

Two different questions must be kept separate.

1. **Civil-calendar construction:** revision-53 calendar routines accept integer seconds. One second is therefore the finest explicit civil field represented by those routines.
2. **Canonical numeric coordinate:** no finite global tick quantum is source-proven. Legacy real-valued management and producer fields are not specified as integer-second values, and the external hydrology payload is binary `REAL(4)`.

TIME02 therefore records:

```text
smallest_explicit_civil_resolution = 1 second
canonical_fixed_tick_quantum = NONE_SELECTED
canonical_coordinate_resolution = exact imported rational value
```

A later implementation may choose a fixed tick internally only after proving that every admitted input, producer frame, event, checkpoint and calendar conversion round-trips exactly within that fixed quantum. That would be an implementation qualification, not a reinterpretation of TIME02 semantics.

## 5. Representable and qualified range

The rational coordinate itself has no practical calendar-range limit when backed by arbitrary-precision integer serialization. The **legacy-compatibility admission envelope** is intentionally narrower:

- at most 60 calendar-year slots per run because `Many=60` controls source array dimensions;
- years 1 through 3000 are the conservative qualified civil-year envelope for legacy compatibility, because ANIMO 4.0 explicitly bounded the end year at 3000 and revision 53 does not provide stronger evidence for year 0 or a wider supported range;
- dates outside that envelope are representable by the candidate type but are `OUTSIDE_TIME02_LEGACY_COMPATIBILITY_QUALIFICATION`.

The supplied testbank spans civil dates 1974 through 2045. Its longest ANIMO run is LWKM, 2021-01-01 through 2045-12-31 inclusive, 9,131 days and 25 calendar-year slots. No testbank case approaches the structural 60-year limit.

## 6. Exact comparison semantics

For two coordinates under the same `calendar_contract_id`:

1. compare `day_index` exactly;
2. if equal, compare `n1*d2` and `n2*d1` using exact integer arithmetic;
3. equality requires exact equality after normalized rational reduction.

There is no epsilon, ULP window or calendar tolerance.

Cross-calendar comparison is forbidden unless an admitted calendar conversion explicitly produces a coordinate under one shared contract.

## 7. Serialization and lossless round trip

Canonical JSON serialization is:

```json
{
  "calendar_contract_id": "ANIMO_PG_86400_NOLEAPSECONDS_V1",
  "day_index": "730119",
  "subday_numerator": "1",
  "subday_denominator": "2"
}
```

Requirements:

- integer fields are decimal strings;
- rational fraction is reduced;
- no floating field participates in identity;
- deserialize-serialize is byte-stable after canonical key ordering chosen by the host format;
- calendar-to-coordinate-to-calendar round trip is exact for valid admitted civil values;
- raw legacy adapter provenance is retained separately when reproducing an original `REAL(4)` or textual legacy record is a requirement.

A canonical coordinate is not a byte-preserving replacement for an external producer record. If exact producer-file re-emission matters, retain original producer bytes/lexeme and schema identity alongside the mapped coordinate.

## 8. Floating-point boundary

Floating values may appear only at legacy/producer adapters. An adapter must:

- identify the source numeric encoding and schema;
- decode the finite value deterministically;
- convert that value to an exact rational before event/frame identity comparison;
- preserve original bytes or lexical text where round-trip to the legacy format is promised;
- reject NaN, infinity and values outside the admitted producer contract;
- never use a floating tolerance to decide whether an event is at `t0` or `t1`.

Legacy source checks such as `abs(judami-judamihy) < 1e-7` or `abs(Timihy-1) < 1e-5` are compatibility/input-validation behaviour. They are not elevated into canonical time equality.

## 9. Qualification boundary

This workunit selects and qualifies a concrete candidate semantic representation against source structure, the supplied testbank and the already-qualified TS01/TIME01 transaction constraints. It does not supply B2 historical behaviour, a real SWAP/WOFOST adapter, a production scheduler, canonical STATE admission, canonical TIME admission, B3 correction or B4 baseline admission.
