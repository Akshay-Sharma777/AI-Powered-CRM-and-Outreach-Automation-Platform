# Prompt Version Changelog

### Version 1.0.0 (`email_draft_v1.md`)
- Initial release of the verified-facts outreach drafting prompt.
- Enforces strict factual grounding: every assertion in `body` must map to an explicit `fact_id`.
- Rejects any external or hallucinated claims regarding compensation, relationships, or experience requirements.
- Outputs structured JSON conforming to `contracts/ai-schemas/draft_output.json`.
