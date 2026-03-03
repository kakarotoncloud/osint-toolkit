import streamlit as st
import requests
import whois
import dns.resolver
import phonenumbers
from phonenumbers import geocoder, carrier
import hashlib

# --- Page Config & Minimalist High-Contrast Styling ---
st.set_page_config(page_title="OSINT Toolkit", page_icon="⬛", layout="wide")

st.markdown("""
    <style>
    .main {background-color: #FAFAFA;}
    h1, h2, h3 {color: #111111;}
    .stButton>button {
        background-color: #111111;
        color: #FFFFFF;
        border-radius: 4px;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #333333;
        color: #FFFFFF;
    }
    .stAlert {border-radius: 4px;}
    </style>
""", unsafe_allow_html=True)

st.title("⬛ Open Source Intelligence Toolkit")
st.markdown("**A clean, modular, and strictly legal intelligence gathering dashboard.**")
st.divider()

# --- Sidebar Navigation ---
st.sidebar.title("Directory")
tool = st.sidebar.radio("Select Module:", 
                        ["IP Geolocation", "Domain Analysis", "Telecom Data", "Credential Check"])

st.sidebar.divider()
st.sidebar.info("Developed with Streamlit. Strictly adheres to open-source data protocols.")

# --- Tool 1: IP Geolocation ---
if tool == "IP Geolocation":
    st.header("🌐 IP Geolocation Lookup")
    ip_address = st.text_input("Target IP Address (e.g., 8.8.8.8):")
    
    if st.button("Execute Lookup"):
        if ip_address:
            try:
                with st.spinner('Querying routing databases...'):
                    response = requests.get(f"http://ip-api.com/json/{ip_address}").json()
                    if response['status'] == 'success':
                        st.success("Target Located.")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Country:** {response.get('country', 'N/A')}")
                            st.write(f"**Region:** {response.get('regionName', 'N/A')}")
                            st.write(f"**City:** {response.get('city', 'N/A')}")
                        with col2:
                            st.write(f"**ISP:** {response.get('isp', 'N/A')}")
                            st.write(f"**Organization:** {response.get('org', 'N/A')}")
                            st.write(f"**Coordinates:** {response.get('lat')}, {response.get('lon')}")
                    else:
                        st.error("Target unreachable or invalid IP.")
            except Exception as e:
                st.error(f"Execution failed: {e}")

# --- Tool 2: Domain Analysis ---
elif tool == "Domain Analysis":
    st.header("🗄️ Domain & DNS Intelligence")
    domain = st.text_input("Target Domain (e.g., github.com):")
    
    if st.button("Execute Analysis"):
        if domain:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Registrar Data (WHOIS)")
                try:
                    with st.spinner('Retrieving WHOIS...'):
                        w_info = whois.whois(domain)
                        st.write(f"**Registrar:** {w_info.registrar}")
                        st.write(f"**Creation Date:** {w_info.creation_date}")
                        st.write(f"**Expiration Date:** {w_info.expiration_date}")
                except Exception as e:
                    st.error("WHOIS lookup failed.")
            
            with col2:
                st.subheader("Routing Data (DNS)")
                try:
                    with st.spinner('Resolving records...'):
                        a_records = dns.resolver.resolve(domain, 'A')
                        st.write("**A Records (IPv4):**")
                        for r in a_records: st.code(r.to_text())
                        
                        mx_records = dns.resolver.resolve(domain, 'MX')
                        st.write("**MX Records (Mail):**")
                        for r in mx_records: st.code(r.to_text())
                except Exception as e:
                    st.error("DNS lookup failed.")

# --- Tool 3: Telecom Data ---
elif tool == "Telecom Data":
    st.header("📱 Telecommunications Parsing")
    st.markdown("*Extracts regional and carrier routing data from international formats.*")
    phone_num = st.text_input("Target Number (Include Country Code, e.g., +14155552671):")
    
    if st.button("Parse Number"):
        if phone_num:
            try:
                parsed_num = phonenumbers.parse(phone_num)
                if phonenumbers.is_valid_number(parsed_num):
                    st.success("Number Format Validated.")
                    st.write(f"**Origin Region:** {geocoder.description_for_number(parsed_num, 'en') or 'Unknown'}")
                    st.write(f"**Service Carrier:** {carrier.name_for_number(parsed_num, 'en') or 'Unknown'}")
                else:
                    st.error("Invalid sequence format.")
            except Exception as e:
                st.error(f"Parsing engine failed: {e}")

# --- Tool 4: Credential Check ---
elif tool == "Credential Check":
    st.header("🔑 Cryptographic Credential Audit")
    st.markdown("*Utilizes k-Anonymity to check passwords against known data breaches without transmitting the full string.*")
    
    password_to_check = st.text_input("Enter credential string to audit:", type="password")
    
    if st.button("Execute Audit"):
        if password_to_check:
            sha1_password = hashlib.sha1(password_to_check.encode('utf-8')).hexdigest().upper()
            first5_char, tail = sha1_password[:5], sha1_password[5:]
            
            try:
                with st.spinner('Cross-referencing cryptographic databases...'):
                    response = requests.get(f"https://api.pwnedpasswords.com/range/{first5_char}")
                    if response.status_code == 200:
                        hashes = (line.split(':') for line in response.text.splitlines())
                        leak_count = next((int(count) for h, count in hashes if h == tail), 0)
                        
                        if leak_count > 0:
                            st.error(f"⚠️ **COMPROMISED:** Credential appears {leak_count:,} times in known breach datasets.")
                        else:
                            st.success("✅ **SECURE:** Credential not found in known datasets.")
                    else:
                        st.error("Database connection failed.")
            except Exception as e:
                st.error(f"Audit failed: {e}")
