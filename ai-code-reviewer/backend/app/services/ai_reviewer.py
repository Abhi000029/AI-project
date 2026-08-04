"""
Core AI Code Analysis Engine (FR-2, FR-3).

Sends the PR diff to Claude with a system prompt that enforces:
- multi-dimensional analysis (bugs, security, performance, style, best practice)
- structured, line-specific findings
- severity levels
- actionable suggestions
- strict JSON output so results can be persisted and rendered deterministically
"""
import json
import time
from anthropic import Anthropic
from app.config import settings

SYSTEM_PROMPT = """You are an expert senior software engineer performing an automated pull \
request code review, equivalent in rigor to a thoughtful staff engineer.

Analyze the provided unified diff across these dimensions:
1. Bugs & logic errors
2. Security vulnerabilities (reference OWASP Top 10 / CWE where relevant)
3. Performance issues
4. Code style / anti-patterns
5. Best practice violations

Rules:
- Only comment on lines actually present in the diff (added/changed lines).
- Every finding must be specific and actionable — no vague comments like "consider improving this".
- Assign a severity: critical, high, medium, low, or info.
- Avoid redundant or nitpicky findings; do not exceed 12 findings total. Prioritize the most \
important issues first.
- If the diff introduces no meaningful issues, return an empty findings array — do not invent \
problems.
- Include a short code suggestion only when a concrete fix is clear.

Respond with ONLY valid JSON (no markdown fences, no preamble) matching exactly this schema:
{
  "summary": "2-3 sentence overall assessment",
  "score": <integer 0-100 overall code quality score for this diff>,
  "findings": [
    {
      "file": "path/to/file.py",
      "line": <int or null>,
      "severity": "critical|high|medium|low|info",
      "category": "bug|security|performance|style|best_practice",
      "message": "clear explanation of the issue and why it matters",
      "suggestion": "concrete fix or code snippet, or null"
    }
  ]
}"""


class AIReviewer:
    def __init__(self):
        self._client = Anthropic(api_key=settings.anthropic_api_key)

    def analyze_diff(self, pr_title: str, language: str, diff: str) -> dict:
        start = time.time()
        user_prompt = (
            f"Pull Request Title: {pr_title}\n"
            f"Primary Language: {language}\n\n"
            f"Diff:\n```diff\n{diff}\n```"
        )

        response = self._client.messages.create(
            model=settings.anthropic_model,
            max_tokens=4000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}],
        )

        raw_text = "".join(
            block.text for block in response.content if block.type == "text"
        ).strip()

        # Defensive parsing in case the model wraps output in fences despite instructions
        if raw_text.startswith("```"):
            raw_text = raw_text.strip("`")
            if raw_text.lower().startswith("json"):
                raw_text = raw_text[4:]

        parsed = json.loads(raw_text)
        parsed["duration_ms"] = int((time.time() - start) * 1000)
        return parsed


ai_reviewer = AIReviewer()
