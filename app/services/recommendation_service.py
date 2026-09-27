from .catalog_service import demo_catalog
from .catalog_service import platform_link

from .gemini_service import generate_recommendation


def fallback_plan(
    planner_type: str,
    payload: dict,
    catalog: list[dict]
):

    budget = float(
        payload["budget"]
    )

    recommendations = []

    for item in catalog:

        copy = dict(item)

        copy["estimated_price"] = round(
            float(
                copy["estimated_price"]
            ),
            2
        )

        copy["quantity"] = 1

        copy["link"] = platform_link(
            copy["platform"],
            copy["name"]
        )

        recommendations.append(
            copy
        )

    recommendations = sorted(
        recommendations,
        key=lambda x: x["estimated_price"]
    )

    selected = []

    running_total = 0

    for item in recommendations:

        price = (
            item["estimated_price"]
            * item.get("quantity", 1)
        )

        if (
            running_total + price
            <= budget
        ):

            selected.append(item)

            running_total += price

    recommendations = selected

    total = round(
        running_total,
        2
    )

    if planner_type == "home":

        allocations = {
            "Furniture":
                round(budget * 0.40, 2),

            "Lighting":
                round(budget * 0.20, 2),

            "Decor":
                round(budget * 0.20, 2),

            "Utilities":
                round(budget * 0.20, 2)
        }

        title = "Smart Home Interior Plan"

    elif planner_type == "party":

        allocations = {

            "Food":
                round(budget * 0.45, 2),

            "Venue":
                round(budget * 0.25, 2),

            "Decoration":
                round(budget * 0.15, 2),

            "Entertainment":
                round(budget * 0.15, 2)
        }

        title = "Smart Party Budget Plan"

    else:

        allocations = {

            "Necklace":
                round(budget * 0.35, 2),

            "Earrings":
                round(budget * 0.25, 2),

            "Bracelet":
                round(budget * 0.20, 2),

            "Reserve":
                round(budget * 0.20, 2)
        }

        title = "Smart Jewelry Budget Plan"

    return {

        "title": title,

        "summary":
            "A PocketSmart AI demo plan generated "
            "from the local recommendation catalog.",

        "estimated_total": total,

        "budget_remaining":
            round(
                max(0, budget - total),
                2
            ),

        "allocations": allocations,

        "recommendations":
            recommendations,

        "tips": [

            "Compare the linked platform listings before purchasing.",

            "Displayed prices are estimates and should be verified.",

            "Keep a small reserve for delivery, taxes or unexpected costs."

        ]
    }


def create_plan(
    planner_type: str,
    payload: dict,
    image_bytes=None,
    image_mime=None
):

    catalog = demo_catalog(
        planner_type,
        float(payload["budget"])
    )

    for item in catalog:

        item["link"] = platform_link(
            item["platform"],
            item["name"]
        )

    ai_result, source_mode = generate_recommendation(

        planner_type,

        payload,

        catalog,

        image_bytes=image_bytes,

        image_mime=image_mime
    )

    result = (
        ai_result
        if ai_result
        else fallback_plan(
            planner_type,
            payload,
            catalog
        )
    )

    budget = float(
        payload["budget"]
    )

    result.setdefault(
        "title",
        f"{planner_type.title()} Budget Plan"
    )

    result.setdefault(
        "summary",
        "Budget-aware recommendation plan."
    )

    result.setdefault(
        "allocations",
        {}
    )

    result.setdefault(
        "recommendations",
        []
    )

    result.setdefault(
        "tips",
        []
    )

    result["estimated_total"] = round(
        float(
            result.get(
                "estimated_total",
                0
            )
        ),
        2
    )

    result["budget_remaining"] = round(
        max(
            0,
            budget -
            result["estimated_total"]
        ),
        2
    )

    for item in result["recommendations"]:

        item.setdefault(
            "quantity",
            1
        )

        item.setdefault(
            "category",
            "General"
        )

        item.setdefault(
            "platform",
            "Amazon"
        )

        item.setdefault(
            "reason",
            "Budget-aware recommendation."
        )

        item.setdefault(
            "link",
            platform_link(
                item["platform"],
                item.get(
                    "name",
                    "products"
                )
            )
        )

    result["planner_type"] = planner_type

    result["budget"] = budget

    result["source_mode"] = source_mode

    return result