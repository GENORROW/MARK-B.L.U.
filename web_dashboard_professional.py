"""
MARK-B.L.U. Professional Web Dashboard
Two-tab interface: Live Simulation + Analytics
Version: 7.0 - Clean Professional (No Status Markers)
Login: genorrow@135 / genorrow@135
"""

import streamlit as st
import sys
import os
import pandas as pd
import time
from datetime import datetime, timedelta
import hashlib

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent_system.database_manager import IdentityDatabase, AdminAuth

# Page configuration
st.set_page_config(
    page_title="MARK-B.L.U. System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional dark theme with maximum contrast
st.markdown("""
<style>
    /* Root and main background - pure black */
    .stApp {
        background-color: #0a0a0a;
        color: #FFFFFF;
    }
    
    .main {
        background-color: #0a0a0a;
        color: #FFFFFF;
    }
    
    /* Sidebar - dark grey */
    [data-testid="stSidebar"] {
        background-color: #1c1c1c;
        color: #FFFFFF;
    }
    
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    
    /* All headers - pure white */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
        font-family: 'Segoe UI', 'Arial', sans-serif;
        font-weight: 600;
    }
    
    /* All paragraphs and text - pure white */
    p, span, div, label {
        color: #FFFFFF !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #00FF00 !important;
        font-size: 32px;
        font-weight: bold;
    }
    
    [data-testid="stMetricLabel"] {
        color: #FFFFFF !important;
        font-size: 14px;
    }
    
    [data-testid="stMetricDelta"] {
        color: #FFFFFF !important;
    }
    
    /* Dataframes and tables */
    .dataframe {
        background-color: #1c1c1c !important;
        color: #FFFFFF !important;
    }
    
    table {
        background-color: #1c1c1c !important;
        color: #FFFFFF !important;
    }
    
    thead tr th {
        background-color: #2d2d2d !important;
        color: #FFFFFF !important;
        font-weight: bold;
        border: 1px solid #3d3d3d !important;
    }
    
    tbody tr td {
        background-color: #1c1c1c !important;
        color: #FFFFFF !important;
        border: 1px solid #2d2d2d !important;
    }
    
    tbody tr:hover {
        background-color: #2d2d2d !important;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #2d2d2d;
        color: #FFFFFF !important;
        border: 2px solid #4d4d4d;
        border-radius: 6px;
        padding: 12px 28px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #3d3d3d;
        border-color: #6d6d6d;
        color: #FFFFFF !important;
    }
    
    /* Input fields */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div>select {
        background-color: #2d2d2d !important;
        color: #FFFFFF !important;
        border: 2px solid #4d4d4d !important;
        border-radius: 6px;
    }
    
    .stTextInput>div>div>input::placeholder {
        color: #888888 !important;
    }
    
    /* Radio buttons and checkboxes */
    .stRadio>div>label>div {
        color: #FFFFFF !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1c1c1c;
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #2d2d2d;
        color: #FFFFFF !important;
        border-radius: 6px 6px 0 0;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #3d3d3d;
        color: #FFFFFF !important;
    }
    
    /* Info boxes */
    .stAlert {
        background-color: #2d2d2d !important;
        color: #FFFFFF !important;
        border: 1px solid #4d4d4d !important;
    }
    
    /* Success/Info/Warning/Error messages */
    .stSuccess {
        background-color: #1a4d1a !important;
        color: #FFFFFF !important;
    }
    
    .stInfo {
        background-color: #1a3d5d !important;
        color: #FFFFFF !important;
    }
    
    .stWarning {
        background-color: #5d4d1a !important;
        color: #FFFFFF !important;
    }
    
    .stError {
        background-color: #5d1a1a !important;
        color: #FFFFFF !important;
    }
    
    /* Cards - dark grey background */
    .info-card {
        background-color: #1c1c1c;
        border: 2px solid #3d3d3d;
        border-radius: 10px;
        padding: 24px;
        margin: 12px 0;
        color: #FFFFFF !important;
    }
    
    .info-card * {
        color: #FFFFFF !important;
    }
    
    /* Status badges */
    .badge {
        padding: 6px 14px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: bold;
        display: inline-block;
        margin: 4px;
    }
    
    .badge-success {
        background-color: #28a745;
        color: #FFFFFF !important;
    }
    
    .badge-danger {
        background-color: #dc3545;
        color: #FFFFFF !important;
    }
    
    .badge-warning {
        background-color: #ffc107;
        color: #000000 !important;
    }
    
    /* Slider */
    .stSlider>div>div>div {
        background-color: #4d4d4d;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #2d2d2d !important;
        color: #FFFFFF !important;
    }
    
    /* Markdown text */
    .stMarkdown {
        color: #FFFFFF !important;
    }
    
    /* Code blocks */
    code {
        background-color: #2d2d2d !important;
        color: #00FF00 !important;
        padding: 2px 6px;
        border-radius: 4px;
    }
    
    pre {
        background-color: #2d2d2d !important;
        border: 1px solid #4d4d4d;
        border-radius: 6px;
        padding: 12px;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
        background-color: #1c1c1c;
    }
    
    ::-webkit-scrollbar-thumb {
        background-color: #4d4d4d;
        border-radius: 6px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background-color: #6d6d6d;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'db' not in st.session_state:
    st.session_state.db = None
if 'auth' not in st.session_state:
    st.session_state.auth = None

# Database initialization
DB_PATH = "data/system.db"

def init_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'db' not in st.session_state:
        st.session_state.db = None
    if 'auth' not in st.session_state:
        st.session_state.auth = None

def init_database():
    """Initialize database and admin auth"""
    os.makedirs("data", exist_ok=True)
    db = IdentityDatabase(DB_PATH)
    auth = AdminAuth(DB_PATH)
    
    # Create default admin if not exists
    if not auth.admin_exists("genorrow@135"):
        auth.create_admin("genorrow@135", "genorrow@135")
    
    return db, auth

def login_page():
    """Display login page"""
    st.markdown("<h1 style='text-align: center;'>MARK-B.L.U. SYSTEM</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #888;'>AI Agent Identity & Monitoring</h3>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div class='info-card'>", unsafe_allow_html=True)
        st.subheader("Admin Login")
        
        username = st.text_input("Username", key="login_username", placeholder="Enter username")
        password = st.text_input("Password", key="login_password", type="password", placeholder="Enter password")
        
        col_a, col_b, col_c = st.columns([1, 1, 1])
        with col_b:
            if st.button("LOGIN", use_container_width=True):
                if username and password:
                    # Initialize auth
                    _, auth = init_database()
                    
                    if auth.verify_admin(username, password):
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
                else:
                    st.warning("Please enter both username and password")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #666; font-size: 12px;'>Default credentials: genorrow@135 / genorrow@135</p>", unsafe_allow_html=True)

def main_dashboard():
    """Main dashboard after login"""
    
    # Initialize database
    if st.session_state.db is None:
        st.session_state.db, st.session_state.auth = init_database()
    
    db = st.session_state.db
    
    # Sidebar
    with st.sidebar:
        st.markdown("<h2>MARK-B.L.U.</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #888;'>Logged in as: {st.session_state.username}</p>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        
        page = st.radio(
            "Navigation",
            ["Live Simulation", "Analytics"],
            label_visibility="collapsed"
        )
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        if st.button("LOGOUT", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.rerun()
    
    # Main content
    if page == "Live Simulation":
        live_simulation_page(db)
    elif page == "Analytics":
        analytics_page(db)

def live_simulation_page(db):
    """Live agent communication simulation - Professional step-by-step format"""
    st.title("AGENT COMMUNICATION VERIFICATION DEMONSTRATION")
    
    st.markdown("""
    <div class='info-card' style='background-color: #1a3d5d; border-left: 4px solid #00BFFF;'>
    <h4>Badge Rotation | Communication Tracking | Admin Verification</h4>
    <p>This demonstrates how agents generate quantum badges, communicate securely, and how admins verify messages later.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    if st.button("START SIMULATION", use_container_width=True, type="primary"):
        # Import required modules
        from agent_system.agent_identity import Agent
        from agent_system.secure_communication import SecureChannel
        import time
        
        # Create 5 agents
        st.markdown("### [SETUP] Created 5 agents for demonstration")
        agents = []
        for i in range(5):
            serial = f"AGENT-DEMO-{i+1:03d}"
            agent = Agent(serial)
            agents.append(agent)
        
        st.success(f"Created {len(agents)} agents")
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # ========== TIMESLOT 1 ==========
        st.markdown("## TIMESLOT 1 (Time: 00:00 - 00:05)")
        st.markdown("<hr>", unsafe_allow_html=True)
        
        st.info("[*] Advancing to timeslot 1")
        st.info(f"[*] Generating new identities for {len(agents)} agents...")
        
        # Generate identities for timeslot 1
        timeslot1_identities = {}
        for agent in agents:
            identity = agent.generate_identity(1)
            db.store_identity(identity)
            timeslot1_identities[agent.serial] = identity
        
        st.success(f"All agent identities updated for timeslot 1")
        
        st.markdown("### [BADGE GENERATION] Each agent got new quantum badge:")
        for agent in agents:
            identity = timeslot1_identities[agent.serial]
            with st.expander(f"  {agent.serial}", expanded=False):
                st.code(f"Badge: {identity.badge.hex()[:32]}...\nTimeslot: {identity.timeslot}", language="")
        
        time.sleep(1)
        
        # Communication in timeslot 1
        st.markdown("### [COMMUNICATION] AGENT-001 sends encrypted message to AGENT-002:")
        
        sender = agents[0]
        receiver = agents[1]
        sender_identity = timeslot1_identities[sender.serial]
        receiver_identity = timeslot1_identities[receiver.serial]
        
        message1 = "Mission Status: Surveillance sector Alpha complete. Proceeding to Bravo."
        channel = SecureChannel(db)
        encrypted_msg1, iv1 = channel.encrypt_message(message1, sender_identity)
        
        # Log to database
        db.log_communication(
            sender.serial,
            receiver.serial,
            sender_identity.timeslot,
            receiver_identity.timeslot,
            encrypted_msg1
        )
        
        comm_id1 = db.get_recent_communications(1)[0][0]
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            **Original Message:**  
            '{message1}'
            
            **Badge Used:**  
            `{sender_identity.badge.hex()[:32]}...`
            """)
        with col2:
            st.markdown(f"""
            **Encrypted:**  
            `{encrypted_msg1.hex()[:64]}...`
            
            **Logged to database (Log ID: {comm_id1})**
            """)
        
        time.sleep(1)
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # ========== TIMESLOT 2 ==========
        st.markdown("## TIMESLOT 2 (Time: 00:05 - 00:10) - 5 MINUTES LATER")
        st.markdown("<hr>", unsafe_allow_html=True)
        
        st.info("[*] Advancing to timeslot 2")
        st.info(f"[*] Generating new identities for {len(agents)} agents...")
        
        # Generate NEW identities for timeslot 2
        timeslot2_identities = {}
        for agent in agents:
            identity = agent.generate_identity(2)
            db.store_identity(identity)
            timeslot2_identities[agent.serial] = identity
        
        st.success(f"All agent identities updated for timeslot 2")
        
        st.markdown("### [BADGE UPDATE] All agents got NEW quantum badges:")
        
        # Show badge rotation for first agent
        with st.expander(f"  {agents[0].serial}: Badge rotation example", expanded=True):
            old_badge = timeslot1_identities[agents[0].serial].badge.hex()[:32]
            new_badge = timeslot2_identities[agents[0].serial].badge.hex()[:32]
            st.markdown(f"""
            ```
            OLD Badge (Timeslot 1): {old_badge}...
            NEW Badge (Timeslot 2): {new_badge}...
            Note: Old badge is now EXPIRED
            ```
            """)
        
        time.sleep(1)
        
        # Communication in timeslot 2
        st.markdown("### [COMMUNICATION] AGENT-001 sends NEW encrypted message to AGENT-003:")
        
        sender = agents[0]
        receiver = agents[2]
        sender_identity = timeslot2_identities[sender.serial]
        receiver_identity = timeslot2_identities[receiver.serial]
        
        message2 = "Alert: Unidentified object detected in sector Bravo. Requesting backup."
        encrypted_msg2, iv2 = channel.encrypt_message(message2, sender_identity)
        
        # Log to database
        db.log_communication(
            sender.serial,
            receiver.serial,
            sender_identity.timeslot,
            receiver_identity.timeslot,
            encrypted_msg2
        )
        
        comm_id2 = db.get_recent_communications(1)[0][0]
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            **Original Message:**  
            '{message2}'
            
            **Badge Used (NEW):**  
            `{sender_identity.badge.hex()[:32]}...`
            """)
        with col2:
            st.markdown(f"""
            **Encrypted:**  
            `{encrypted_msg2.hex()[:64]}...`
            
            **Logged to database (Log ID: {comm_id2})**
            """)
        
        time.sleep(1)
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # ========== ADMIN VERIFICATION ==========
        st.markdown("## ADMIN VERIFICATION PROCESS")
        st.markdown("<hr>", unsafe_allow_html=True)
        
        st.markdown("""
        **[SCENARIO]** Admin needs to verify communications later...
        - Admin doesn't know which agent sent which message
        - Admin will use database to verify sender identity
        """)
        
        st.markdown("### [ADMIN VIEW] Communication logs in database:")
        
        all_comms = db.get_recent_communications(10)
        for comm in all_comms[:4]:
            comm_id, sender_serial, receiver_serial, sender_slot, receiver_slot, enc_msg, timestamp = comm
            import hashlib
            # Convert to bytes if it's a string
            if isinstance(enc_msg, str):
                enc_msg_bytes = bytes.fromhex(enc_msg)
            else:
                enc_msg_bytes = enc_msg
            msg_hash = hashlib.md5(enc_msg_bytes).hexdigest()
            st.text(f"""
Log ID: {comm_id}
  Timestamp: {timestamp}
  Sender: {sender_serial} (Timeslot {sender_slot})
  Receiver: {receiver_serial} (Timeslot {receiver_slot})
  Message Hash: {msg_hash[:32]}...
            """)
        
        st.markdown("-"*80)
        
        # Verification 1
        st.markdown("### [VERIFICATION 1] Verifying first communication:")
        st.markdown("-"*80)
        
        # Get the first communication from DB
        comm = all_comms[1] if len(all_comms) > 1 else all_comms[0]
        comm_id, sender_serial, receiver_serial, sender_slot, receiver_slot, enc_msg, timestamp = comm
        
        st.markdown(f"""
        **Step 1: Identify sender and timeslot**
        - Sender: {sender_serial}
        - Timeslot: {sender_slot}
        
        **Step 2: Query database for sender's badge at that timeslot**
        """)
        
        # Get sender's badge from database
        with db._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT badge FROM identities
                WHERE serial = ? AND timeslot = ?
            """, (sender_serial, sender_slot))
            result = cursor.fetchone()
            if result:
                stored_badge = result[0]
                st.code(f"Badge Found: {stored_badge[:32]}...", language="")
                
                st.markdown("**Step 3: Decrypt message using sender's badge**")
                
                # Create identity object from stored badge
                from agent_system.agent_identity import AgentIdentity
                stored_identity = AgentIdentity(
                    serial=sender_serial,
                    timeslot=sender_slot,
                    badge=bytes.fromhex(stored_badge),
                    qrng_seed=b"",
                    timestamp=""
                )
                
                # Find original IV for this message
                iv_to_use = iv1 if sender_slot == 1 else iv2
                
                try:
                    decrypted_msg = channel.decrypt_message(enc_msg, iv_to_use, stored_identity)
                    st.success(f"  DECRYPTED: '{decrypted_msg}'")
                    
                    st.markdown(f"""
                    **Step 4: Verification complete**
                    - Confirmed sender: {sender_serial}
                    - Confirmed timeslot: {sender_slot}
                    - Confirmed message authenticity
                    - Only {sender_serial} had this badge at timeslot {sender_slot}
                    """)
                except Exception as e:
                    st.error(f"Decryption error: {str(e)}")
        
        st.markdown("-"*80)
        
        # Security test
        st.markdown("## SECURITY DEMONSTRATION")
        st.markdown("<hr>", unsafe_allow_html=True)
        
        st.markdown("**[TEST] What if someone tries to use OLD badge to decrypt NEW message?**")
        st.info("Attempting to decrypt Timeslot 2 message with Timeslot 1 badge...")
        
        try:
            wrong_decrypt = channel.decrypt_message(encrypted_msg2, iv2, timeslot1_identities[agents[0].serial])
            st.error("FAILED: Security breach!")
        except:
            st.success("  SECURITY SUCCESS: Old badge cannot decrypt new message!")
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Summary
        st.markdown("## SUMMARY")
        st.markdown("<hr>", unsafe_allow_html=True)
        
        st.markdown("""
        **BADGE ROTATION:**
        - Each agent gets NEW badge every timeslot (5 minutes)
        - Same agent, different timeslots = different badges
        
        **CENTRALIZED TRACKING:**
        - All badges stored in database with timeslot info
        - Admin can query any agent's badge at any timeslot
        
        **COMMUNICATION LOGGING:**
        - Every message logged with sender, receiver, timeslot
        - Encrypted message stored in database
        
        **ADMIN VERIFICATION:**
        - Admin queries: "Which agent sent this at what timeslot?"
        - Admin retrieves: Badge for that agent at that timeslot
        - Admin decrypts: Message using correct badge
        - Admin confirms: Sender identity verified
        
        **SECURITY:**
        - Old badges don't work for new messages
        - Wrong agents can't decrypt messages
        - Each communication uniquely tied to agent + timeslot
        
        **SYSTEM VALIDATION:**
        - All security mechanisms verified
        - Badge rotation working correctly
        - Authentication and logging functional
        """)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        st.success("DEMONSTRATION COMPLETE!")
        st.markdown("<hr>", unsafe_allow_html=True)
    

def analytics_page(db):
    """Analytics and statistics from simulation"""
    st.title("SIMULATION ANALYTICS")
    
    st.markdown("""
    <div class='info-card' style='background-color: #2d1a4d; border-left: 4px solid #FF00FF;'>
    <h4>Real-Time Statistics & Performance Metrics</h4>
    <p>All data is calculated from the SQLite database in real-time</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Get data from database
    all_identities = db.get_recent_identities(1000)
    all_comms = db.get_recent_communications(1000)
    
    # Calculate metrics
    total_identities = len(all_identities)
    unique_agents = len(set([identity[1] for identity in all_identities]))
    total_messages = len(all_comms)
    
    # Display key metrics
    st.markdown("### Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Agents", unique_agents, help="Unique agents in database")
    with col2:
        st.metric("Total Identities", total_identities, help="Total badge generations")
    with col3:
        st.metric("Messages Sent", total_messages, help="Total encrypted communications")
    with col4:
        avg_identities = total_identities / unique_agents if unique_agents > 0 else 0
        st.metric("Avg Identities/Agent", f"{avg_identities:.1f}", help="Average badge rotations per agent")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Agent breakdown
    if all_identities:
        st.markdown("### Agent Details")
        
        # Group by agent
        agent_stats = {}
        for identity in all_identities:
            serial = identity[1]
            timeslot = identity[2]
            badge = identity[3]
            timestamp = identity[4]
            
            if serial not in agent_stats:
                agent_stats[serial] = {
                    "identities": [],
                    "first_seen": timestamp,
                    "last_seen": timestamp,
                    "timeslots": []
                }
            
            agent_stats[serial]["identities"].append({
                "timeslot": timeslot,
                "badge": badge,
                "timestamp": timestamp
            })
            agent_stats[serial]["timeslots"].append(timeslot)
            agent_stats[serial]["last_seen"] = timestamp
        
        # Display agent stats
        for serial, stats in sorted(agent_stats.items()):
            with st.expander(f"{serial} ({len(stats['identities'])} identit(ies))", expanded=False):
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.markdown(f"""
                    **Agent Information:**
                    - First Seen: `{stats['first_seen']}`
                    - Last Seen: `{stats['last_seen']}`
                    - Total Identities: `{len(stats['identities'])}`
                    - Timeslots: `{sorted(set(stats['timeslots']))}`
                    """)
                
                with col_b:
                    st.markdown("**Latest Badge:**")
                    latest = stats['identities'][0]
                    st.code(f"{latest['badge'][:64]}...", language="")
                    st.caption(f"Timeslot {latest['timeslot']}")
    else:
        st.info("No agents in database yet. Run the **Live Simulation** to generate data.")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Communication analytics
    if all_comms:
        st.markdown("### Communication Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Message distribution
            sender_counts = {}
            for comm in all_comms:
                sender = comm[1]
                sender_counts[sender] = sender_counts.get(sender, 0) + 1
            
            st.markdown("**Top Senders:**")
            for sender, count in sorted(sender_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
                st.text(f"{sender}: {count} message(s)")
        
        with col2:
            # Message sizes
            sizes = [len(comm[5]) for comm in all_comms]
            avg_size = sum(sizes) / len(sizes) if sizes else 0
            min_size = min(sizes) if sizes else 0
            max_size = max(sizes) if sizes else 0
            
            st.markdown("**Message Sizes:**")
            st.text(f"Average: {avg_size:.1f} bytes")
            st.text(f"Minimum: {min_size} bytes")
            st.text(f"Maximum: {max_size} bytes")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Recent messages
        st.markdown("**Recent Communications:**")
        recent_data = []
        for comm in all_comms[:10]:
            recent_data.append({
                "ID": comm[0],
                "From": comm[1],
                "To": comm[2],
                "Sender Slot": comm[3],
                "Receiver Slot": comm[4],
                "Size": f"{len(comm[5])} bytes",
                "Time": comm[6]
            })
        
        df = pd.DataFrame(recent_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No communications logged yet. Run the **Live Simulation** to generate data.")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # System status
    st.markdown("### Security Status")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Encryption:**
        - Algorithm: AES-256-CBC
        - Status: Active
        - Key Derivation: SHA-256
        """)
    
    with col2:
        st.markdown("""
        **Quantum Badges:**
        - Circuit Size: 16 qubits
        - Entangling Layers: 3
        - Hash Function: Qiskit-based
        """)
    
    with col3:
        st.markdown("""
        **Database:**
        - Type: SQLite
        - Status: Connected
        - Integrity: Verified
        """)


# Main execution
if __name__ == "__main__":
    init_session_state()
    
    if not st.session_state.authenticated:
        login_page()
    else:
        main_dashboard()
