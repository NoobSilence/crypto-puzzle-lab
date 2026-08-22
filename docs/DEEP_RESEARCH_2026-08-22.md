# Deep Research Report - 22 augustus 2026

Wereldwijde scan van crypto puzzle landschap. Bronnen: floflo777/open-crypto-puzzles, oritwoen/boha, btcpuzzle.info, privatekeys.pw, bitcoinwords.github.io.

## Marktoverzicht

- 31 gefinancierde onopgeloste puzzels = $641,000 (9.71 BTC + 13.21 ETH + 1900 AR)
- Bitcoin Puzzle Transaction: 160 puzzels, 83 opgelost, 903 BTC onopgelost
- Puzzle #66 opgelost (6.6 BTC); pubkeys bekend voor #135-160 (Kangaroo-aanval mogelijk)

## Onze puzzels in wereldcontext

| Puzzel | Waarde | Wereldrang | Status |
|--------|--------|------------|--------|
| GSMG | 5.0069 BTC ($315K) | #1 big prize | open |
| Guntis | 8.61 ETH ($16K) | #6 big prize | open |
| BLM | 0.201 BTC ($12.7K) | #7 big prize | open |

## Externe onderzoekers volgen ons werk

floflo777 heeft 40 puzzels onderzocht, loste er enkele op, en documenteert per puzzel: adressen, clues, wat hij probeerde, waar hij vastliep. Zijn repo accepteert pull requests (community lid wayzeek leverde al een PR).

## Belangrijkste externe repos

- github.com/floflo777/open-crypto-puzzles (research database + engines/ GPU code)
- github.com/oritwoen/boha (puzzle data + kangaroo GPU solver)
- github.com/oritwoen/kangaroo (Pollard Kangaroo ECDLP, O(sqrt n))
- btcpuzzle.info (160-puzzle tracker + pools)
- privatekeys.pw (21 puzzels, solved keys directory)

## Methodologie-lessen uit de wereld

1. GPU-economie bewezen: 1 triljoen mnemonics in 30 uur, $425 kosten, 0.99 BTC gewonnen (bitcoinwords.github.io)
2. CPU 1,250/sec vs GPU (2080Ti) 143,000/sec; vast.ai + Azure credits
3. Checksum-aware BIP39 OpenCL engines zijn open source (floflo777/engines)
4. Kangaroo-aanval op puzzles met bekende pubkey: O(sqrt n) ipv O(n)
5. Certificeer oracles tegen solved siblings VOOR grote sweeps
6. Metadata (HTML tags, article:tag) bevat hints die zichtbare tekst niet heeft
7. Wallet-activiteit checken: gefinancierd escrow kan een ACTIEVE wallet zijn
