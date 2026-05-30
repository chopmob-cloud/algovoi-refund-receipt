> **AlgoVoi is available for acquisition** — [docs.algovoi.co.uk/acquisition](https://docs.algovoi.co.uk/acquisition)

---

# algovoi-refund-receipt

[![PyPI](https://img.shields.io/pypi/v/algovoi-refund-receipt?label=PyPI)](https://pypi.org/project/algovoi-refund-receipt/)
[![npm](https://img.shields.io/npm/v/@algovoi/refund-receipt?label=npm)](https://www.npmjs.com/package/@algovoi/refund-receipt)
[![Apache 2.0](https://img.shields.io/badge/license-Apache--2.0-green)](./LICENSE)
[![IETF I-D](https://img.shields.io/badge/companion%20IETF%20I--D-draft--hopley--x402--refund--receipt--00-blue)](https://datatracker.ietf.org/doc/draft-hopley-x402-refund-receipt/)

AlgoVoi-authored reference implementation for the refund receipt format
specified in IETF Internet-Draft
[`draft-hopley-x402-refund-receipt`](https://datatracker.ietf.org/doc/draft-hopley-x402-refund-receipt/)
(Independent Submission, Informational; AlgoVoi-authored).

Companion to the compliance receipt format
[`draft-hopley-x402-compliance-receipt`](https://datatracker.ietf.org/doc/draft-hopley-x402-compliance-receipt/).
Where the compliance receipt records an admission-time screening
decision, the refund receipt records a post-settlement
reversal-of-funds event with the same canonicalisation discipline
(JCS RFC 8785, `urn:x402:canonicalisation:jcs-rfc8785-v1`) and the
same audit-chain semantics.

Python and TypeScript reference implementations, byte-for-byte
parity, Apache 2.0.

## Use cases

- Build refund-event records that compose with compliance receipts via
  the `original_payment_ref` linkage.
- Verify that a refund receipt produced by a counterparty canonicalises
  to the expected `content_hash` for retention-period audit.
- Validate refund receipts against the eight-implementation
  cross-validation matrix at the canonicalisation layer (Python,
  TypeScript, Go, Rust, Java, PHP, .NET, Ruby).

## Packages

| Language | Package | Install |
|---|---|---|
| Python | [`algovoi-refund-receipt`](https://pypi.org/project/algovoi-refund-receipt/) | `pip install algovoi-refund-receipt` |
| TypeScript | [`@algovoi/refund-receipt`](https://www.npmjs.com/package/@algovoi/refund-receipt) | `npm install @algovoi/refund-receipt` |

Both packages depend on `algovoi-substrate` (PyPI) and
`@algovoi/substrate` (npm) respectively for the canonicalisation
primitive.

Both packages are byte-deterministic on identical inputs and tested
against the same `refund_receipt_v1` conformance vector set published
at
[`chopmob-cloud/algovoi-jcs-conformance-vectors`](https://github.com/chopmob-cloud/algovoi-jcs-conformance-vectors/tree/main/vectors/refund_receipt_v1).

## Quick start

### Python

```python
from algovoi_refund_receipt import build_refund_receipt
from algovoi_substrate import sha256_jcs

receipt = build_refund_receipt(
    original_payment_ref="sha256:0dd5d0b76c9b9281fdeb2509ad38ab132b16a17385ca01d976ff9e6e12563a0f",
    refund_result="FULL",
    refund_timestamp_ms=1716494400000,
    refund_provider_did="did:web:api.algovoi.co.uk",
    refund_amount={"amount_minor": "100000", "asset_id": "USDC.6"},
    jurisdiction_flags=["UK", "EU"],
)
content_hash = sha256_jcs(dict(receipt))
print(content_hash)
# 7fdd283c3a8abb14d893999d1d16e2f7697ad0539250f2e0fc3e31ce89943dcb
```

### TypeScript

```typescript
import { buildRefundReceipt } from "@algovoi/refund-receipt";
import { sha256Jcs } from "@algovoi/substrate";

const receipt = buildRefundReceipt({
  original_payment_ref:
    "sha256:0dd5d0b76c9b9281fdeb2509ad38ab132b16a17385ca01d976ff9e6e12563a0f",
  refund_result: "FULL",
  refund_timestamp_ms: 1716494400000,
  refund_provider_did: "did:web:api.algovoi.co.uk",
  refund_amount: { amount_minor: "100000", asset_id: "USDC.6" },
  jurisdiction_flags: ["UK", "EU"],
});
console.log(sha256Jcs(receipt));
// 7fdd283c3a8abb14d893999d1d16e2f7697ad0539250f2e0fc3e31ce89943dcb
```

## Receipt format

A refund receipt is a seven-field JSON object canonicalised under RFC
8785 (JCS). Field names are sorted lexicographically by JCS during
canonicalisation.

| Field | Type | Description |
|---|---|---|
| `canon_version` | string | In-band canonicalisation rule pin. Fixed `jcs-rfc8785-v1` for this version. |
| `jurisdiction_flags` | ordered array of string | Applicable regulatory frameworks. Array order is significant under RFC 8785 §3.2.3. |
| `original_payment_ref` | string | Content-addressed reference to the original payment (`sha256:<hex>`). |
| `refund_amount` | object | `{amount_minor: string, asset_id: string}` -- refunded value in the asset's minor unit. |
| `refund_provider_did` | string | DID URI identifying the refund-issuing entity. |
| `refund_result` | string (closed enum) | `FULL` / `PARTIAL` / `REJECTED`. Closed three-element enumeration; load-bearing under consumer-rights and PSD2 statutes. |
| `refund_timestamp_ms` | integer | Epoch milliseconds. **Substrate Rule 2**: MUST be integer; RFC 3339 string forms rejected. |

See [`draft-hopley-x402-refund-receipt`](https://datatracker.ietf.org/doc/draft-hopley-x402-refund-receipt/)
Section 3 for the full specification.

## Closed enumeration: `refund_result`

| Value | Semantic | Regulatory significance |
|---|---|---|
| `FULL` | Entire original amount returned. | Closes consumer's right to further remedy under UK Consumer Rights Act 2015 and EU Consumer Rights Directive 2011/83/EU Article 9. |
| `PARTIAL` | Less than the original amount returned. | Does not close consumer-rights remedies; further refund obligations may remain. |
| `REJECTED` | Refund request processed and denied. No funds moved. | Required under PSD2 (Directive 2015/2366) Article 89 for unauthorised-payment refund disputes; documented denial obligation. |

## Composition with compliance receipts

When refunding a payment admitted under an
`algovoi-substrate` compliance receipt, set `original_payment_ref` to
the `content_hash` of the compliance receipt. A verifier walking the
audit chain can then confirm the full payment lifecycle:

```
compliance_receipt (ALLOW) -> settlement -> refund_receipt (FULL)
```

Audit chain row shape is identical between the compliance receipt and
refund receipt formats; both anchor to the same `canon_version` pin.

## Conformance vectors

The vector set at
[`vectors/refund_receipt_v1/`](https://github.com/chopmob-cloud/algovoi-jcs-conformance-vectors/tree/main/vectors/refund_receipt_v1)
pins eight byte-level reference receipts + five pair invariants +
three chain invariants.

Any implementation claiming conformance with
`draft-hopley-x402-refund-receipt` MUST reproduce all eight
`expected_content_hash` values verbatim.

## Companion IETF Internet-Draft

This library implements the format specified in
[`draft-hopley-x402-refund-receipt`](https://datatracker.ietf.org/doc/draft-hopley-x402-refund-receipt/)
(Independent Submission, Informational). The draft pins
`urn:x402:canonicalisation:jcs-rfc8785-v1` (same canonicalisation
discipline as the compliance receipt I-D) and specifies the seven-field
receipt format, the audit-chain composition, and the year-N
auditability properties.

## Related AlgoVoi packages

| Package | Purpose |
|---|---|
| [`algovoi-substrate`](https://pypi.org/project/algovoi-substrate/) / [`@algovoi/substrate`](https://www.npmjs.com/package/@algovoi/substrate) | JCS RFC 8785 canonicalisation, `action_ref`, transactional lifecycle, compliance receipt builder |
| [`algovoi-audit-verifier`](https://pypi.org/project/algovoi-audit-verifier/) / [`@algovoi/audit-verifier`](https://www.npmjs.com/package/@algovoi/audit-verifier) | Selective-disclosure audit bundle verifier |
| [`algovoi-rfc9421-verifier`](https://pypi.org/project/algovoi-rfc9421-verifier/) / [`@algovoi/rfc9421-verifier`](https://www.npmjs.com/package/@algovoi/rfc9421-verifier) | RFC 9421 + RFC 9530 HTTP message signature verifier |
| **`algovoi-refund-receipt`** / `@algovoi/refund-receipt` | **This package.** Refund receipt format reference implementation |

## Conformance to the canonicalisation discipline

This package emits refund receipts pinned to `canon_version: jcs-rfc8785-v1` on every emitted receipt. The pin is in-band; downstream verifiers (including [`algovoi-audit-verifier`](https://pypi.org/project/algovoi-audit-verifier/) and any conformant third-party verifier) read the pin to select the canonicalisation rule applied at emission.

The pin is the load-bearing primitive for the [Substrate Adopters Registry](https://docs.algovoi.co.uk/adopters): adopters anchoring to this discipline pin the same `canon_version` value in their own publicly-citable artefacts. AlgoVoi maintains the registry as a neutral observer; this package itself is recorded there as the AlgoVoi reference implementation.

## Substrate adopters

AlgoVoi is recorded in the [Substrate Adopters Registry](https://docs.algovoi.co.uk/adopters) as the substrate author (v1 and v2). Parties anchoring their own services or specifications to `canon_version: jcs-rfc8785-v1` are recorded in the registry via the [submission process](https://docs.algovoi.co.uk/adopters#how-to-submit-an-adoption-entry). AlgoVoi validates submissions against the artefact's canonical bytes and adds qualifying entries.

## Tests

```bash
# Python (14 tests)
pip install -e python/[dev]
python -m pytest python/tests/ -v

# TypeScript (15 tests)
cd typescript && npm install && npm test
```

## Licence

Apache 2.0. See [`LICENSE`](./LICENSE).

## Author

AlgoVoi (Christopher Hopley, GitHub [`chopmob-cloud`](https://github.com/chopmob-cloud)).
