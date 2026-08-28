def hunt_similar_protocols(hack_case):
    """
    Given a hack case, find other protocols with same vulnerability:
    1. Extract vulnerability class (e.g., SC03 oracle manipulation)
    2. Scan DeFi protocols on same chains
    3. Check for same code patterns
    4. Rank by TVL (potential bounty size)
    5. Output: list of protocols to audit
    """
    # Example: After Moonwell, scan all Base lending protocols
    # for spot-price oracles + illiquid collateral
    # Submit bounties before they get hacked
    pass


def scan_base_lending_protocols():
    """
    Scan all lending protocols on Base for Moonwell-like vulnerabilities.

    The provider and analysis helpers are intentionally injected separately;
    this function does not make network calls or assume a specific data source.
    """
    protocols = get_all_lending_protocols(chain="base")
    vulnerable_protocols = []

    for protocol in protocols:
        oracle_type = analyze_oracle_implementation(protocol.address)
        collateral_tokens = get_accepted_collateral(protocol.address)

        if oracle_type == "spot" and has_illiquid_collateral(collateral_tokens):
            vulnerable_protocols.append({
                "protocol": protocol.name,
                "tvl": protocol.tvl,
                "risk_score": calculate_risk(oracle_type, collateral_tokens),
                "bounty_potential": protocol.tvl * 0.1,
            })

    return sorted(vulnerable_protocols, key=lambda item: item["tvl"], reverse=True)
