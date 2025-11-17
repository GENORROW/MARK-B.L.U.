# agent_system/secure_communication.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import hashlib
import secrets
from typing import Optional, Tuple
from datetime import datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from agent_system.agent_identity import AgentIdentity, Agent
from agent_system.database_manager import IdentityDatabase


class SecureChannel:
    """Handles encrypted communication between agents using quantum badges."""
    
    def __init__(self, database: Optional[IdentityDatabase] = None):
        self.database = database
        self.backend = default_backend()
    
    def _derive_key_from_badge(self, badge: bytes) -> bytes:
        return hashlib.sha256(badge).digest()
    
    def encrypt_message(self, message: str, sender_identity: AgentIdentity) -> Tuple[bytes, bytes]:
        key = self._derive_key_from_badge(sender_identity.badge)
        iv = secrets.token_bytes(16)
        message_bytes = message.encode('utf-8')
        
        padder = padding.PKCS7(128).padder()
        padded_message = padder.update(message_bytes) + padder.finalize()
        
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=self.backend
        )
        encryptor = cipher.encryptor()
        encrypted_message = encryptor.update(padded_message) + encryptor.finalize()
        
        return encrypted_message, iv
    
    def decrypt_message(self, encrypted_message: bytes, iv: bytes, 
                       receiver_identity: AgentIdentity) -> Optional[str]:
        try:
            key = self._derive_key_from_badge(receiver_identity.badge)
            
            cipher = Cipher(
                algorithms.AES(key),
                modes.CBC(iv),
                backend=self.backend
            )
            decryptor = cipher.decryptor()
            padded_message = decryptor.update(encrypted_message) + decryptor.finalize()
            
            unpadder = padding.PKCS7(128).unpadder()
            message_bytes = unpadder.update(padded_message) + unpadder.finalize()
            
            return message_bytes.decode('utf-8')
        
        except Exception as e:
            print(f"[✗] Decryption failed: {e}")
            return None
    
    def send_message(self, sender: Agent, receiver: Agent, 
                    message: str, verify: bool = True) -> bool:
        sender_identity = sender.get_current_identity()
        receiver_identity = receiver.get_current_identity()
        
        if not sender_identity or not receiver_identity:
            print("[✗] Both sender and receiver must have current identities")
            return False
        
        print(f"\n[*] Sending encrypted message from {sender.serial} to {receiver.serial}")
        print(f"    Sender timeslot: {sender_identity.timeslot}")
        print(f"    Receiver timeslot: {receiver_identity.timeslot}")
        
        encrypted_message, iv = self.encrypt_message(message, sender_identity)
        
        print(f"[✓] Message encrypted: {len(encrypted_message)} bytes")
        print(f"    Original message: '{message}'")
        print(f"    Encrypted (hex): {encrypted_message.hex()[:64]}...")
        
        combined_data = iv + encrypted_message
        
        verified = False
        if self.database:
            log_id = self.database.log_communication(
                sender_serial=sender.serial,
                receiver_serial=receiver.serial,
                sender_timeslot=sender_identity.timeslot,
                receiver_timeslot=receiver_identity.timeslot,
                encrypted_message=combined_data,
                verified=False
            )
            print(f"[✓] Communication logged (ID: {log_id})")
        
        if verify:
            decrypted = self.decrypt_message(encrypted_message, iv, sender_identity)
            if decrypted == message:
                print(f"[✓] Verification successful: Message decrypted correctly")
                verified = True
            else:
                print(f"[✗] Verification failed: Decryption mismatch")
        
        return True
    
    def intercept_message(self, encrypted_message: bytes, iv: bytes, 
                         attacker_identity: AgentIdentity) -> bool:
        print(f"\n[!] Simulating interception attack by {attacker_identity.serial}")
        
        decrypted = self.decrypt_message(encrypted_message, iv, attacker_identity)
        
        if decrypted:
            print(f"[✗] SECURITY BREACH: Attacker successfully decrypted message!")
            return True
        else:
            print(f"[✓] Attack failed: Wrong badge cannot decrypt message")
            return False


