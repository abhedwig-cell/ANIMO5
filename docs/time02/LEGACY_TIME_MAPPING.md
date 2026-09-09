# ANIMO-TIME02 legacy time mapping

Status: `SOURCE_BOUND_MAPPING_WITH_EXPLICIT_UNQUALIFIED_EDGES`.

## 1. Purpose

This document maps revision-53 time-bearing source values to the TIME02 candidate coordinate. It deliberately does not collapse similarly named legacy values into one semantic object.

## 2. Mapping table

| Legacy value / input | Source role | Candidate mapping | Qualification note |
| --- | --- | --- | --- |
| `StartDate` (4.1) | requested simulation start date | civil date at 00:00 -> exact coordinate | source-bound |
| `EndDate` (4.1) | requested final calendar date | civil date at 24:00 -> next midnight | source-bound |
| `YRMIAN,TIMIAN` (4.0) | start year plus real day number | legacy calendar adapter -> exact coordinate | 4.0 compatibility path; numeric parse/build details remain adapter provenance |
| `YRMAAN,TIMAAN` (4.0) | end year plus real day number | legacy calendar adapter, end treated with hour 24 | 4.0 compatibility path |
| `Juda` | main-loop interval-end clock after `St` advance | candidate `t1` for the source-equivalence interval being executed | role is source-bound; binary value is not canonical |
| `Juda-St` | expression used as interval start in source predicates | candidate `t0` for that interval | derive from accepted boundary identity, not by floating subtraction in new code |
| `St` | current interval duration | exact rational duration attached to interval/frame | value may originate from producer or decade rule |
| `Tito` | cumulative simulation time | diagnostic/legacy progression coordinate relative to run start | not automatically canonical absolute time |
| `Tiyr` | time relative to start of current year | derived calendar-relative value | not canonical absolute identity |
| `Judami` | legacy absolute simulation-start Julian-day value | maps to canonical start coordinate | do not preserve legacy floating JD as identity |
| `Judama` | legacy absolute simulation-end Julian-day value | maps to canonical final boundary | same |
| `Judayr` | Julian-day value for current 1 January | derived year-start coordinate | same |
| `Tinead` input | cumulative management event day number | `Judami + raw_value - 1/2 day` under legacy mapping | source conversion is explicit |
| `Tinead` absolute | next management packet event coordinate | exact event coordinate with management predicate `(t0,t1]` | reader cursor remains continuation concern |
| `Tiso`,`Tiup1`,`Tiha` from 4.1 management date rows | crop sowing/transition/harvest dates | `YYYY-MM-DD 12:00` | source calls `julianDay_date(...,12,0,0)` |
| `TIWA` / `STiwa` | hydrology producer time field | producer-specific raw frame coordinate; map explicitly to canonical frame `t1` | never equate directly to `Juda` without mode evidence |
| `SSt` | producer interval length | exact decoded producer duration, then bind to frame | `REAL(4)` payload |
| `TIMIHY`,`TIMAHY` | hydrology header period | producer calendar-envelope metadata | mapping includes legacy SWAP-version conventions |
| `HydroYearSwitch` | requested mapping between ANIMO and producer years | explicit calendar transform in adapter provenance | not a change to canonical arithmetic rules |
| external crop `YEAR MONTH DAY` | producer record date | exact civil date metadata on crop frame | exact interval relation must be adapter-qualified |
| `TIBA` / output dates | report/balance period date | diagnostic schedule coordinate | not physical accept/event rule |

## 3. Legacy Julian-day representation is not canonical identity

Revision 53 uses `julianDay_date` and `GDATE` to move between civil fields and a Julian-day `REAL`. The historical compiler project is missing. PREP01 strongly supports, but does not historically prove, eight-byte default REAL semantics.

TIME02 therefore maps the **calendar meaning** into an exact rational coordinate. It does not require equality of the new canonical rational with the exact binary bits produced by an unproven historical build.

Where bit-for-bit reproduction of a legacy numeric field is required later, the adapter must carry the selected historical build/numeric contract as separate evidence.

## 4. 4.1 general-date mapping

Revision-53 source mapping is:

```text
StartDate YYYY-MM-DD -> julianDay_date(Y,M,D,00,00,00)
EndDate   YYYY-MM-DD -> julianDay_date(Y,M,D,24,00,00)
```

TIME02 canonicalizes this without a Julian floating intermediate:

```text
start = civil_to_coordinate(Y,M,D,00:00:00)
end   = civil_to_coordinate(next_civil_day(Y,M,D),00:00:00)
```

This conversion is exact, including leap-day transitions.

## 5. Management mapping

The first and following management times are read as real cumulative day values. Revision 53 then applies `+ Judami - 0.5`.

