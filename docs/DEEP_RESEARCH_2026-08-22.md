# Deep Research Report - 22 August 2026

Global scan of the crypto puzzle landscape. Sources: floflo777/open-crypto-puzzles, oritwoen/boha, btcpuzzle.info, privatekeys.pw, bitcoinwords.github.io.

## Market Overview

- 31 funded unsolved puzzles = $641,000 (9.71 BTC + 13.21 ETH + 1900 AR)
- Bitcoin Puzzle Transaction: 160 puzzles, 83 solved, 903 BTC unsolved
- Puzzle #66 solved (6.6 BTC); pubkeys known for #135-160 (Kangaroo attack possible)

## Our Puzzles in Global Context

| Puzzle | Value | Global rank | Status |
|--------|--------|------------|--------|
| GSMG | 5.0069 BTC ($315K) | #1 big prize | open |
| Guntis | 8.61 ETH ($16K) | #6 big prize | open |
| BLM | 0.201 BTC ($12.7K) | #7 big prize | open |

## External Researchers Following Our Work

floflo777 has investigated 40 puzzles, solved several, and documents addresses, clues, attempted approaches, and stopping points for each puzzle. His repo accepts pull requests (community member wayzeek has already contributed one).

## Key External Repositories

- github.com/floflo777/open-crypto-puzzles (research database + engines/ GPU code)
- github.com/oritwoen/boha (puzzle data + kangaroo GPU solver)
- github.com/oritwoen/kangaroo (Pollard Kangaroo ECDLP, O(sqrt n))
- btcpuzzle.info (160-puzzle tracker + pools)
- privatekeys.pw (21 puzzles, solved keys directory)

## Methodology Lessons from the Field

1. GPU economics proven: 1 trillion mnemonics in 30 hours, $425 cost, 0.99 BTC won (bitcoinwords.github.io)
2. CPU 1,250/sec vs GPU (2080Ti) 143,000/sec; vast.ai + Azure credits
3. Checksum-aware BIP39 OpenCL engines are open source (floflo777/engines)
4. Kangaroo attack on puzzles with a known pubkey: O(sqrt n) instead of O(n)
5. Certify oracles against solved siblings BEFORE large sweeps
6. Metadata (HTML tags, article:tag) can contain hints absent from visible text
7. Check wallet activity: a funded escrow can be an ACTIVE wallet
