def build_summary_prompt(project_json, rule_based_summary):
    return f"""
You are a technical writing assistant for developers.

Your task:
Rewrite the provided project summary into a clear, concise, professional paragraph.
Do NOT add new information.
Do NOT invent features or outcomes.
Do NOT change technical facts.
Do NOT mention AI or automation.

Tone guidelines:
- Clear
- Neutral
- Professional
- Suitable for a portfolio or recruiter review

- Avoid abstract phrases such as "reflects an emphasis on", "showcases", or "highlights".
- Prefer simple, direct sentences written by a developer.


Project context (structured data):
{project_json}

Rule-based summary (ground truth):
{rule_based_summary}

Output requirements:
- 1-2 short paragraphs
- No bullet points
- No emojis
- No marketing language
- Focus on clarity and technical accuracy

Return ONLY the rewritten summary text.
"""
