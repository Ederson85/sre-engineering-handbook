# Engineering Case Studies

This section contains in-depth engineering case studies based on real production investigations.

Unlike the shorter scenarios available in the `real-world` directories, these case studies document complex incidents involving multiple technology layers, long-running investigations, observability, architectural decisions and collaboration between engineering teams.

---

## Purpose

The goal of this section is to demonstrate how Site Reliability Engineers:

- Investigate intermittent failures
- Correlate signals across multiple system layers
- Separate symptoms from root causes
- Build observability for complex environments
- Coordinate investigations with internal teams and technology vendors
- Design and validate reliability improvements
- Convert incident knowledge into reusable engineering practices

---

## Confidentiality and Anonymization

All case studies are anonymized.

Sensitive operational information is intentionally removed or generalized, including:

- Organization names
- People and team names
- Hostnames and IP addresses
- Cluster and environment identifiers
- Exact infrastructure sizing
- Internal URLs and credentials
- Ticket and support-case identifiers
- Customer and traffic volumes
- Proprietary logs and screenshots

Technology names may be referenced only when they provide relevant technical context.

The published content represents an engineering reconstruction of the investigation and is not an official statement from any organization or technology vendor.

---

## Available Case Studies

<!-- AUTO-INDEX:START -->

- [Case Study 01 — Intermittent Cassandra Storage Latency in a Cloud Environment](case-01-cloud-cassandra-storage-latency/README.md)

<!-- AUTO-INDEX:END -->
---

## Case Study Structure

Each case study may include:

- Executive Summary
- Architecture
- Timeline
- Investigation
- Observability
- Root Cause Analysis
- Remediation
- Lessons Learned
- Architecture Diagrams

---

## Review Principles

Before publishing a case study, confirm that:

- All confidential information has been removed.
- Logs and metrics have been rewritten or generalized.
- Hypotheses are clearly separated from confirmed evidence.
- Vendor statements are paraphrased rather than reproduced.
- Business impact is described without exposing internal volumes.
- The investigation reflects engineering evidence rather than assumptions.