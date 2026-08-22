# Guntis Breakthrough - Externe Intel (22 aug 2026)

Bron: floflo777/open-crypto-puzzles/1-big-prizes/guntis-vitolins-metamask-8-6eth (laatst bijgewerkt 21 aug 2026, 14 uur geleden).

## De 5 hints van de auteur (over ~40 latere video descriptions)

1. Laatste woord is een tropische vogel -> parrot (positie 12)
2. Woord 1 noemt Nederland -> dutch (positie 1)
3. Woord 5 is gemaakt van gecondenseerde waterdruppels -> fog (positie 5)
4. Hint 4 video (youtube 03wXiMczCXk, gesproken op 15:26) -> fiber
5. Hint 5 video (youtube ZjBJKooVmuE, letter voor letter gespeld op 17:28) -> fork

## Bevestigde feiten

- Positie 1 = dutch
- Positie 5 = fog (of cloud; laatste commit lost op: fog)
- Positie 12 = parrot
- fiber en fork = bevestigde leden, posities onbekend
- fork zat in archived 2020 blog metadata (article:tag: ethereum fork, round)
- Tekst van video+blog byte-voor-byte onveranderd sinds 2020 (web archive 2020-05-28)
- 5 planted sentences statistisch bevestigd (z = 3.71 vs control corpus)

## WALLET IS ACTIEF

Guntis heeft 7 outgoing txs gedaan sinds 2021-05 (laatst 2024-06-04, totaal ~1.377 ETH). Hij houdt de private key nog steeds en gebruikt hem periodiek. Dit is GEEN bevroren escrow.

## Wat floflo777 al testte

- 16.75 miljard derivations, 8 families, allemaal negatief, witnessed
- Anchors 1/5/12 + fiber/fork in pool

## OPEN LEADS (nog NOOIT getest - onze kans)

1. Connecting words toevoegen aan pool: there, will, also, only, because, like (BIP39: will, only, like) - uren op 1 GPU
2. Substrings van langere woorden (auteur: possible zit in impossible) - dag op 1 GPU
3. Video+post metadata opnieuw lezen (blog tags zaten er jaren verborgen) - 1 uur menswerk

## Onze aanvalsplan

- Fix posities 1=dutch, 5=fog, 12=parrot
- Plaats fiber+fork in 2 van 9 vrije slots (72 manieren)
- Vul 7 slots uit pool: round, cattle, forest, wood, fresh, hunter, lake, goat, sing, song (+ will, only, like)
- Checksum pre-filter (1/16), dan ETH Keccak derivatie
- Laptop: ~43M combos -> ~2.7M derivations -> haalbaar met multiprocessing
- Script: scripts/attacks/guntis/guntis_anchored_attack.py
