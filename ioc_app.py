import pandas as pd
import re
import streamlit as st
from urllib.parse import urlparse


# Regex patterns
patterns = {
    "hash": re.compile(r'^[a-fA-F0-9]{32}$|^[a-fA-F0-9]{40}$|^[a-fA-F0-9]{64}$|^[a-fA-F0-9]{128}$'),
    "ip": re.compile(r'^(?:\d{1,3}\.){3}\d{1,3}$'),
    "domain": re.compile(r'^(?!\-)(?:[a-zA-Z0-9-]{1,63}\.)+[a-zA-Z]{2,}$')
}

def extract_domain_from_url(val):
    try:
        parsed = urlparse(val if val.startswith(('http://','https://')) else 'http://' + val)
        return parsed.hostname or ""
    except:
        return ""

def classify_value(val):
    val = val.strip()
    if not val:
        return None
    # if it's a URL, try to get domain
    if val.startswith(('http://','https://')) or '/' in val:
        dom = extract_domain_from_url(val)
        if dom:
            if patterns["domain"].match(dom):
                return ("domain", dom)
    # direct checks
    if patterns["hash"].match(val):
        return ("hash", val)
    if patterns["ip"].match(val):
        return ("ip", val)
    if patterns["domain"].match(val):
        return ("domain", val)
    # fallback: check if looks like domain inside (e.g., www.example.com/path)
    dom = extract_domain_from_url(val)
    if dom and patterns["domain"].match(dom):
        return ("domain", dom)
    return None

def extract_iocs(df):
    hashes, ips, domains = set(), set(), set()
    for col in df.columns:
        for value in df[col].astype(str):
            res = classify_value(value)
            if not res:
                continue
            typ, item = res
            if typ == "hash":
                hashes.add(item)
            elif typ == "ip":
                ips.add(item)
            elif typ == "domain":
                domains.add(item)
    return hashes, ips, domains

# Streamlit UI
st.title("🔍 IOC Extractor from Excel (Streamlit)")
st.write("Upload an Excel file (.xlsx/.xls). The app will auto-detect hashes, IPs, and domains (extracts domain from URLs).")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx", "xls"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, dtype=str).fillna("")
    st.success("✅ File uploaded!")
    hashes, ips, domains = extract_iocs(df)

    st.write(f"**Hashes found:** {len(hashes)}")
    st.write(f"**IPs found:** {len(ips)}")
    st.write(f"**Domains found:** {len(domains)}")

    # Optional small preview
    st.subheader("Preview (up to 20 each)")
    st.write("Hashes:", list(sorted(hashes))[:20])
    st.write("IPs:", list(sorted(ips))[:20])
    st.write("Domains:", list(sorted(domains))[:20])

    # Download buttons
    if hashes:
        st.download_button("⬇️ Download Hashes", "\n".join(sorted(hashes)), file_name="hashes.txt")
    if ips:
        st.download_button("⬇️ Download IPs", "\n".join(sorted(ips)), file_name="ips.txt")
    if domains:
        st.download_button("⬇️ Download Domains", "\n".join(sorted(domains)), file_name="domains.txt")

    # Optional: save files to local folder where Streamlit runs
    if st.checkbox("Save files to local folder (hashes.txt, ips.txt, domains.txt)"):
        with open("hashes.txt", "w") as f:
            f.write("\n".join(sorted(hashes)))
        with open("ips.txt", "w") as f:
            f.write("\n".join(sorted(ips)))
        with open("domains.txt", "w") as f:
            f.write("\n".join(sorted(domains)))
        st.success("Files saved to the current folder.")
