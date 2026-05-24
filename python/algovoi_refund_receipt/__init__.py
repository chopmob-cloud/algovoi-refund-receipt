"""
algovoi-refund-receipt -- AlgoVoi refund receipt format reference implementation.

Companion to algovoi-substrate compliance receipt. Post-settlement counterpart
that records reversal-of-funds events under the same JCS RFC 8785
canonicalisation pin (urn:x402:canonicalisation:jcs-rfc8785-v1).

Specified in IETF Internet-Draft draft-hopley-x402-refund-receipt-00
(Independent Submission, Informational; AlgoVoi-authored).

The categorical outcome (FULL / PARTIAL / REJECTED) is load-bearing for
downstream consumer-rights and PSD2 obligations: a REJECTED outcome carries
dispute-evidence obligations distinct from FULL/PARTIAL, and the receipt
format preserves the operational distinction at the canonical-bytes level
rather than collapsing it to a score or tier projection.

Composes with algovoi-substrate.compliance_receipt via the
original_payment_ref linkage so a verifier can walk the full payment
lifecycle (admission decision -> settlement -> refund event) under one
canonicalisation pin.

Licensed under Apache 2.0.
"""

from algovoi_refund_receipt.refund_receipt import (
    REFUND_RESULTS,
    RefundAmount,
    RefundReceipt,
    RefundReceiptError,
    build_refund_receipt,
)

__all__ = [
    "REFUND_RESULTS",
    "RefundAmount",
    "RefundReceipt",
    "RefundReceiptError",
    "build_refund_receipt",
]

__version__ = "0.1.0"
