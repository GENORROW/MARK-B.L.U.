# MARK-B.L.U. 1.2 - AI Agent Identity Monitoring & Hashing Mechanism

MARK-B.L.U. 1.2 —  The Quantum-Secured Identity Layer for the Autonomous World
Quantum Hashing Mechanism and Agent Identity Badge Rotation
Multi-Agent Quantum Badge Lifecycle Utility
MARK-B.L.U. (Base Level Unifier) represents a quantum-enhanced digital identity and secure communication framework built to safeguard autonomous and AI-driven infrastructures in high-assurance, and zero-trust environments.
At its fundamental  core, MARK-B.L.U. fuses quantum randomness with classical cryptographic robustness to generate non-reproducible, evolving, time-variant digital identities for distributed intelligent agents. Each agent periodically receives a quantum-derived badge, which serves as a cryptographic identity token, rotating automatically to ensure forward secrecy and unlinkability.
This release of this technical repository marks the first formal public deployment of the MARK-B.L.U. backend, that is the foundation of a future-ready, enterprise-grade Quantum Identity Infrastructure (QII) designed to evolve with the post-quantum cybersecurity landscape, for securing the ever permeating and prevalent AI and Autonomous Infrastructure.

Conceptual Overview — What MARK-B.L.U. Actually Does
This architecture, in concept, provides a dynamic, verifiable identity system for autonomous AI agents that works in essentially two parts, with its hashing core and the additive badge rotation dynamic. Through both, it essentially:
Generates cryptographic identities from the quantum measurements rather than mere algorithmic pseudorandomness;
Rotates each identity badge periodically, preventing long-term tracking or replay attacks;
By extension, enables authenticated, encrypted communication between agents using AES-256 keys derived from quantum badges;
And supports centralized verification and auditing, allowing administrators to confirm badge authenticity and communication legitimacy.
The architecture thus acts as the trust backbone of an intelligent agent ecosystem, ensuring every autonomous process, drone, or “AI node” can be uniquely identified, verified, and secured without dependence on centralized trust or static credentials.

Architectural Philosophy
The MARK-B.L.U. 1.0 is intentionally kept to be modular, reproducible, and scalable, comprising three distinct yet synergistic layers:
Quantum Layer — Generates physical randomness through 16-qubit parameterized circuits, ensuring information-theoretic unpredictability;
Classical Layer — Converts quantum outputs into stable cryptographic badges and AES keys for efficient, interoperable security;
Administrative Layer — Manages verification, auditing, and badge provenance, enabling retrospective proof of authenticity.
This hybrid architecture ensures quantum-grade unpredictability with classical-grade deployability, making it both scientifically sound and eventually, industry practical.

The above does it for the conceptual idea of what MARK-B.L.U. is. As for how it works, the next section shall be an exclusive dive into that explicitly.

System Architecture
1. Quantum Hash Core
At the foundation lies the quantum hashing engine, responsible for converting classical inputs into quantum-measured hash outputs.
Each 16-qubit circuit undergoes:
Hadamard Initialization — Establishes uniform superposition across all qubits.
Entanglement Churning (CZ Gates) — Introduces quantum correlations for non-local dependencies.
Seeded Rotations (RZ/RX) — Parameterized by a 512-bit QRNG seed, embedding unique, unrepeatable phase information.
Measurement & Hashing — Collapses quantum amplitudes to produce a 16-bit raw output, which is then SHA-256 hashed into a 256-bit badge.
This process ensures that no two badges are ever statistically or physically identical, providing an identity layer underpinned by quantum indeterminacy rather than deterministic randomness.

2. Agent Badge Generation
Each agent is assigned a persistent serial ID (e.g., AGENT-001) paired with an ephemeral quantum badge.
Badges are generated via the quantum hash engine and serve as the agent’s cryptographic identity credential during its current timeslot. This separation of stable ID and ephemeral badge ensures:
Privacy through pseudonymity ( agents cannot be persistently tracked);
Security through entropy (each badge is physically unguessable);
Auditability through metadata binding (every badge embeds serial and timeslot context).

