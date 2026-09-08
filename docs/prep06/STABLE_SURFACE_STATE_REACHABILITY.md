# ANIMO-PREP06 — Stable-DOM layer-0 reachability

Status: `PARSER_REPRESENTABLE_DYNAMICALLY_DORMANT_IN_REVISION53`.

## Source question

`Outbal_calc.for` contains three explicit comments in the ponding-runoff ledger:

```text
AvcoStdiorma(0) not yet included
AvcoStdiorni(0) not yet included
AvcoStdiorpo(0) not yet included
```

Before treating those comments as active mass-balance defects, PREP06 traced the revision-53 reachability of the corresponding layer-0 stable dissolved-organic states.

## Parser and restart surface

`input1.for` reads `CoStdiorma`, `CoStdiorni` and, when P is active, `CoStdiorpo` for `Ln=0,Nl`. `Output_Init.for` likewise writes the stable result arrays over `Ln=0,Nl`.

Thus the generic parser/restart arrays syntactically expose layer 0.

## Dynamic update surface

The actual stable-DOM process solve in `resp_miner.for` iterates through the `SqNu` sequence but explicitly skips `Ln==0` via `goto 1000`. All stable-DOM production, decay, transport approximation and result-state assignments occur only for soil layers.

`Init.for` initializes `RsCoStdiorma/ni/po(0:Nl)` to zero at the first timestep and on later steps copies those result arrays back into `CoStdiorma/ni/po(0:Nl)`.

The only explicit assignments to layer-0 stable states outside this are zeroing during the Addit ploughing/top-reservoir reset path. No source routine was found that dynamically produces or transports a nonzero stable DOM/DON/DOP state in layer 0.

## Supplied testbank

The supplied `>sdomin:` input rows use zero for layer 0. Therefore no supplied reference case activates stable dissolved-organic mass in the ponding layer.

## Controlled parser-activation check

STONE was selected because its first annual water-balance record has nonzero beginning ponding storage (`~1.2174 mm`). A temporary testcase copy set only the layer-0 stable concentrations to nonzero values:

```text
CoStdiorma(0) = 1.0 kg/m3
CoStdiorni(0) = 0.1 kg/m3
CoStdiorpo(0) = 0.05 kg/m3
```

The unchanged deterministic GNU diagnostic executable completed successfully. The annual OM/N/P balance records were byte/numerically unchanged from the original STONE diagnostic execution. This confirms that parser acceptance of the values does not make them an operational revision-53 layer-0 state in the exercised route.

## Classification

The missing stable-component ponding-runoff terms are **not promoted to active mass-balance defects** by PREP06.

Current classification:

`PARSER_REPRESENTABLE_DYNAMICALLY_DORMANT_STATE_SURFACE`

This remains architecturally relevant. A future ANIMO5 model must not expose a state index in input/restart contracts unless its ownership and evolution semantics are defined. If stable DOM is ever admitted in surface water, its runoff ledger and output routes must include C, N and P components consistently.

The nearby `Outsel` expressions for `Rudon` and `Rudop` also use `AvcoStdiorma(0)` instead of the N/P-specific stable concentrations. Because the current revision-53 stable layer-0 state is dynamically dormant, PREP06 records this as a latent output-path defect, not an active supplied-case discrepancy.

Production migration remains `NOT_ADMITTED`.
