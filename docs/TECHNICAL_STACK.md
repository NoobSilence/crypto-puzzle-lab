# Technical Stack - Laptop Setup

## Specifications
- CPU: Intel Core i3-6157U @ 2.40GHz (2 cores/4 threads)
- RAM: 8 GB
- Storage: 238 GB SSD
- GPU: Intel Iris Graphics 550 (no CUDA/OpenCL)
- OS: Windows 10 (64-bit)

## Installed Software

### Python
- Version: 3.11.3
- Packages: embit 0.8.0, coincurve 21.0.0, pycryptodome 3.23.0, pillow 12.3.0, numpy 2.4.6, opencv-python 5.0.0.93, yt-dlp

### ffmpeg
- Version: 9.0-full_build
- Use: Video frame extraction

### Git
- Version: 2.55.0.windows.3

## Scripts

### Certificering
- scripts/cert/laptop_cert.py

### Tools
- scripts/tools/guntis_analyze.py
- scripts/tools/guntis_frames_all.py

### Attacks
- scripts/attacks/guntis/guntis_attack.py
- scripts/attacks/guntis/guntis_attack2.py
- scripts/attacks/guntis/guntis_exhaustive.py
- scripts/attacks/guntis/guntis_checksum_list.py
- scripts/attacks/guntis/guntis_focused.py
- scripts/attacks/gsmg/gsmg_final_solver_v2.py

## Performance

### BIP39 Derivation
- BTC (BIP44/84): ~1000 addr/sec
- ETH (Keccak): ~800 addr/sec
- With passphrase: ~500 addr/sec
