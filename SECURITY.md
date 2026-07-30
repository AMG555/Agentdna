# Security Policy

AgentDNA handles sensitive local activity metadata. Security reports are welcome and should be handled responsibly.

## Report a vulnerability

Do not open a public issue for an undisclosed vulnerability. Contact the repository maintainers privately with:

- Affected component
- Reproduction steps
- Impact
- Suggested mitigation
- Whether user data or credentials could be exposed

Do not include real personal activity data, API keys, passwords, or private documents in a report.

## Security expectations

- The local API should bind to loopback.
- Monitoring must remain disabled until explicit consent.
- API keys must never enter the frontend bundle or logs.
- Cloud model use must be opt-in.
- Sensitive metadata must be redacted before indexing or transmission.
- Automation tools must be allowlisted and confirmation-gated.
- Data deletion must remove activity, embeddings, feedback, and audit records within the declared scope.