class SecureFleetCommunication:
    """Manages secure communication for an entire fleet."""
    
    def __init__(self, database: Optional[IdentityDatabase] = None):
        self.channel = SecureChannel(database)
        self.database = database
    
    def broadcast_message(self, sender: Agent, receivers: list, 
                         message: str) -> Tuple[int, int]:
        print(f"\n[*] Broadcasting message from {sender.serial} to {len(receivers)} agents")
        
        successful = 0
        failed = 0
        
        for receiver in receivers:
            if self.channel.send_message(sender, receiver, message, verify=False):
                successful += 1
            else:
                failed += 1
        
        print(f"\n[✓] Broadcast complete: {successful} successful, {failed} failed")
        return successful, failed
    
    def peer_to_peer_exchange(self, agent1: Agent, agent2: Agent) -> bool:
        print(f"\n=== Peer-to-Peer Communication ===")
        
        msg1 = f"Hello from {agent1.serial}. Status: Operational"
        success1 = self.channel.send_message(agent1, agent2, msg1)
        
        msg2 = f"Acknowledged by {agent2.serial}. Standing by"
        success2 = self.channel.send_message(agent2, agent1, msg2)
        
        return success1 and success2
    
    def demonstrate_security(self, sender: Agent, legitimate_receiver: Agent,
                           attacker: Agent):
        print(f"\n=== Security Demonstration ===")
        
        sender_identity = sender.get_current_identity()
        attacker_identity = attacker.get_current_identity()
        
        if not sender_identity or not attacker_identity:
            print("[✗] All agents must have current identities")
            return
        
        secret_message = "CLASSIFIED: Mission coordinates are 45.5231, -122.6765"
        encrypted_message, iv = self.channel.encrypt_message(secret_message, sender_identity)
        
        print(f"[*] Sensitive message sent from {sender.serial}")
        print(f"    Message: '{secret_message}'")
        
        print(f"\n[*] Legitimate receiver ({legitimate_receiver.serial}) attempting decryption...")
        receiver_identity = legitimate_receiver.get_current_identity()
        if receiver_identity:
            decrypted = self.channel.decrypt_message(encrypted_message, iv, sender_identity)
            if decrypted:
                print(f"[✓] Successfully decrypted: '{decrypted}'")
        
        self.channel.intercept_message(encrypted_message, iv, attacker_identity)


def demo_secure_communication():
    print("=== Secure Communication Demo ===\n")
    
    db = IdentityDatabase("data/demo_secure_comm.db")
    channel = SecureChannel(db)
    
    print("[*] Initializing agents...")
    agent1 = Agent("SECURE-AGENT-001")
    agent2 = Agent("SECURE-AGENT-002")
    agent3 = Agent("ATTACKER-AGENT-003")
    
    for agent in [agent1, agent2, agent3]:
        identity = agent.generate_identity(1)
        db.store_identity(identity)
        print(f"[✓] {agent.serial} identity generated")
    
    print("\n--- Basic Encrypted Communication ---")
    message = "Mission update: Proceed to waypoint Alpha"
    channel.send_message(agent1, agent2, message)
    
    print("\n--- Peer-to-Peer Communication ---")
    fleet_comm = SecureFleetCommunication(db)
    fleet_comm.peer_to_peer_exchange(agent1, agent2)
    
    print("\n--- Security Test ---")
    fleet_comm.demonstrate_security(agent1, agent2, agent3)
    
    print("\n--- Communication Logs ---")
    logs = db.get_communication_logs(limit=10)
    print(f"[*] Total logged communications: {len(logs)}")
    for log in logs:
        print(f"    {log['sender_serial']} -> {log['receiver_serial']} "
              f"at {log['timestamp']} (verified: {log['verified']})")
    
    print("\n[✓] Secure communication demo complete!")


if __name__ == "__main__":
    demo_secure_communication()
