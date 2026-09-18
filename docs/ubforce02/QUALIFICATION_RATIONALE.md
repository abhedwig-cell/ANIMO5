# ANIMO-UBFORCE02 Qualification Rationale

UBFORCE02 moves one step beyond UBFORCE01: it evaluates the exact bounded revision-53 load equations rather than only carrying already-resolved loads.

The implementation is intentionally not a parser and not a hydrology model. It accepts explicit hydrology and chemistry inputs and evaluates the pinned `UBoundconc` formulas for the detailed route `Iwa=2 AND Iopthyvs=1`.

A key fail-closed boundary is retained around `Rupr` and `Runinu`. Those quantities are outputs of the hydrology-resolution responsibility. UBFORCE02 does not derive them from raw runoff. This avoids silently recreating or repairing legacy `Hydro_detailed` semantics inside a chemistry resolver.

The resolver also leaves dry deposition outside its scope because frozen revision-53 applies dry N deposition separately before computing the wet/advective loads.

Positive qualification means only:

`REV53_TCD042_WET_ADVECTIVE_LOAD_FORMULAS_HAVE_A_TYPED_NONPRODUCTION_EXECUTABLE_REALIZATION_WITH_EXPLICIT_HYDROLOGY_AND_CHEMISTRY_OWNERSHIP`.

It does not mean the complete TCD-042 forcing path is admitted.
