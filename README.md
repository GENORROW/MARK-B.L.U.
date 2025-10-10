# MARK-B.L.U. Professional System# MARK-B.L.U. - AI Agent Identity & Monitoring System# MARK-B.L.U. 1.0: Part-1: The Hashing Mechanism



**Multi-Agent Badge-based Location-independent Unified System**



A professional quantum-secured agent identity and communication verification system.## Table of Contents## Overview



---1. [Overview](#overview)



## System Overview2. [System Architecture](#system-architecture)The MARK-B.L.U. Architecture is quantum encryption framework built using parameterized quantum circuits. It simulates a hash mechanism based on quantum circuit behavior, to safeguard autonomous & AI Infrastructure.



MARK-B.L.U. provides a secure, quantum-based identity management system for autonomous agents with:3. [Features](#features)



- **Quantum Badge Generation**: 16-qubit quantum circuits (Qiskit)4. [Installation](#installation)This mechanism demonstrates a first-step implementation that maps classical input data to quantum parameters, extracts measurement-based signatures, and secures agent identity & output communication logs.

- **AES-256-CBC Encryption**: Quantum-derived encryption keys

- **Badge Rotation**: Time-based identity rotation (5-minute timeslots)5. [Configuration](#configuration)

- **Centralized Verification**: Admin can verify any communication retroactively

- **Database Tracking**: SQLite-based identity and communication logging6. [Usage](#usage)## Features



---7. [API Reference](#api-reference)



## Quick Start8. [Security](#security)- Parameterized quantum circuit with entangling layers



### Installation9. [Troubleshooting](#troubleshooting)- Input encoding into continuous quantum gate parameters



```bash- Statevector-based computation

pip install qiskit streamlit pandas cryptography

```---- Tests for entropy, collisions, avalanche effect, and bit independence



### Run Dashboard



```bash## Overview## Installation

cd MARK-BLU

streamlit run web_dashboard_professional.py

```

MARK-B.L.U. (Multi-Agent Resource Keeper - Blockchain Leveraged Utility) is an advanced AI agent identity generation and monitoring system that provides:### Requirements

### Login



- **Username**: `genorrow@135`

- **Password**: `genorrow@135`- Quantum-based identity generation for AI agents- Python 3.9+



### Use- AES-256 encrypted communication between agents- Qiskit



1. **Live Simulation** tab - Run step-by-step demonstration- Real-time monitoring and analytics- NumPy

2. **Analytics** tab - View statistics and metrics

- Centralized database with complete audit trails

---

- Web-based admin dashboard for system management### Setup

## Architecture



### Core Components

### Key CapabilitiesClone the repo:

1. **Agent Identity System** - Quantum badge generation and management

2. **Secure Communication** - AES-256-CBC encryption

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
