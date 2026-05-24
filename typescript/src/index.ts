/**
 * @algovoi/refund-receipt
 *
 * AlgoVoi refund receipt format reference implementation. Companion
 * to @algovoi/substrate compliance receipt. Post-settlement counterpart
 * that records reversal-of-funds events under the same JCS RFC 8785
 * canonicalisation pin (urn:x402:canonicalisation:jcs-rfc8785-v1).
 *
 * Specified in IETF Internet-Draft draft-hopley-x402-refund-receipt-00
 * (Independent Submission, Informational; AlgoVoi-authored).
 *
 * Licensed under Apache 2.0.
 */

export {
  REFUND_RESULTS,
  type RefundResult,
  RefundReceiptError,
  type RefundReceipt,
  type RefundAmount,
  type BuildRefundReceiptInput,
  buildRefundReceipt,
} from './refund-receipt.js';
