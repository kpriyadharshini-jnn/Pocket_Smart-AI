import json

from typing import Any

from google import genai
from google.genai import types

from ..config import get_settings


settings = get_settings()


def get_client():

    if not settings.gemini_api_key:
        return None

    return genai.Client(
        api_key=settings.gemini_api_key
    )


def extract_json(
    text: str
):

    text = text.strip()

    if text.startswith("```"):

        lines = text.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]

        text = "\n".join(
            lines
        ).strip()

    try:

        return json.loads(text)

    except json.JSONDecodeError:

        start = text.find("{")
        end = text.rfind("}")

        if start >= 0 and end > start:

            return json.loads(
                text[start:end + 1]
            )

        raise


def generate_recommendation(
    planner_type: str,
    payload: dict[str, Any],
    catalog: list[dict[str, Any]],
    image_bytes: bytes | None = None,
    image_mime: str | None = None
):

    client = get_client()

    if client is None:

        return None, "demo"

    system_prompt = """
You are PocketSmart AI.

You are a budget-aware lifestyle planning assistant.

Return ONLY valid JSON.

Do not invent:
- live stock
- live availability
- exact current prices
- reviews
- ratings
- private APIs

Estimated prices are allowed.

Use the supplied catalog as example platform links.

Keep the estimated total within the user's budget
when practical.

If the budget is too low, explain the trade-off.

JSON structure:

{
    "title": "...",
    "summary": "...",
    "estimated_total": 0,
    "budget_remaining": 0,
    "allocations": {},
    "recommendations": [
        {
            "name": "...",
            "category": "...",
            "platform": "...",
            "estimated_price": 0,
            "quantity": 1,
            "reason": "...",
            "link": "..."
        }
    ],
    "tips": []
}
"""

    user_prompt = f"""
Planner type:

{planner_type}

User request:

{json.dumps(
    payload,
    ensure_ascii=False
)}

Example catalog:

{json.dumps(
    catalog,
    ensure_ascii=False
)}

Create a practical budget-aware plan.

Use only supplied platform links.
"""

    contents: list[Any] = [
        system_prompt + "\n" + user_prompt
    ]

    if image_bytes and image_mime:

        contents.append(
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=image_mime
            )
        )

        contents.append(
            """
Analyze only visible outfit color and
style characteristics. Do not identify the person.
"""
        )

    try:

        response = client.models.generate_content(

            model=settings.gemini_model,

            contents=contents,

            config=types.GenerateContentConfig(

                temperature=0.4,

                max_output_tokens=3000,

                response_mime_type="application/json"
            )
        )

        data = extract_json(
            response.text or ""
        )

        return data, "gemini"

    except Exception:

        return None, "demo"