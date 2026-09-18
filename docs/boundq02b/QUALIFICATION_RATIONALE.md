# ANIMO-BOUNDQ02B Qualification Rationale

BOUNDQ02 was source-faithful but not strongly immutable at the Fortran type boundary. Its frame components were public, so a downstream caller could alter otherwise valid content after construction.

This is a runtime architecture defect rather than a scientific defect.

BOUNDQ02B wraps BOUNDQ02 construction in an opaque frame whose components are private. Access is copy-out only after full validation.

The workunit also tightens provenance. A canonical lowercase SHA-256 content identity is required at construction, and the UBFORCE02 forcing identity is deterministically derived from that content identity plus the selected BOUNDARY year slot.

The workunit does not compute or certify the SHA itself. It only refuses to accept a frame without a canonical content identifier and prevents the identifier/content pair from being mutated after construction.

Positive qualification means:

`BOUNDQ02_SOURCE_FAITHFUL_INTERVAL_CHEMISTRY_CAN_BE_CARRIED_IN_AN_OPAQUE_COPY_OUT_ONLY_FRAME_WITH_CONTENT_AND_SLOT_BOUND_FORCING_IDENTITY`.

It does not mean the source-file hash has been verified by Fortran, nor does it admit canonical forcing state, restart state or production.
