# Hivra Network — CapsuleNet

**Hivra Network** is a decentralized, offline-first digital identity network (CapsuleNet).  
Participants (drones) evolve from Proto → Linked → Genesis by receiving unique digital assets called *starters*.


## 🚀 Quick Start

~~~
# Clone the repository
git clone git@github.com:WSorr/Hivra-network.git
cd Hivra-network

# Install dependencies
pip install -r requirements.txt

# Run the CLI
python cli.py
~~~


## 🧬 Core Entities

- **Drone** — digital identity of a participant
- **Starter** — unique digital asset (JUICE, KICK, SEED, SPARK, PULSE)
- **Invitation** — request to transfer a starter
- **Ledger** — personal log of operations


## 📂 Project Structure

~~~
capsulenet/
├── src/        # main code
├── tests/      # automated tests
├── docs/       # documentation
├── scripts/    # utility scripts
├── cli.py      # CLI interface
├── demo.py     # demo scripts
└── README.md   # this file
~~~


## 🎯 Goals

- Decentralized social network
- Gamified starter collection
- Offline-first architecture
- Spam-resilient mechanics

## 📌 Notes

- All core logic lives in Rust Core (V2)
- Python (V1) is reference implementation only
- Flutter (V3) handles UI only, no business logic