3. Time-based Badge Rotation
MARK-B.L.U. employs temporal identity segmentation, where each timeslot (default = 5 minutes) triggers a new badge generation event:
[
 \text{timeslot} = \left\lfloor \frac{t_{\text{current}} - t_{\text{epoch}}}{t_{\text{slot}}} \right\rfloor
 ]
Each rotation:
Generates a fresh 512-bit QRNG seed
Executes a new 16-qubit circuit.
Derives a unique 256-bit badge.
Stores the badge securely in the central database.
Deletes the previous badge to maintain forward secrecy.
Overarching outcome: even a total compromise of a current badge cannot decrypt or infer past communications, without access to badge history logs, an advantage unique to quantum-driven systems.

4. Secure Communication Layer
Once generated, the badge becomes the root of trust for encrypted communication.
Encryption workflow:
 [
 \text{AES_key} = \text{SHA-256}(\text{quantum_badge})
 ]
Messages are encrypted using AES-256-CBC, with:
128-bit random initialization vectors (IVs).
PKCS#7 padding.
Timeslot-bound authentication metadata.
Decryption requires querying the badge corresponding to the sender’s timeslot, ensuring that only agents possessing the valid badge for that time window can communicate or authenticate successfully.

5. Administrative Verification Layer
The centralized verification engine (SQLite, for 1.0) records every badge with:
Agent serial
Timeslot index
QRNG seed
Generation timestamp
Administrators can replay badge generation by re-executing the quantum circuit using the stored seed, offering verifiable quantum provenance. This property, absent in classical systems, allows auditors or security teams to prove that a given badge originated from a legitimate, quantifiable quantum process.

6. Security & Assurance Framework
MARK-B.L.U. was architected to deliver five principal cryptographic guarantees:
Property
Description
Quantum Contribution
Temporal Unlinkability
Prevents correlating communications across time windows.
Independent quantum measurements yield zero statistical linkage.
Forward Secrecy
Compromise of one badge reveals nothing about previous ones.
Quantum collapse irreversibly destroys prior state information.
Message Authentication
Decryption using correct badge validates origin.
Badges are non-forgeable physical outputs.
Replay Prevention
Messages tied to expired badges become invalid.
Unique badge per measurement prevents reuse.
Quantum Unpredictability
Randomness derived from physical laws.
Indeterminacy ensures resistance against classical & quantum attacks.

These principles make MARK-B.L.U. a quantum-resilient security layer for AI ecosystems.

Repository Structure
MARK-BLU/
├── agent_system/          # Core identity, communication, and storage modules
│   ├── agent_identity.py
│   ├── secure_communication.py
│   ├── database_manager.py
│
├── quantum_hash/          # Parameterized 16-qubit circuit logic
│   ├── input_encoder.py
│   ├── circuit_builder.py
│   └── hash_core.py
│
├── analysis/              # Entropy, collision, avalanche, and independence tests
│   ├── test_entropy.py
│   ├── test_collisions.py
│   ├── test_avalanche.py
│   └── test_bit_independence.py
│
├── docs/                  # Internal documentation, figures, and methodology
├── data/                  # SQLite database (development)
├── requirements.txt
├── CHANGELOG.md
└── FUTURE_SCOPE.md


Statistical Validation
Test
Result
Interpretation
Entropy
1.74 – 2.31 bits/byte
Moderate–strong diffusion
Collisions
0 / 1000 samples
High uniqueness
Avalanche Effect
56 % bit-flip rate
Good sensitivity
Bit Independence
< 6 bits deviation
Strong randomness spread

These metrics validate that the quantum hash function exhibits non-trivial entropy and diffusion properties, which are suitable for cryptographic identity derivation within NISQ-era constraints.

