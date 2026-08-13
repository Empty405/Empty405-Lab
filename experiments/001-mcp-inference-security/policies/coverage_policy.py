class CoveragePolicy:
    def __init__(self, max_unique_combinations=5):
        self.max_unique_combinations = max_unique_combinations
        self.seen = set()

    def check(self, location, resource):
        key = (location, resource)

        if key in self.seen:
            return {
                "allowed": True,
                "new_coverage": False,
                "coverage_count": len(self.seen),
            }

        if len(self.seen) >= self.max_unique_combinations:
            return {
                "allowed": False,
                "new_coverage": True,
                "coverage_count": len(self.seen),
            }

        self.seen.add(key)

        return {
            "allowed": True,
            "new_coverage": True,
            "coverage_count": len(self.seen),
        }
