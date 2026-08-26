# GPU Methodology - Proven Economics

Sources: bitcoinwords.github.io/how-i-checked-over-1-trillion-mnemonics + floflo777/engines + oritwoen/kangaroo.

## Case Study: 1 Trillion Mnemonics, 0.99 BTC Won

- CPU (Rust): 1,250 mnemonics/sec -> 25 jaar voor 2^40
- GPU (2080Ti, OpenCL): 143,000 mnemonics/sec -> 83 dagen solo
- Pool van ~80 GPUs (vast.ai + Azure): piek 40 miljard/uur -> 30 uur totaal
- Cost: $350 vast.ai + $75 Azure = $425
- Winnings: 0.99 BTC

## OpenCL optimalisaties

- Alles on-GPU: SHA-256, SHA-512, RIPEMD-160, EC add/mult (libsecp256k1 port, ~2000 regels)
- 32kB precompute table ipv 64kB (past in constant memory)
- Batches van 16.7M mnemonics (network latency < 1%)
- 2080Ti meest kostenefficient; V100 slechts 15% sneller maar 4x duurder

## Open source engines

- floflo777/engines: checksum-aware BIP39, brainwallet, Electrum v1, Arweave kernels
- oritwoen/kangaroo: GPU Pollard Kangaroo voor ECDLP met bekende pubkey

## Kangaroo Attack

- For puzzles with a known pubkey (BTC tx #135-160): O(sqrt n) instead of O(n)
- 66-bit puzzle solved with rho/kangaroo after the pubkey was exposed
- Bots sometimes steal solutions by watching the mempool (RBF fee bump required)

## Application to Our Work

- Phase 2: rent 1-2x 2080Ti on vast.ai (~$0.20/hour) for the Guntis connecting-words sweep
- Use floflo777 engines instead of writing OpenCL from scratch
- Certify against the abandon-x11-about vector BEFORE every sweep
