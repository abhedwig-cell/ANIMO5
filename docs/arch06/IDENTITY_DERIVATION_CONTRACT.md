# ANIMO-ARCH06 identity derivation contract

Status: `CANDIDATE_ARCHITECTURE_DESIGN`.

## Canonical scalar rendering

ARCH06 deliberately permits only strings, nullable strings, booleans, integer cardinalities and registered enums. No scientific floating-point values occur in the manifest.

Canonical values are rendered as JSON scalars after normalization:

- strings: UTF-8 NFC JSON string;
- booleans: `true` or `false`;
- integers: base-10 integer with no leading zeros;
- inactive conditional value: `null`;
- enums: registered lowercase token rendered as JSON string.

## Canonical record

For one identity domain:

1. select exactly the fields whose `identity_scope` contains that identity's scope token;
2. sort selected fields by `field_id` ascending;
3. render each as `field_id=<canonical-json-scalar>\n`;
4. prepend `<domain-tag>\n`;
5. SHA-256 hash the exact UTF-8 bytes;
6. render the result as `sha256:<64 lowercase hexadecimal characters>`.

Unknown fields, missing required fields, invalid conditional combinations or unsupported enum values fail before hashing.

## Domain separation

Five candidate identities use different domain tags:

- `ANIMO5_ARCH06_FEATURE_SET_V1`;
- `ANIMO5_ARCH06_PHYSICAL_LAYOUT_V1`;
- `ANIMO5_ARCH06_EXCHANGE_BINDING_V1`;
- `ANIMO5_ARCH06_CONFIGURATION_V1`;
- `ANIMO5_ARCH06_OBSERVER_CONFIGURATION_V1`.

The same selected scalar content in two different semantic domains therefore does not produce an interchangeable identity.

## Identity meaning

### feature_set_id

Represents normalized feature topology and cardinality choices. It does not identify parameters, forcing, numerical policy or diagnostics.

### physical_layout_id

Represents state topology, ownership-sensitive allocation, geometry, exchange-shape compatibility and precision representation references. It is the candidate direct checkpoint/state-layout compatibility identity introduced by ARCH04.

### exchange_binding_id

Represents static external-owner and exchange schema bindings. Runtime producer frame identity remains an ARCH05 transaction concern.

### configuration_identity

Represents the full static physical/behavioural model configuration needed to bind a coupled trial: parameter set, geometry, feature/layout topology, exchange bindings, forcing/management bindings, qualification references and numerical-policy references. Diagnostics are excluded.

### observer_configuration_id

Represents diagnostic allocation only. It may change while all four physical/coupling identities above remain unchanged.

## What these hashes do not prove

Identity equality proves equality of normalized architecture inputs under this candidate schema. It does not prove scientific equivalence, historical equivalence, numerical equivalence or compatibility across schema versions. Cross-schema migration requires an explicit qualified migration contract.
