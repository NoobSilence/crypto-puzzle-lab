# Guntis Breakthrough - External Intelligence (22 Aug 2026)

Source: floflo777/open-crypto-puzzles/1-big-prizes/guntis-vitolins-metamask-8-6eth (last updated 21 Aug 2026, 14 hours earlier).

## The Author's 5 Hints (Across ~40 Later Video Descriptions)

1. The last word is a tropical bird -> parrot (position 12)
2. Word 1 refers to the Netherlands -> dutch (position 1)
3. Word 5 is made of condensed water droplets -> fog (position 5)
4. Hint 4 video (YouTube 03wXiMczCXk, spoken at 15:26) -> fiber
5. Hint 5 video (YouTube ZjBJKooVmuE, spelled letter by letter at 17:28) -> fork

## Confirmed Facts

- Position 1 = dutch
- Position 5 = fog or cloud (the upstream dossier does not treat this as settled)
- Position 12 = parrot
- fiber and fork = confirmed members, positions unknown
- fork appeared in archived 2020 blog metadata (article:tag: ethereum fork, round)
- Video and blog text unchanged byte-for-byte since 2020 (Web Archive 2020-05-28)
- 5 planted sentences statistically confirmed (z = 3.71 vs control corpus)

## WALLET IS ACTIVE

Guntis made 7 outgoing transactions since 2021-05 (most recently 2024-06-04, ~1.377 ETH total). He still holds the private key and uses it periodically. This is NOT a frozen escrow.

## What floflo777 Already Tested

- 16.75 billion derivations, across 8 families, all negative and witnessed
- Anchors 1/5/12 + fiber/fork in pool

## OPEN LEADS (NEVER TESTED - Our Opportunity)

1. Add connecting words to the pool: there, will, also, only, because, like (BIP39: will, only, like) - hours on 1 GPU
2. Substrings of longer words (author: possible appears in impossible) - one day on 1 GPU
3. Re-read video and post metadata (blog tags were hidden for years) - 1 hour of human work

## Our Attack Plan

- Fix positions 1=dutch, 5=fog, 12=parrot
- Place fiber+fork in 2 of 9 free slots (72 ways)
- Fill 7 slots from the pool: round, cattle, forest, wood, fresh, hunter, lake, goat, sing, song (+ will, only, like)
- Checksum pre-filter (1/16), then ETH Keccak derivation
- Laptop: ~43M combinations -> ~2.7M derivations -> feasible with multiprocessing
- Script: scripts/guntis_anchored_attack_v2.py
