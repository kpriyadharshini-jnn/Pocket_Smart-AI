from urllib.parse import quote_plus


PLATFORMS = {

    "Amazon":
        "https://www.amazon.in/s?k={q}",

    "Flipkart":
        "https://www.flipkart.com/search?q={q}",

    "IKEA":
        "https://www.ikea.com/in/en/search/?q={q}",

    "Swiggy":
        "https://www.swiggy.com/search?query={q}",

    "Zomato":
        "https://www.zomato.com/search?q={q}",

    "OYO":
        "https://www.oyorooms.com/search/?location={q}"
}


def platform_link(
    platform: str,
    query: str
) -> str:

    template = PLATFORMS.get(
        platform,
        PLATFORMS["Amazon"]
    )

    return template.format(
        q=quote_plus(query)
    )


def demo_catalog(
    planner_type: str,
    budget: float
):

    if planner_type == "home":

        return [

            {
                "name": "LED Ceiling Light",
                "category": "Lighting",
                "platform": "IKEA",
                "estimated_price": 1299,
                "reason":
                    "Energy-efficient lighting option."
            },

            {
                "name": "Study Table",
                "category": "Furniture",
                "platform": "Amazon",
                "estimated_price": 3499,
                "reason":
                    "Compact table suitable for small spaces."
            },

            {
                "name": "Decorative Wall Art Set",
                "category": "Decor",
                "platform": "Flipkart",
                "estimated_price": 999,
                "reason":
                    "Low-cost way to add visual interest."
            },

            {
                "name": "Ceiling Fan",
                "category": "Utility",
                "platform": "Amazon",
                "estimated_price": 2299,
                "reason":
                    "Practical airflow upgrade."
            }

        ]

    if planner_type == "party":

        return [

            {
                "name": "Catering Search",
                "category": "Food",
                "platform": "Swiggy",
                "estimated_price":
                    max(500, budget * 0.35),
                "reason":
                    "Search local catering and food listings."
            },

            {
                "name": "Restaurant Food Search",
                "category": "Food",
                "platform": "Zomato",
                "estimated_price":
                    max(500, budget * 0.20),
                "reason":
                    "Compare nearby food providers."
            },

            {
                "name": "Decoration Supplies",
                "category": "Decoration",
                "platform": "Amazon",
                "estimated_price":
                    max(300, budget * 0.10),
                "reason":
                    "Reusable decoration supplies."
            },

            {
                "name": "Stay / Venue Search",
                "category": "Venue",
                "platform": "OYO",
                "estimated_price":
                    max(800, budget * 0.20),
                "reason":
                    "Search accommodation and venue-style options."
            }

        ]

    return [

        {
            "name": "Minimal Pendant Necklace",
            "category": "Necklace",
            "platform": "Amazon",
            "estimated_price":
                max(599, budget * 0.22),
            "reason":
                "Versatile style for many occasions."
        },

        {
            "name": "Stud Earrings",
            "category": "Earrings",
            "platform": "Flipkart",
            "estimated_price":
                max(399, budget * 0.12),
            "reason":
                "Easy-to-match accessory."
        },

        {
            "name": "Bangle Bracelet Set",
            "category": "Bracelet",
            "platform": "Amazon",
            "estimated_price":
                max(499, budget * 0.15),
            "reason":
                "Adds coordinated detail."
        },

        {
            "name": "Statement Earrings",
            "category": "Earrings",
            "platform": "Flipkart",
            "estimated_price":
                max(699, budget * 0.25),
            "reason":
                "Suitable for a stronger accent."
        }

    ]