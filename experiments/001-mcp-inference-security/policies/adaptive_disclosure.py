class AdaptiveDisclosurePolicy:
    def __init__(self):
        self.seen = set()

    def check(self, location, resource):
        key = (location, resource)

        if key not in self.seen:
            self.seen.add(key)

        coverage = len(self.seen)

        if coverage <= 3:
            level = 0
        elif coverage <= 5:
            level = 1
        elif coverage <= 7:
            level = 2
        else:
            level = 3

        return {
            "coverage_count": coverage,
            "disclosure_level": level,
        }


def degrade_value(value, disclosure_level):
    if disclosure_level == 0:
        return {
            "precision": "exact",
            "value": value,
        }

    if disclosure_level == 1:
        lower = (value // 10) * 10
        upper = lower + 10

        return {
            "precision": "range",
            "value": f"{lower}-{upper}",
        }

    if disclosure_level == 2:
        if value < 34:
            category = "low"
        elif value < 67:
            category = "medium"
        else:
            category = "high"

        return {
            "precision": "category",
            "value": category,
        }

    return {
        "precision": "regional",
        "value": "limited",
    }