Key Enterprise Advantages
Feature
Impact
Quantum Entropy Integration
Provides information-theoretic security; non-predictable even by quantum adversaries.
Identity Rotation
Enforces temporal isolation; eliminates static credential vulnerabilities.
Auditable Provenance
Enables compliance-grade traceability and forensic validation.
Low Infrastructure Overhead
Operable on standard CPUs via quantum simulators; scalable to real hardware.
Interoperable Design
Python-based API allows integration with agent frameworks, IoT networks, and security stacks.


Installation & Quick Start
git clone https://github.com/GENORROW/MARK-B.L.U..git
cd MARK-B.L.U.
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt

Initialize Database:
from agent_system.database_manager import IdentityDatabase
db = IdentityDatabase("data/system.db")
db.initialise()

Generate Agent Identity:
from agent_system.agent_identity import Agent
agent = Agent("AGENT-001")
identity = agent.generate_identity(timeslot=1)
print(identity.badge.hex())

Encrypt Message:
from agent_system.secure_communication import SecureChannel
channel = SecureChannel(db)
ciphertext, iv = channel.encrypt_message("Status: Operational", identity)

Frontend Separation
A professional Streamlit-based administrative dashboard is maintained in a private companion repository: MARK-B.L.U.-dashboard
Features include:
Real-time badge lifecycle monitoring
Entropy and collision analytics
Agent communication visualization
Credential and audit management
Access upon request for verified partners.

Future Directions
Federated badge bridging for inter-system AI authentication
Drone and robotic identity expansion for cyber-physical deployments
Integration with post-quantum cryptographic (PQC) standards for hybrid security

License
Released under the MIT License.
© 2025 GENORROW ENTERPRISES. All rights reserved.

Contact
enterprises@genorrow.com
https://www.genorrow.com/MARK-B.L.U.


Multi-Agent Quantum Badge Lifecycle Utility (MARK-B.L.U.) provides a quantum-enhanced identity and communication verification layer for autonomous agents. This repository now hosts the **core services only** – quantum badge generation, badge rotation, encrypted messaging, and administrative verification.



