# Documentation Standards

This directory defines the editorial and structural standards for the SRE Engineering Handbook.

The goal is to keep each module consistent, practical and useful during real SRE work.

---

## Content Types

- [Concept Template](concept-template.md): conceptual explanation and SRE reasoning.
- [Reference Template](reference-template.md): command syntax, examples and interpretation.
- [Lab Template](lab-template.md): hands-on practice in a safe environment.
- [Troubleshooting Template](troubleshooting-template.md): structured investigation flow.
- [Runbook Template](runbook-template.md): operational procedure, mitigation, validation and escalation.
- [Cheatsheet Template](cheatsheet-template.md): compact command reference.
- [Tutorial Template](tutorial-template.md): step-by-step learning guide.

---

## Repository Standards

- [Folder Structure](folder-structure.md)
- [Naming Convention](naming-convention.md)
- [Markdown Style](markdown-style.md)
- [Writing Style](writing-style.md)
- [Diagram Style](diagram-style.md)
- [GitHub Workflow](github-workflow.md)
- [RAG Guidelines](rag-guidelines.md)

---

## SRE Review Criteria

Before marking a module as complete, validate:

- Links are navigable from the module README.
- Commands distinguish read-only investigation from mitigation.
- Destructive commands include a safer dry-run or validation step.
- Runbooks include prerequisites, diagnosis, mitigation, validation, rollback, escalation and post-incident actions.
- Labs can be executed safely outside production.
- Related documents are linked using relative Markdown links.
