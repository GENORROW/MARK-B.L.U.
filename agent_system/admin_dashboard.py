# agent_system/admin_dashboard.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import getpass
from datetime import datetime
from typing import Optional
from agent_system.drone_identity import DroneFleet, DroneAgent
from agent_system.database_manager import IdentityDatabase
from agent_system.secure_communication import SecureFleetCommunication


class AdminDashboard:
    """Command-line admin interface for MARK-B.L.U. system."""
    
    def __init__(self):
        """Initialize the admin dashboard."""
        self.db = IdentityDatabase("data/mark_blu_production.db")
        self.fleet: Optional[DroneFleet] = None
        self.fleet_comm: Optional[SecureFleetCommunication] = None
        self.authenticated = False
        self.current_admin = None
    
    def authenticate(self) -> bool:
        """Authenticate admin user."""
        print("\n" + "="*60)
        print("  MARK-B.L.U. ADMIN DASHBOARD - AUTHENTICATION REQUIRED")
        print("="*60)
        
        # Check if any admins exist
        admins = self.db.auth.list_admins()
        if not admins:
            print("\n[!] No admin users found. Creating default admin...")
            username = input("Enter admin username: ").strip()
            password = getpass.getpass("Enter admin password: ")
            
            if self.db.auth.create_admin(username, password):
                print(f"[✓] Admin user '{username}' created successfully")
            else:
                print("[✗] Failed to create admin user")
                return False
        
        # Authenticate
        max_attempts = 3
        for attempt in range(max_attempts):
            username = input("\nUsername: ").strip()
            password = getpass.getpass("Password: ")
            
            if self.db.auth.verify_admin(username, password):
                self.authenticated = True
                self.current_admin = username
                print(f"\n[✓] Authentication successful. Welcome, {username}!")
                return True
            else:
                remaining = max_attempts - attempt - 1
                if remaining > 0:
                    print(f"[✗] Authentication failed. {remaining} attempts remaining.")
                else:
                    print("[✗] Authentication failed. Access denied.")
        
        return False
    
    def display_main_menu(self):
        """Display the main menu."""
        print("\n" + "="*60)
        print(f"  MARK-B.L.U. ADMIN DASHBOARD | User: {self.current_admin}")
        print("="*60)
        print("\n[1] Fleet Management")
        print("[2] Identity Management")
        print("[3] Communication Logs")
        print("[4] Database Statistics")
        print("[5] System Administration")
        print("[0] Logout & Exit")
        print("-"*60)
    
    def fleet_management_menu(self):
        """Fleet management submenu."""
        while True:
            print("\n" + "="*60)
            print("  FLEET MANAGEMENT")
            print("="*60)
            print("\n[1] Initialize New Fleet")
            print("[2] View Fleet Status")
            print("[3] Advance Timeslot (Generate New Identities)")
            print("[4] Simulate Multiple Timeslots")
            print("[5] List All Drones")
            print("[0] Back to Main Menu")
            print("-"*60)
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "1":
                self.initialize_fleet()
            elif choice == "2":
                self.view_fleet_status()
            elif choice == "3":
                self.advance_timeslot()
            elif choice == "4":
                self.simulate_timeslots()
            elif choice == "5":
                self.list_all_drones()
            elif choice == "0":
                break
            else:
                print("[✗] Invalid option")
    
    def initialize_fleet(self):
        """Initialize a new fleet."""
        print("\n--- Initialize New Fleet ---")
        
        try:
            num_drones = int(input("Number of drones (default 40): ").strip() or "40")
            fleet_id = input("Fleet ID (default MARK-BLU-FLEET-001): ").strip() or "MARK-BLU-FLEET-001"
            
            self.fleet = DroneFleet(num_drones=num_drones, fleet_id=fleet_id)
            self.fleet_comm = SecureFleetCommunication(self.db)
            
            print(f"\n[✓] Fleet '{fleet_id}' initialized with {num_drones} drones")
            
            # Generate initial identities
            if input("Generate initial identities for timeslot 1? (y/n): ").lower() == 'y':
                self.fleet.advance_timeslot()
                
                # Store all identities in database
                identities = self.fleet.get_all_current_identities()
                success, failed = self.db.store_multiple_identities(identities)
                print(f"[✓] Stored {success} identities in database")
                
                # Update fleet metadata
                self.db.update_fleet_metadata(fleet_id, num_drones, 1)
        
        except ValueError:
            print("[✗] Invalid input")
    
    def view_fleet_status(self):
        """View current fleet status."""
        print("\n--- Fleet Status ---")
        
        if not self.fleet:
            print("[!] No fleet initialized. Please initialize a fleet first.")
            return
        
        status = self.fleet.get_fleet_status()
        
        print(f"\nFleet ID: {status['fleet_id']}")
        print(f"Number of Drones: {status['num_drones']}")
        print(f"Current Timeslot: {status['current_timeslot']}")
        print(f"Fleet Started: {status['fleet_start_time']}")
        print(f"Runtime: {status['runtime_seconds']:.2f} seconds")
        print(f"Total Identities Generated: {status['total_identities_generated']}")
    
    def advance_timeslot(self):
        """Advance to next timeslot."""
        print("\n--- Advance Timeslot ---")
        
        if not self.fleet:
            print("[!] No fleet initialized.")
            return
        
        print(f"[*] Current timeslot: {self.fleet.current_global_timeslot}")
        if input("Advance to next timeslot? (y/n): ").lower() == 'y':
            new_timeslot = self.fleet.advance_timeslot()
            
            # Store new identities
            identities = self.fleet.get_all_current_identities()
            success, failed = self.db.store_multiple_identities(identities)
            
            print(f"[✓] Advanced to timeslot {new_timeslot}")
            print(f"[✓] Stored {success} new identities")
            
            # Update fleet metadata
            self.db.update_fleet_metadata(
                self.fleet.fleet_id, 
                self.fleet.num_drones, 
                new_timeslot
            )
    
    def simulate_timeslots(self):
        """Simulate multiple timeslots."""
        print("\n--- Simulate Multiple Timeslots ---")
        
        if not self.fleet:
            print("[!] No fleet initialized.")
            return
        
        try:
            num_slots = int(input("Number of timeslots to simulate: ").strip())
            
            for i in range(num_slots):
                new_timeslot = self.fleet.advance_timeslot()
                identities = self.fleet.get_all_current_identities()
                success, failed = self.db.store_multiple_identities(identities)
                
                self.db.update_fleet_metadata(
                    self.fleet.fleet_id,
                    self.fleet.num_drones,
                    new_timeslot
                )
            
            print(f"\n[✓] Simulation complete. Now at timeslot {self.fleet.current_global_timeslot}")
        
        except ValueError:
            print("[✗] Invalid input")
    
    def list_all_drones(self):
        """List all drones in fleet."""
        print("\n--- All Drones ---")
        
        if not self.fleet:
            print("[!] No fleet initialized.")
            return
        
        print(f"\nTotal Drones: {len(self.fleet.drones)}")
        print("-"*60)
        
        for i, (serial, drone) in enumerate(self.fleet.drones.items(), 1):
            current_id = drone.get_current_identity()
            if current_id:
                print(f"{i}. {serial}")
                print(f"   Timeslot: {current_id.timeslot}")
                print(f"   Badge: {current_id.badge.hex()[:32]}...")
            else:
                print(f"{i}. {serial} (No identity generated)")
            
            if i >= 10 and i < len(self.fleet.drones):
                if input("\nShow more? (y/n): ").lower() != 'y':
                    print(f"... and {len(self.fleet.drones) - i} more drones")
                    break
    
    def identity_management_menu(self):
        """Identity management submenu."""
        while True:
            print("\n" + "="*60)
            print("  IDENTITY MANAGEMENT")
            print("="*60)
            print("\n[1] Query Identity by Serial & Timeslot")
            print("[2] View All Identities for Timeslot")
            print("[3] Export Identities to JSON")
            print("[4] View Drone Identity History")
            print("[0] Back to Main Menu")
            print("-"*60)
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "1":
                self.query_identity()
            elif choice == "2":
                self.view_timeslot_identities()
            elif choice == "3":
                self.export_identities()
            elif choice == "4":
                self.view_identity_history()
            elif choice == "0":
                break
            else:
                print("[✗] Invalid option")
    
    def query_identity(self):
        """Query specific identity."""
        print("\n--- Query Identity ---")
        
        serial = input("Drone serial: ").strip()
        try:
            timeslot = int(input("Timeslot: ").strip())
            
            identity = self.db.get_identity(serial, timeslot)
            
            if identity:
                print(f"\n[✓] Identity found:")
                print(f"Serial: {identity.serial}")
                print(f"Timeslot: {identity.timeslot}")
                print(f"Timestamp: {identity.timestamp}")
                print(f"QRNG Seed: {identity.qrng_seed.hex()[:32]}...")
                print(f"Badge: {identity.badge.hex()}")
            else:
                print("[!] Identity not found")
        
        except ValueError:
            print("[✗] Invalid timeslot number")
    
    def view_timeslot_identities(self):
        """View all identities for a timeslot."""
        print("\n--- Timeslot Identities ---")
        
        try:
            timeslot = int(input("Timeslot number: ").strip())
            identities = self.db.get_all_identities_for_timeslot(timeslot)
            
            if identities:
                print(f"\n[✓] Found {len(identities)} identities for timeslot {timeslot}")
                print("-"*60)
                
                for i, identity in enumerate(identities[:10], 1):
                    print(f"{i}. {identity.serial}: {identity.badge.hex()[:32]}...")
                
                if len(identities) > 10:
                    print(f"... and {len(identities) - 10} more identities")
            else:
                print(f"[!] No identities found for timeslot {timeslot}")
        
        except ValueError:
            print("[✗] Invalid timeslot number")
    
    def export_identities(self):
        """Export identities to JSON."""
        print("\n--- Export Identities ---")
        
        output_file = input("Output filename (default: identities_export.json): ").strip()
        output_file = output_file or "identities_export.json"
        
        timeslot_input = input("Export specific timeslot? (leave blank for all): ").strip()
        timeslot = int(timeslot_input) if timeslot_input else None
        
        try:
            self.db.export_to_json(f"data/{output_file}", timeslot)
        except Exception as e:
            print(f"[✗] Export failed: {e}")
    
    def view_identity_history(self):
        """View identity history for a drone."""
        print("\n--- Drone Identity History ---")
        
        serial = input("Drone serial: ").strip()
        
        if self.fleet and serial in self.fleet.drones:
            drone = self.fleet.drones[serial]
            history = drone.identity_history
            
            if history:
                print(f"\n[✓] Identity history for {serial}:")
                print(f"Total identities: {len(history)}")
                print("-"*60)
                
                for identity in history:
                    print(f"Timeslot {identity.timeslot}: {identity.badge.hex()[:32]}... "
                          f"({identity.timestamp.strftime('%Y-%m-%d %H:%M:%S')})")
            else:
                print(f"[!] No identity history for {serial}")
        else:
            print("[!] Drone not found in current fleet")
    
    def communication_logs_menu(self):
        """Communication logs submenu."""
        while True:
            print("\n" + "="*60)
            print("  COMMUNICATION LOGS")
            print("="*60)
            print("\n[1] View Recent Communications")
            print("[2] Filter by Sender")
            print("[3] Filter by Receiver")
            print("[4] Test Communication Between Drones")
            print("[0] Back to Main Menu")
            print("-"*60)
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "1":
                self.view_recent_communications()
            elif choice == "2":
                self.filter_by_sender()
            elif choice == "3":
                self.filter_by_receiver()
            elif choice == "4":
                self.test_communication()
            elif choice == "0":
                break
            else:
                print("[✗] Invalid option")
    
    def view_recent_communications(self):
        """View recent communication logs."""
        print("\n--- Recent Communications ---")
        
        try:
            limit = int(input("Number of logs to display (default 20): ").strip() or "20")
            logs = self.db.get_communication_logs(limit=limit)
            
            if logs:
                print(f"\n[✓] Displaying {len(logs)} recent communications:")
                print("-"*60)
                
                for log in logs:
                    print(f"[{log['timestamp']}] {log['sender_serial']} -> {log['receiver_serial']}")
                    print(f"  Timeslots: S{log['sender_timeslot']} -> R{log['receiver_timeslot']}")
                    print(f"  Hash: {log['message_hash'][:16]}... | Verified: {log['verified']}")
                    print()
            else:
                print("[!] No communications logged")
        
        except ValueError:
            print("[✗] Invalid input")
    
    def filter_by_sender(self):
        """Filter logs by sender."""
        print("\n--- Filter by Sender ---")
        
        sender = input("Sender serial: ").strip()
        logs = self.db.get_communication_logs(limit=50, sender=sender)
        
        if logs:
            print(f"\n[✓] Found {len(logs)} communications from {sender}:")
            for log in logs:
                print(f"  -> {log['receiver_serial']} at {log['timestamp']}")
        else:
            print(f"[!] No communications from {sender}")
    
    def filter_by_receiver(self):
        """Filter logs by receiver."""
        print("\n--- Filter by Receiver ---")
        
        receiver = input("Receiver serial: ").strip()
        logs = self.db.get_communication_logs(limit=50, receiver=receiver)
        
        if logs:
            print(f"\n[✓] Found {len(logs)} communications to {receiver}:")
            for log in logs:
                print(f"  {log['sender_serial']} -> at {log['timestamp']}")
        else:
            print(f"[!] No communications to {receiver}")
    
    def test_communication(self):
        """Test communication between drones."""
        print("\n--- Test Drone Communication ---")
        
        if not self.fleet or not self.fleet_comm:
            print("[!] Fleet not initialized")
            return
        
        print("\nAvailable drones:")
        drone_list = list(self.fleet.drones.keys())[:10]
        for i, serial in enumerate(drone_list, 1):
            print(f"{i}. {serial}")
        
        try:
            sender_idx = int(input("\nSelect sender (number): ")) - 1
            receiver_idx = int(input("Select receiver (number): ")) - 1
            message = input("Message to send: ").strip()
            
            sender = self.fleet.drones[drone_list[sender_idx]]
            receiver = self.fleet.drones[drone_list[receiver_idx]]
            
            if self.fleet_comm.channel.send_message(sender, receiver, message):
                print("\n[✓] Communication successful!")
            else:
                print("\n[✗] Communication failed")
        
        except (ValueError, IndexError):
            print("[✗] Invalid selection")
    
    def database_statistics(self):
        """Display database statistics."""
        print("\n--- Database Statistics ---")
        
        stats = self.db.get_database_stats()
        
        print(f"\nDatabase: {stats['database_path']}")
        print("-"*60)
        print(f"Total Identities: {stats['total_identities']}")
        print(f"Unique Drones: {stats['unique_drones']}")
        print(f"Total Communications: {stats['total_communications']}")
        print(f"Maximum Timeslot: {stats['max_timeslot']}")
        print(f"Admin Users: {stats['total_admins']}")
        
        input("\nPress Enter to continue...")
    
    def system_administration(self):
        """System administration submenu."""
        while True:
            print("\n" + "="*60)
            print("  SYSTEM ADMINISTRATION")
            print("="*60)
            print("\n[1] List Admin Users")
            print("[2] Create New Admin User")
            print("[3] Change Password (Not Implemented)")
            print("[4] System Information")
            print("[0] Back to Main Menu")
            print("-"*60)
            
            choice = input("\nSelect option: ").strip()
            
            if choice == "1":
                self.list_admins()
            elif choice == "2":
                self.create_admin_user()
            elif choice == "3":
                print("[!] Feature not implemented yet")
            elif choice == "4":
                self.system_information()
            elif choice == "0":
                break
            else:
                print("[✗] Invalid option")
    
    def list_admins(self):
        """List all admin users."""
        print("\n--- Admin Users ---")
        
        admins = self.db.auth.list_admins()
        
        if admins:
            print(f"\n[✓] Total admin users: {len(admins)}")
            print("-"*60)
            
            for admin in admins:
                print(f"ID: {admin['admin_id']} | Username: {admin['username']}")
                print(f"  Created: {admin['created_at']}")
                print(f"  Last Login: {admin['last_login'] or 'Never'}")
                print()
        else:
            print("[!] No admin users found")
    
    def create_admin_user(self):
        """Create new admin user."""
        print("\n--- Create New Admin ---")
        
        username = input("Username: ").strip()
        password = getpass.getpass("Password: ")
        confirm = getpass.getpass("Confirm password: ")
        
        if password != confirm:
            print("[✗] Passwords do not match")
            return
        
        if self.db.auth.create_admin(username, password):
            print(f"[✓] Admin user '{username}' created successfully")
        else:
            print("[✗] Failed to create admin user (username may already exist)")
    
    def system_information(self):
        """Display system information."""
        print("\n--- System Information ---")
        
        print(f"\nMARK-B.L.U. Version: 1.0.0")
        print(f"System: Quantum Hash-Based Agent Identity System")
        print(f"Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Logged in as: {self.current_admin}")
        
        if self.fleet:
            print(f"\nActive Fleet: {self.fleet.fleet_id}")
            print(f"Fleet Drones: {self.fleet.num_drones}")
            print(f"Current Timeslot: {self.fleet.current_global_timeslot}")
        else:
            print(f"\nNo active fleet")
        
        input("\nPress Enter to continue...")
    
    def run(self):
        """Run the admin dashboard."""
        # Authenticate
        if not self.authenticate():
            print("\n[✗] Authentication failed. Exiting...")
            return
        
        # Main loop
        while True:
            self.display_main_menu()
            choice = input("\nSelect option: ").strip()
            
            if choice == "1":
                self.fleet_management_menu()
            elif choice == "2":
                self.identity_management_menu()
            elif choice == "3":
                self.communication_logs_menu()
            elif choice == "4":
                self.database_statistics()
            elif choice == "5":
                self.system_administration()
            elif choice == "0":
                print(f"\n[*] Logging out {self.current_admin}...")
                print("[✓] Goodbye!")
                break
            else:
                print("[✗] Invalid option. Please try again.")


def main():
    """Main entry point."""
    dashboard = AdminDashboard()
    dashboard.run()


if __name__ == "__main__":
    main()
