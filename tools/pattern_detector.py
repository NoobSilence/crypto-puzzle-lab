class PatternDetector:
    def __init__(self):
        self.patterns = load_patterns_from_github()

    def analyze_case(self, case_data):
        """
        Analyze a new hack case and extract patterns.
        """
        patterns_found = []
        for pattern in self.patterns:
            if pattern.matches(case_data):
                patterns_found.append(pattern.name)
        return patterns_found

    def predict_next_targets(self, pattern_name):
        """
        Given a pattern, predict which protocols are vulnerable.
        """
        pattern = self.patterns[pattern_name]
        vulnerable_protocols = []
        for chain in ["ethereum", "base", "arbitrum", "optimism", "bsc", "tron"]:
            protocols = scan_protocols_on_chain(chain, pattern.vulnerability_class)
            vulnerable_protocols.extend(protocols)
        return vulnerable_protocols
