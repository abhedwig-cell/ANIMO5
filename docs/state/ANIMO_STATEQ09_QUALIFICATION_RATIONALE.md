# ANIMO-STATEQ09 Qualification Rationale

STATEQ09 answers a narrow but important runtime question exposed by HYDROEXEC01 and KT13: where do the next interval's beginning values for ponding, interception, snow and layer moisture fraction come from?

Frozen revision-53 source gives a direct answer. Before reading and resolving the next hydrology step, `Animo.for` calls `Init`, whose documented purpose is to initialize the current timestep from the previous timestep. In the current detailed SWAP route, the endpoint values are copied exactly into `Pn`, `Sic`, `Snla` and `Mofro(1:Nl)`.

That is state-transfer semantics, not a new physical process.

The workunit intentionally leaves `Runinu` out. `Runinu` has different source behavior and is already handled by STATEQ08 as execution continuation.

Positive qualification would establish a typed, source-derived endpoint-to-origin continuation bundle for detailed hydrology. It would not by itself admit that bundle to the canonical state registry or checkpoint format.
