import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import secrets, hashlib
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
from quantum_hash.hash_core import quantum_hash_function

@dataclass
class AgentIdentity:
    serial: str
    timeslot: int
    timestamp: datetime
    qrng_seed: bytes
    badge: bytes
    def to_dict(self):
        return {'serial': self.serial, 'timeslot': self.timeslot, 'timestamp': self.timestamp.isoformat(), 'qrng_seed': self.qrng_seed.hex(), 'badge': self.badge.hex()}

class Agent:
    def __init__(self, serial: str, base_seed=None):
        self.serial = serial
        self.base_seed = base_seed or secrets.token_bytes(32)
        self.identity_history = []
    def generate_identity(self, timeslot: int):
        qrng_seed = secrets.token_bytes(32)
        hash_input = self.serial.encode('utf-8').ljust(8, b'\x00')[:8] + timeslot.to_bytes(8, 'big') + qrng_seed[:16]
        badge = quantum_hash_function(hash_input)
        identity = AgentIdentity(self.serial, timeslot, datetime.now(), qrng_seed, badge)
        self.identity_history.append(identity)
        return identity
    def get_current_identity(self):
        return self.identity_history[-1] if self.identity_history else None

class AgentSystem:
    def __init__(self, num_agents=40, system_id='MARK-BLU-SYSTEM-001'):
        self.system_id = system_id
        self.num_agents = num_agents
        self.agents = {}
        self.current_global_timeslot = 0
        for i in range(num_agents):
            serial = f'AGENT-{system_id}-{i+1:03d}'
            self.agents[serial] = Agent(serial)
    def advance_timeslot(self):
        self.current_global_timeslot += 1
        print(f'[*] Advancing to timeslot {self.current_global_timeslot}')
        for agent in self.agents.values():
            agent.generate_identity(self.current_global_timeslot)
        print(f'[] All agent identities updated')
        return self.current_global_timeslot
    def get_agent(self, serial):
        return self.agents.get(serial)
    def get_all_current_identities(self):
        return [a.get_current_identity() for a in self.agents.values() if a.get_current_identity()]
    def get_system_status(self):
        return {'system_id': self.system_id, 'num_agents': self.num_agents, 'current_timeslot': self.current_global_timeslot}
