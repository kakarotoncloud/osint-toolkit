# ⬛ OSINT Toolkit

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-FF4B4B.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A modular, highly accessible Open Source Intelligence (OSINT) dashboard. This application aggregates publicly available data and routing information into a clean, minimal, and high-contrast user interface.

**Disclaimer:** This tool relies strictly on open-source, publicly available APIs and legal data extraction methods. It does not perform active scanning, exploitation, or illegal data acquisition. 

## 🚀 Features

* **🌐 IP Geolocation:** Resolves IPv4 addresses to physical locations, ISPs, and coordinates via `ip-api`.
* **🗄️ Domain Analysis:** Extracts WHOIS registration data and resolves core DNS records (A, MX) using `python-whois` and `dnspython`.
* **📱 Telecommunications Parsing:** Validates and extracts regional and carrier data from E.164 formatted international phone numbers.
* **🔑 Cryptographic Credential Audit:** Securely checks passwords against global data breaches using the `k-Anonymity` model via the HIBP API (ensuring the actual password string never leaves the client machine).

## 🛠️ Installation & Setup

### Local Execution
Ensure you have Python 3.8+ installed on your system.

1. **Clone the repository**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/osint-toolkit.git](https://github.com/YOUR_USERNAME/osint-toolkit.git)
   cd osint-toolkit
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the application**
   ```bash
   streamlit run app.py
   ```
   The application will become available at `http://localhost:8501`.

### Cloud Deployment (Streamlit Community Cloud)
1. Fork or clone this repository to your GitHub account.
2. Log into [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **New app**, select this repository, and set the main file path to `app.py`.
4. Click **Deploy**.

## 🏗️ Architecture

* **Frontend/UI:** Streamlit (Customized with minimal high-contrast CSS)
* **Networking & Requests:** `requests`
* **DNS/Domain Resolving:** `dnspython`, `python-whois`
* **Parsing:** `phonenumbers`
* **Cryptography:** `hashlib` (SHA-1 hashing for k-Anonymity)

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
