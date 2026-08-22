# GPU Methodology - Bewezen Economie

Bron: bitcoinwords.github.io/how-i-checked-over-1-trillion-mnemonics + floflo777/engines + oritwoen/kangaroo.

## Case study: 1 triljoen mnemonics, 0.99 BTC gewonnen

- CPU (Rust): 1,250 mnemonics/sec -> 25 jaar voor 2^40
- GPU (2080Ti, OpenCL): 143,000 mnemonics/sec -> 83 dagen solo
- Pool van ~80 GPUs (vast.ai + Azure): piek 40 miljard/uur -> 30 uur totaal
- Kosten: $350 vast.ai + $75 Azure = $425
- Winst: 0.99 BTC

## OpenCL optimalisaties

- Alles on-GPU: SHA-256, SHA-512, RIPEMD-160, EC add/mult (libsecp256k1 port, ~2000 regels)
- 32kB precompute table ipv 64kB (past in constant memory)
- Batches van 16.7M mnemonics (network latency < 1%)
- 2080Ti meest kostenefficient; V100 slechts 15% sneller maar 4x duurder

## Open source engines

- floflo777/engines: checksum-aware BIP39, brainwallet, Electrum v1, Arweave kernels
- oritwoen/kangaroo: GPU Pollard Kangaroo voor ECDLP met bekende pubkey

## Kangaroo-aanval

- Voor puzzles met bekende pubkey (BTC tx #135-160): O(sqrt n) ipv O(n)
- 66-bit puzzle opgelost met rho/kangaroo nadat pubkey bloot kwam
- Bots stelen soms solutions via mempool watching (RBF fee bump nodig)

## Toepassing op ons

- Fase 2: huur 1-2x 2080Ti op vast.ai (~$0.20/uur) voor Guntis connecting-words sweep
- Gebruik floflo777 engines ipv zelf OpenCL schrijven
- Certificeer tegen abandon-x11-about vector VOOR elke sweep
