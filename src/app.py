import streamlit as st
import requests
import pandas as pd
from io import StringIO
import json
from datetime import datetime
import os
from dotenv import load_dotenv
from utils import styling, api_rate_limiter, schema_information, sanitize_dataframe

load_dotenv()

SERVING_API = os.getenv("SERVING_API")
PAGE_ICON = os.getenv("PAGE_ICON")
key_data = os.getenv("API_KEY")

st.set_page_config(
    page_title="DeepMitre | DeepTempo",
    page_icon=PAGE_ICON,
    layout="wide",
)

st.markdown(styling, unsafe_allow_html=True)

# Constants for required NetFlow schema
REQUIRED_COLUMNS = [  
    "timestamp", "flow_dur", "src_ip", "dest_ip", "dest_port", "src_port", 
    "fwd_bytes", "bwd_bytes", "total_bwd_pkts", "total_fwd_pkts"
]

st.title("DeepMitre : NetFlow Log to Mitre Classification Tool")
st.write("Classify your NetFlow logs using Sigma rules and MITRE ATT&CK patterns powered by DeepTempo's Model.")
col1, col2 = st.columns(2)

with col1:
    with st.expander("📋 Instructions", expanded=True):
        st.markdown("""
        <div class="custom-markdown">
        1. Ensure your CSV file follows the required structure.
        2. Limit your file to 100 rows.
        3. Simply drop your file into the upload area.
        4. Download the processed report or review the visualizations.
        </div>
        """, unsafe_allow_html=True)

with col2:
    with st.expander("📋 View Required Schema", expanded=False):
        st.text("Your CSV file must include the following columns:")
        st.markdown(schema_information, unsafe_allow_html=True)

upload_placeholder = st.empty()
uploaded_file = upload_placeholder.file_uploader(
    "Upload your NetFlow CSV", 
    type="csv",
    help="Maximum file size: 200MB"
)

def display_csv_preview(csv_data):
    st.write("Uploaded File:")
    st.dataframe(csv_data[:2])

@api_rate_limiter
def call_serve_api(input_data):
    headers = {"Authorization": f"Bearer f{key_data}","Content-Type": "application/json"}
    try:
        response = requests.post(SERVING_API, headers=headers, json=[input_data])
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        st.error(f"API Error: {e.response.status_code} - {e.response.text}")
        return None

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        df, errors = sanitize_dataframe(df)
    except Exception as e:
        st.error(f"Invalid CSV file: {str(e)}")
        st.stop()
    
    payload = [row for row in df.to_dict(orient='records')]
    missing_columns = [col for col in REQUIRED_COLUMNS if col.lower() not in df.columns.str.lower()]

    if missing_columns:
        st.error(f"Missing columns: {', '.join(missing_columns)}")
    elif len(df) <= 100:
        st.success("File contains all required columns and meets the row limit of 100.")
        
        with st.spinner("Processing your request, please wait...",show_time=True):
            comparison_results = call_serve_api(payload)

        if comparison_results:
            results_df = pd.read_json(StringIO(json.dumps(comparison_results)), orient="records")
            tab1, tab2 = st.tabs(["Classification Results", "Visualization"])
            
            with tab1:
                st.subheader("MITRE ATT&CK Classification")
                st.info("Outputs sample")
                st.dataframe(results_df[:5])

            with tab2:
                st.subheader("Threat Visualization")
                st.write("Coming Soon......")

            downloaded = st.download_button(
                label="📥 Download Classified Data",
                data=results_df.to_csv(index=False).encode('utf-8'),
                file_name='netflow_to_mitre.csv',
                mime='text/csv'
            )

            if downloaded:
                st.success("Download complete.")
                st.rerun()

        else:
            st.error("Failed to get classification results.")
    else:
        st.error(f"File exceeds the row limit of 100. Your file contains {len(df)} rows.")
else:
    st.warning("Please upload a CSV file to proceed.")

st.header("📢 Obtaining an API Key")
st.markdown("""
To use our service programmatically, you will need an API key. If you don't have one, please reach out to the DeepTempo team.

- Visit our [Contact Us](https://www.deeptempo.ai/contact-us.html) page.
- Review our [Privacy Policy](https://www.deeptempo.ai/docs/DeepTempo%20-%20Privacy%20Policy%20for%20Snowflake%20NativeApp.pdf) for more information.
- Check our [Documentation](https://github.com/deepsecoss/DeepMITRE) for detailed API usage instructions.
""")
st.header("🎁 Free Trial of DeepTempo's Incident and MITRE Model")
st.markdown("""
We are pleased to offer a free trial of DeepTempo's Incident and MITRE Models on [Snowflake](https://www.snowflake.com/en/data-cloud/platform/).

- **Trial Features**:
    - Unrestricted access to Incident and MITRE models without row limitations.
    - Comprehensive analysis capabilities for NetFlow logs.

To begin your trial, please visit our [Free Trial Signup](https://app.snowflake.com/marketplace/listing/GZTYZOYXHP3/deeptempo-cybersecurity-tempo) page.

For further assistance or inquiries, Contact our team via the [Contact Us](https://www.deeptempo.ai/contact-us.html) page.
""")

st.markdown("""
<div class="footer">
    <p>
        <strong>DeepTempo.ai</strong> | 
        <a href="https://www.deeptempo.ai/contact-us.html">Contact Us</a> |
        <a href="https://github.com/deepsecoss">Community</a> | 
        <a href="https://www.deeptempo.ai/docs/DeepTempo%20-%20Privacy%20Policy%20for%20Snowflake%20NativeApp.pdf">Privacy</a> |
        <a href="https://app.snowflake.com/marketplace/listing/GZTYZOYXHP3/deeptempo-cybersecurity-tempo">Try Pro</a>
    </p>
    <p>© {} DeepTempo.ai. All rights reserved.</p>
</div>
""".format(datetime.now().year), unsafe_allow_html=True)