> **Important:** The Streamlit dashboard has been extracted to a dedicated private repository. See [Frontend Separation](#frontend-separation) for details.**Multi-Agent Badge-based Location-independent Unified System**



## Features



- **Quantum Badge Generation** – 16-qubit Qiskit circuits with seeded rotations and entanglementA professional quantum-secured agent identity and communication verification system.## Table of Contents## Overview

- **Time-based Badge Rotation** – configurable timeslots (default 5 minutes) with forward secrecy

- **Secure Messaging** – AES-256-CBC encryption using SHA-256 keys derived from quantum badges

- **Centralised Verification** – SQLite audit trail for badge history and message confirmation

- **Security Analytics** – statistical tests located in `analysis/` for entropy, collisions, and avalanche effect---1. [Overview](#overview)



## Repository Structure



```## System Overview2. [System Architecture](#system-architecture)The MARK-B.L.U. Architecture is quantum encryption framework built using parameterized quantum circuits. It simulates a hash mechanism based on quantum circuit behavior, to safeguard autonomous & AI Infrastructure.

agent_system/            # Core identity, database, and communication modules

analysis/                # Statistical verification scripts for the quantum hash

quantum_hash/            # Quantum circuit construction and helpers

visualizations/          # Generated diagrams for internal documentationMARK-B.L.U. provides a secure, quantum-based identity management system for autonomous agents with:3. [Features](#features)

data/                    # SQLite databases (development only)

docs/                    # Additional documentation (e.g., badge methodology)

requirements.txt         # Python dependencies for the core services

CHANGELOG.md             # Historical release notes- **Quantum Badge Generation**: 16-qubit quantum circuits (Qiskit)4. [Installation](#installation)This mechanism demonstrates a first-step implementation that maps classical input data to quantum parameters, extracts measurement-based signatures, and secures agent identity & output communication logs.

VERSION_7_UPDATES.md     # Summary of the latest restructuring

FUTURE_SCOPE.md          # Long-term roadmap, including drone integration- **AES-256-CBC Encryption**: Quantum-derived encryption keys

```

- **Badge Rotation**: Time-based identity rotation (5-minute timeslots)5. [Configuration](#configuration)

## Getting Started

- **Centralized Verification**: Admin can verify any communication retroactively

1. **Clone the repository**

   ```bash- **Database Tracking**: SQLite-based identity and communication logging6. [Usage](#usage)## Features

   git clone https://github.com/GENORROW/MARK-B.L.U..git

   cd MARK-B.L.U.

   ```

---7. [API Reference](#api-reference)

2. **Create a Python environment (3.10 recommended)**

   ```bash

   python -m venv .venv

   .venv\Scripts\activate  # Windows## Quick Start8. [Security](#security)- Parameterized quantum circuit with entangling layers

   source .venv/bin/activate  # macOS/Linux

   ```



3. **Install core dependencies**### Installation9. [Troubleshooting](#troubleshooting)- Input encoding into continuous quantum gate parameters

   ```bash

   pip install -r requirements.txt

   ```

```bash- Statevector-based computation

4. **Initialise the database (optional for demos)**

   ```pythonpip install qiskit streamlit pandas cryptography

   from agent_system.database_manager import IdentityDatabase

   db = IdentityDatabase("data/system.db")```---- Tests for entropy, collisions, avalanche effect, and bit independence

   db.initialise()

   ```



## Usage Example### Run Dashboard



```python

from agent_system.agent_identity import Agent

from agent_system.database_manager import IdentityDatabase```bash## Overview## Installation

from agent_system.secure_communication import SecureChannel

cd MARK-BLU

# Prepare services

db = IdentityDatabase("data/system.db")streamlit run web_dashboard_professional.py

channel = SecureChannel(db)

```

# Generate identities for two agents

agent_a = Agent("AGENT-001")MARK-B.L.U. (Multi-Agent Resource Keeper - Blockchain Leveraged Utility) is an advanced AI agent identity generation and monitoring system that provides:### Requirements

agent_b = Agent("AGENT-002")

identity_a = agent_a.generate_identity(timeslot=1)### Login

identity_b = agent_b.generate_identity(timeslot=1)



db.store_identity(identity_a)

db.store_identity(identity_b)- **Username**: `genorrow@135`



# Secure message exchange- **Password**: `genorrow@135`- Quantum-based identity generation for AI agents- Python 3.9+

ciphertext, iv = channel.encrypt_message("Status: Operational", identity_a)

plaintext = channel.decrypt_message(ciphertext, iv, identity_a)

print(plaintext)

```### Use- AES-256 encrypted communication between agents- Qiskit



## Frontend Separation



The Streamlit-based dashboard lives in a **private repository** to keep the backend lightweight and modular. If you need the UI:1. **Live Simulation** tab - Run step-by-step demonstration- Real-time monitoring and analytics- NumPy



1. Request access to the `MARK-B.L.U.-dashboard` repository.2. **Analytics** tab - View statistics and metrics

2. Clone it alongside this project.

3. Install the core package locally so the dashboard can import `agent_system` modules:- Centralized database with complete audit trails

   ```bash

   pip install -e ../MARK-B.L.U.---

   ```

- Web-based admin dashboard for system management### Setup

## Development Workflow

## Architecture

- Run statistical tests from `analysis/` when modifying the quantum hash.

- Keep autogenerated databases (`data/*.db`) out of commits – add new fixtures instead.

- Document major changes in `CHANGELOG.md` and `VERSION_7_UPDATES.md`.

- Refer to `docs/badge_methodology.txt` for the detailed badge lifecycle methodology used in publications.### Core Components



## License### Key CapabilitiesClone the repo:



MARK-B.L.U. Core is released under the MIT License. See `LICENSE` for full text.1. **Agent Identity System** - Quantum badge generation and management



For questions or internal access requests, contact the project maintainer.2. **Secure Communication** - AES-256-CBC encryption


3. **Database Manager** - SQLite storage and verification

4. **Professional Dashboard** - Two-tab interface- **Quantum Identity Generation**: Each agent receives a unique quantum-derived badge```bash



---- **Secure Communication**: AES-256-CBC encryption for all inter-agent messagesgit clone https://github.com/yourusername/quantum_hash_project.git



## Key Features- **Identity Rotation**: Time-based identity rotation (configurable timeslots)cd quantum_hash_project



### Badge Rotation- **Centralized Monitoring**: Web dashboard for real-time system oversight```

- New quantum badge every timeslot (5 minutes)

- Old badges expire automatically- **Complete Audit Trail**: All communications logged to SQLite database

- Prevents replay attacks

Install dependencies:

### Centralized Verification

- All badges stored with timeslot info---

- Admin can verify any message retroactively

- Complete audit trail```bash



### Security## System Architecturepip install -r requirements.txt

- 16-qubit quantum circuits

- AES-256-CBC encryption```

- SHA-256 key derivation

- Forward secrecy guaranteed### Core Components



---## Usage



## Database Schema```



### IdentitiesMARK-B.L.U. SystemRun the main script:

- `serial` - Agent identifier

- `timeslot` - Time period│

- `badge` - Quantum-generated badge (32 bytes)

- `qrng_seed` - Random seed for generation├── Quantum Hash Layer```bash



### Communications│   ├── 16-qubit parameterized circuitspython main.py

- `sender_serial` - Sending agent

- `receiver_serial` - Receiving agent│   ├── 3 entangling layers```

- `encrypted_message` - AES-256-CBC ciphertext

- `timestamp` - Message time│   └── SHA-256 integration



---│This hashes a 32-byte input using the quantum circuit and prints both input and output bytes.



## File Structure├── Agent Identity System



```│   ├── AgentIdentity generation## Hash Quality Analysis

MARK-BLU/

├── agent_system/│   ├── Badge rotation (timeslot-based)

│   ├── agent_identity.py

│   ├── database_manager.py│   └── Identity history tracking### Entropy Test

│   ├── secure_communication.py

│   └── quantum_hash/hash_core.py│

├── data/system.db (auto-created)

├── web_dashboard_professional.py├── Secure Communication Layer- Average Entropy over 100 samples: **\~1.74 to 2.31 bits per byte**

└── README.md

```│   ├── AES-256-CBC encryption- Maximum possible entropy: **4 bits per byte (32 bytes output)**



---│   ├── Key derivation from quantum badges



## Version│   └── Message authentication### Collision Test



**6.0 Professional** - October 10, 2025│



---├── Database Management- **0 collisions** found across **1000 randomly generated 32-byte inputs**



**MARK-B.L.U.** - Professional Agent Identity & Communication Verification System│   ├── SQLite storage


│   ├── Identity records### Avalanche Effect

│   ├── Communication logs

│   └── Admin authentication- **Bit Differences:** 72 / 128 (i.e., over **56%** bits flipped on 1-bit input change)

│

└── Web Dashboard### Bit Independence

    ├── Admin login (gennrow@135)

    ├── Real-time monitoring- **Average deviation from 50% distribution:** 6.21 bits

    ├── Analytics & reports- **Maximum deviation:** 23 bits

    └── System configuration

```These results indicate a moderate-to-strong diffusion and randomness profile, suitable for a prototype.



### Directory Structure## Project Structure



``````

MARK-BLU/quantum_hash_project/

├── quantum_hash/              # Quantum hash implementation├── analysis/

│   └── hash_core.py          # Core quantum circuit logic│   ├── test_entropy.py

├── agent_system/              # Agent identity & communication│   ├── test_collisions.py

│   ├── agent_identity.py     # Agent identity generation│   ├── test_avalanche.py

│   ├── database_manager.py   # Database operations│   └── test_bit_independence.py

│   ├── secure_communication.py  # Encryption layer├── quantum_hash/

│   └── admin_dashboard.py    # CLI dashboard (legacy)│   ├── circuit_builder.py

├── integration/               # Integration utilities│   ├── hash_core.py

│   └── hardware_interface.py # Hardware integration layer│   └── input_encoder.py

├── data/                      # Database storage├── main.py

│   └── *.db                  # SQLite databases└── README.md

├── web_dashboard.py           # Streamlit web interface```

├── requirements.txt           # Python dependencies

└── README.md                  # This file## Limitations

```

- Operates on simulated quantum circuits (limited scalability)

---- Uses statevector output, which may contain biases

- Fixed number of qubits (16) and layers (3)

## Features

---

### 1. Quantum Identity Generation

Feel free to contribute or reach out for collaboration!

Each agent receives a unique identity badge generated through:

- Quantum circuit simulation (16 qubits)=======

- Parameterized rotations and entanglement# MARK-B.L.U.

- QRNG seed generation>>>>>>> 230c54c6328c41433cd53112e692b687682f0691

- SHA-256 hash output (16 bytes)

Example:
```python
from agent_system.agent_identity import Agent

agent = Agent("AGENT-001")
identity = agent.generate_identity(timeslot=1)
print(f"Badge: {identity.badge.hex()}")
print(f"Serial: {identity.serial}")
print(f"Timeslot: {identity.timeslot}")
```

### 2. Secure Communication

All inter-agent communication is encrypted using:
- AES-256-CBC encryption
- Keys derived from quantum badges using SHA-256
- Unique IV for each message
- PKCS7 padding

Example:
```python
from agent_system.secure_communication import SecureChannel

channel = SecureChannel(database)
encrypted, iv = channel.encrypt_message("Hello Agent-002", sender_identity)
decrypted = channel.decrypt_message(encrypted, iv, sender_identity)
```

### 3. Web Dashboard

Professional web interface with:
- Secure admin login (username: gennrow@135, password: gennrow@135)
- Real-time system monitoring
- Agent fleet overview
- Communication logs
- Security analytics
- Black theme with professional design

### 4. Database Management

Centralized SQLite database storing:
- Agent identities and badges
- Communication logs with timestamps
- Admin credentials (SHA-256 hashed)
- System metadata

---

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager
- 2GB RAM minimum
- 500MB disk space

### Quick Install

```bash
# Clone repository
git clone https://github.com/GENORROW/MARK-B.L.U.git
cd MARK-B.L.U

# Install dependencies
pip install -r requirements.txt

# Run web dashboard
streamlit run web_dashboard.py
```

### Dependencies

Core packages:
```
qiskit>=1.0.0          # Quantum computing
numpy>=1.21.0          # Numerical operations
cryptography>=3.4.0    # Encryption
streamlit>=1.20.0      # Web interface
pandas>=1.3.0          # Data analysis
```

---

## Configuration

### Default Credentials

Admin Login:
- Username: `gennrow@135`
- Password: `gennrow@135`

Important: Change default credentials in production

### System Configuration

Create config.yaml:
```yaml
system:
  name: "MARK-B.L.U. Production"
  max_agents: 100
  
security:
  badge_update_interval: 300  # 5 minutes
  quantum_circuit_qubits: 16
  entangling_layers: 3
  encryption: "AES-256-CBC"
  
database:
  path: "data/system.db"
  backup_enabled: true
  backup_interval: 3600  # 1 hour
```

---

## Usage

### Starting the System

Web Dashboard (Recommended):
```bash
streamlit run web_dashboard.py --server.port 8501
```

Access at: http://localhost:8501

### Creating Agents

```python
from agent_system.agent_identity import Agent
from agent_system.database_manager import IdentityDatabase

# Initialize database
db = IdentityDatabase("data/system.db")

# Create agent
agent = Agent("AGENT-001")

# Generate identity for timeslot 1
identity = agent.generate_identity(timeslot=1)

# Store in database
db.store_identity(identity)

print(f"Agent {identity.serial} created")
print(f"Badge: {identity.badge.hex()[:16]}...")
```

### Secure Communication

```python
from agent_system.secure_communication import SecureSystemCommunication

# Initialize communication layer
comm = SecureSystemCommunication(database)

# Send encrypted message
success = comm.send_secure_message(
    sender_serial="AGENT-001",
    receiver_serial="AGENT-002",
    message="Status: Operational"
)
```

---

## API Reference

### Agent Identity API

Agent(serial: str)
- generate_identity(timeslot: int) -> AgentIdentity
- get_current_identity() -> AgentIdentity
- get_identity_history() -> List[AgentIdentity]

AgentIdentity
- serial: str - Agent unique identifier
- badge: bytes - Quantum-derived identity badge (16 bytes)
- timeslot: int - Time period identifier
- timestamp: str - ISO format creation time

### Database API

IdentityDatabase(db_path: str)
- store_identity(identity: AgentIdentity)
- get_identity(serial: str, timeslot: int) -> AgentIdentity
- get_current_identity(serial: str) -> AgentIdentity
- log_communication(...)
- get_recent_communications(limit: int) -> List

AdminAuth(db_path: str)
- create_admin(username: str, password: str)
- verify_admin(username: str, password: str) -> bool
- admin_exists(username: str) -> bool

### Encryption API

SecureChannel(database: IdentityDatabase)
- encrypt_message(message: str, identity: AgentIdentity) -> (bytes, bytes)
- decrypt_message(ciphertext: bytes, iv: bytes, identity: AgentIdentity) -> str

---

## Security

### Authentication

Admin login uses:
- SHA-256 password hashing
- Random 32-byte salt per account
- Session-based authentication in web dashboard
- Secure password storage (never plaintext)

Default credentials:
- Username: gennrow@135
- Password: gennrow@135

Change in production using AdminAuth.create_admin()

### Encryption

All inter-agent messages use:
- Algorithm: AES-256-CBC
- Key derivation: SHA-256 hash of quantum badge
- IV: Random 16 bytes per message
- Padding: PKCS7

Security features:
- Quantum-derived keys (impossible to predict)
- Rotating identities (time-based badges)
- Message authentication
- Replay attack prevention (timeslot validation)

### Best Practices

1. Change default credentials before production use
2. Backup database regularly (data/*.db files)
3. Use HTTPS for web dashboard in production
4. Rotate admin passwords periodically
5. Monitor security logs for unauthorized access attempts
6. Update dependencies regularly for security patches

---

## Troubleshooting

### Common Issues

1. Web Dashboard Won't Start
```bash
# Port already in use
streamlit run web_dashboard.py --server.port 8502

# Module not found
pip install -r requirements.txt
```

2. Login Fails with Correct Credentials
```python
# Reset admin password
from agent_system.database_manager import AdminAuth
auth = AdminAuth("data/system.db")
auth.create_admin("gennrow@135", "gennrow@135")
```

3. Database Locked Error
```bash
# Close all connections and delete lock files
rm data/system.db-wal data/system.db-shm
streamlit run web_dashboard.py
```

4. Quantum Circuit Errors
```bash
# Update Qiskit
pip install --upgrade qiskit
python -c "import qiskit; print(qiskit.__version__)"
```

### Performance Optimization

For large systems (100+ agents):
- Pre-generate identities for multiple timeslots
- Create database indexes on serial and timestamp columns
- Use connection pooling for high-volume operations

---

## License

MIT License - see LICENSE file for details

---

## Contact

- GitHub: https://github.com/GENORROW/MARK-B.L.U.
- Issues: https://github.com/GENORROW/MARK-B.L.U./issues

---

## Changelog

### v1.0.0 (2025-10-09)
- Initial release
- Quantum identity generation
- AES-256 encryption
- Web dashboard with admin login
- SQLite database
- Complete documentation

---

MARK-B.L.U. - Secure AI Agent Identity & Monitoring System
