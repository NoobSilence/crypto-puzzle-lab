class BountyHunter:
    def __init__(self):
        self.immunefi_programs = load_immunefi_programs()

    def find_high_value_targets(self):
        """
        Find protocols with:
        - High TVL (large bounty potential)
        - Known vulnerability patterns
        - Active bug bounty program
        """
        targets = []
        for program in self.immunefi_programs:
            if program.tvl > 10_000_000:  # $10M+ TVL
                if self.has_known_vulnerability(program):
                    targets.append({
                        "protocol": program.name,
                        "tvl": program.tvl,
                        "max_bounty": program.max_bounty,
                        "vulnerability": self.identify_vulnerability(program),
                    })
        return sorted(targets, key=lambda item: item["max_bounty"], reverse=True)