For legacy-compatible scheduling, the adapter must preserve that transformation exactly in rational arithmetic after the raw input numeric value has been deterministically interpreted. An integer raw event value `N` therefore maps to noon on cumulative day `N` relative to a midnight simulation start.

The event-class predicate remains separate from this conversion:

- mapping determines coordinate `E`;
- management selection determines `t0 < E <= t1`.

Do not encode endpoint membership by perturbing the mapped coordinate.

## 6. Crop management dates

For 4.1 management-period rows the source constructs `Tiso`, `Tiup1` and `Tiha` at 12:00. TIME02 preserves noon. Converting these dates to midnight would be a behavioural change and is forbidden absent a separately admitted scientific/discrepancy decision.

Harvest membership then applies the independent `[t0,t1)` predicate.

## 7. Hydrology mapping

### Raw encoding

The supplied detailed hydrology files use PowerStation-compatible sequential-unformatted framing. Dynamic producer time and step fields are `REAL(4)` payload values. PREP01 already qualifies the record-format decoding as evidence/tooling, not as B2 behaviour.

TIME02 adapter requirements are:

1. decode the producer numeric field under its declared binary schema;
2. retain raw payload/content identity;
3. convert the finite numeric value to an exact rational;
4. apply the producer-mode calendar/origin transform;
5. bind resulting exact `t0`/`t1` to the interval frame;
6. reject any identity mismatch exactly.

### Testbank observation

Across all nine supplied hydrology files, decoded dynamic steps are only `1`, `8`, `9`, `10` or `11` days and decoded `TIWA` values are integral days. This does not create a one-day canonical quantum.

### Legacy version adjustments

Revision 53 contains compatibility handling such as treating a hydrology `TIMIHY` near `1` as the older SWAP day-zero convention and tolerating selected header mismatches/known producer bugs. Those are adapter compatibility dispositions. They must not become the canonical equality relation.

A future real producer adapter must name the exact rule it applies and emit the transformed canonical coordinate. Canonical frame comparison after transformation is exact.

## 8. External crop mapping

`CROP_EXT` supplies integer year/month/day per producer record. The 4.0 guide states that crop forcing time resolution follows the hydrological input (daily, weekly or decade). Therefore the date alone is insufficient to infer a universal subday boundary or event rule.

The future crop adapter must bind each crop frame to the exact same canonical interval as the hydrology/ANIMO trial using producer-specific semantics. TIME02 does not infer this relation from record position alone.

## 9. Range mapping

Observed testbank ANIMO periods:

| Case | ANIMO period | inclusive days |
| --- | --- | ---: |
| CranMais | 1974-01-01 to 1982-12-31 | 3287 |
| RuurloGrass | 1980-01-01 to 1985-04-30 | 1947 |
| GrassPeat | 1986-01-01 to 2000-12-31 | 5479 |
| CranGrass | 1992-01-01 to 1999-12-31 | 2922 |
| STONE_akk_0006 | 2001-01-01 to 2015-12-31 | 5478 |
| Puitmijn_Cranendonck_60 | 2002-01-01 to 2013-12-31 | 4383 |
| GHGMais | 2010-01-01 to 2019-12-31 | 3652 |
| Zuiderzeeland | 2015-01-01 to 2017-12-31 | 1096 |
| LWKM_gras_1040 | 2021-01-01 to 2045-12-31 | 9131 |

The source structural range remains at most 60 calendar-year slots because `Many=60`. TIME02 requires a new loader to fail closed if that legacy-compatibility limit is exceeded rather than reproduce an unchecked array-overrun risk.

## 10. Round-trip classes

TIME02 distinguishes three round-trip promises:

1. **canonical round trip:** coordinate -> canonical serialization -> coordinate is exact and mandatory;
2. **civil round trip:** valid admitted civil date/time -> coordinate -> civil date/time is exact and mandatory;
3. **legacy producer byte round trip:** optional, requires retention of original bytes/lexeme plus producer schema/build provenance. It is not guaranteed by the coordinate alone.

This distinction prevents a mathematically exact canonical coordinate from being mistaken for a byte-for-byte copy of an external floating record.

## 11. Unqualified edges

TIME02 explicitly leaves these open:

- exact historical default-REAL compiler semantics remain a strongly supported hypothesis rather than direct release evidence;
- arbitrary subdaily SWAP/WATBAL producer contracts are not qualified by the supplied testbank;
- exact split-run/restart historical behaviour is not B2-qualified;
- real SWAP and external-crop production adapters are not implemented;
- year 0 and years above 3000 are outside the qualified legacy-compatibility envelope;
- any scientific correction to management/harvest endpoint asymmetry requires its owning admission route.
