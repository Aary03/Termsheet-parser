import streamlit as st
import os
import json
import tempfile
from extract import extract_termsheet
import pandas as pd
import base64

# Set page configuration
st.set_page_config(
    page_title="2Cents Capital Termsheet Parser", 
    page_icon="📄", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for theme and styling
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-yellow: #F7D358;
        --secondary-yellow: #F1C232;
        --light-yellow: #FFF2CC;
        --black: #000000;
        --dark-gray: #333333;
        --white: #FFFFFF;
        --light-gray: #F8F8F8;
    }
    
    /* Global styles */
    .stApp {
        background-color: var(--white);
        color: var(--dark-gray);
    }
    
    h1, h2, h3 {
        color: var(--black) !important;
    }
    
    /* Header styling */
    .main-header {
        background-color: var(--primary-yellow);
        padding: 2rem;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        margin: 0;
        padding: 0;
        font-size: 2.5rem;
        font-weight: bold;
    }
    
    /* Card styling */
    .data-card {
        background-color: var(--white);
        border-left: 5px solid var(--secondary-yellow);
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    .data-card h3 {
        color: var(--black);
        margin-top: 0;
        border-bottom: 2px solid var(--light-yellow);
        padding-bottom: 0.5rem;
    }
    
    /* Upload area styling */
    .upload-area {
        background-color: var(--light-gray);
        border: 2px dashed var(--secondary-yellow);
        border-radius: 0.5rem;
        padding: 2rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: var(--secondary-yellow);
        color: var(--black);
        font-weight: bold;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 0.25rem;
    }
    
    .stButton>button:hover {
        background-color: var(--primary-yellow);
        color: var(--black);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: var(--light-gray);
        border-radius: 4px 4px 0 0;
        border-left: 1px solid #E0E0E0;
        border-right: 1px solid #E0E0E0;
        border-top: 1px solid #E0E0E0;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--light-yellow);
        border-left: 1px solid var(--secondary-yellow);
        border-right: 1px solid var(--secondary-yellow);
        border-top: 3px solid var(--secondary-yellow);
    }
    
    /* Property styling */
    .property-label {
        font-weight: bold;
        color: var(--dark-gray);
    }
    
    .property-value {
        color: var(--black);
    }
    
    /* Table styling */
    .table-container {
        border-radius: 0.5rem;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: var(--light-yellow);
        border-radius: 4px;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 2rem;
        padding: 1rem;
        background-color: var(--light-yellow);
        border-radius: 0.5rem;
    }

    /* Hide dataframe index */
    .dataframe thead tr:first-child th:first-child {
        display: none;
    }
    .dataframe tbody tr td:first-child {
        display: none;
    }
    
    /* Download button */
    .download-button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background-color: var(--secondary-yellow);
        color: var(--black);
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        text-decoration: none;
        margin-top: 1rem;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    
    .download-button:hover {
        background-color: var(--primary-yellow);
    }
    
    .download-icon {
        margin-right: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Create a download link
def get_download_link(data, filename, text):
    """Generates a link to download the given data as a file with the given filename"""
    json_str = json.dumps(data, indent=4)
    b64 = base64.b64encode(json_str.encode()).decode()
    href = f'<a class="download-button" href="data:file/json;base64,{b64}" download="{filename}">📥 <span class="download-icon"></span>{text}</a>'
    return href

# Header
st.markdown('<div class="main-header"><h1>2Cents Capital Termsheet Parser</h1></div>', unsafe_allow_html=True)
st.markdown("Easily extract structured data from complex financial product term sheets", unsafe_allow_html=True)

# Upload section
st.markdown('<div class="upload-area">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload Termsheet", type=["pdf"], label_visibility="collapsed")
if uploaded_file is not None:
    st.markdown(f"📄 **File uploaded:** {uploaded_file.name}")
st.markdown('</div>', unsafe_allow_html=True)

def render_property(label, value, is_important=False):
    """Helper function to render a property with consistent styling"""
    if is_important:
        return f'<div><span class="property-label">{label}:</span> <span class="property-value" style="font-size: 1.1rem; font-weight: bold;">{value}</span></div>'
    return f'<div><span class="property-label">{label}:</span> <span class="property-value">{value}</span></div>'

if uploaded_file is not None:
    # Save the uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name
    
    # Process button
    if st.button("Extract Data", key="extract_button"):
        with st.spinner("🔍 Extracting data from the termsheet..."):
            try:
                # Extract data
                result = extract_termsheet(tmp_path)
                
                # Remove the temporary file
                os.unlink(tmp_path)
                
                # Display success message
                st.success("✅ Extraction complete!")
                
                # Generate filename for download (based on uploaded file)
                filename = f"{os.path.splitext(uploaded_file.name)[0]}_extracted.json"
                
                # Display download button
                download_col1, download_col2 = st.columns([1, 3])
                with download_col1:
                    st.markdown(get_download_link(result, filename, "Download JSON"), unsafe_allow_html=True)
                
                # Display results in tabs
                tab1, tab2, tab3, tab4, tab5 = st.tabs(["General Info", "Underlyings & Dates", "Coupon & Redemption", "Risk Factors", "Raw JSON"])
                
                with tab1:
                    # Product General Information
                    if result.get("productGeneral"):
                        pg = result["productGeneral"]
                        
                        st.markdown('<div class="data-card">', unsafe_allow_html=True)
                        st.markdown('<h3>Product General Information</h3>', unsafe_allow_html=True)
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(render_property("Product Name", pg.get('productName', 'N/A'), True), unsafe_allow_html=True)
                            st.markdown(render_property("Product Type", pg.get('productType', 'N/A')), unsafe_allow_html=True)
                            st.markdown(render_property("Currency", pg.get('currency', 'N/A')), unsafe_allow_html=True)
                            st.markdown(render_property("Issue Size", pg.get('issueSize', 'N/A')), unsafe_allow_html=True)
                        with col2:
                            st.markdown(render_property("Denomination", pg.get('denomination', 'N/A')), unsafe_allow_html=True)
                            st.markdown(render_property("Minimum Investment", pg.get('minimumInvestment', 'N/A')), unsafe_allow_html=True)
                            st.markdown(render_property("ISIN", pg.get('ISIN', 'N/A')), unsafe_allow_html=True)
                            st.markdown(render_property("Valor", pg.get('valor', 'N/A')), unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Issuer Information
                    if result.get("issuerInformation"):
                        ii = result["issuerInformation"]
                        
                        st.markdown('<div class="data-card">', unsafe_allow_html=True)
                        st.markdown('<h3>Issuer Information</h3>', unsafe_allow_html=True)
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(render_property("Issuer Name", ii.get('issuerName', 'N/A'), True), unsafe_allow_html=True)
                            st.markdown(render_property("Issuer Address", ii.get('issuerAddress', 'N/A')), unsafe_allow_html=True)
                            st.markdown(render_property("Issuer Rating", ii.get('issuerRating', 'N/A')), unsafe_allow_html=True)
                        with col2:
                            st.markdown(render_property("Supervisory Authority", ii.get('supervisoryAuthority', 'N/A')), unsafe_allow_html=True)
                            st.markdown(render_property("Calculation Agent", ii.get('calculationAgent', 'N/A')), unsafe_allow_html=True)
                            agents = ii.get('fiscalTransferPayingAgents', [])
                            if agents and isinstance(agents, list):
                                agents_str = ", ".join(filter(None, agents))
                                st.markdown(render_property("Fiscal/Transfer/Paying Agents", agents_str), unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Product Description
                    if result.get("productDescription"):
                        pd_data = result["productDescription"]
                        
                        st.markdown('<div class="data-card">', unsafe_allow_html=True)
                        st.markdown('<h3>Product Description</h3>', unsafe_allow_html=True)
                        st.markdown(render_property("Description", pd_data.get('description', 'N/A')), unsafe_allow_html=True)
                        st.markdown(render_property("Market Expectation", pd_data.get('marketExpectation', 'N/A')), unsafe_allow_html=True)
                        if pd_data.get('referenceCodes') and isinstance(pd_data['referenceCodes'], dict):
                            st.markdown(render_property("Reference Code", pd_data['referenceCodes'].get('code', 'N/A')), unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                
                with tab2:
                    # Key Dates
                    if result.get("dates"):
                        dates = result["dates"]
                        
                        st.markdown('<div class="data-card">', unsafe_allow_html=True)
                        st.markdown('<h3>Key Dates</h3>', unsafe_allow_html=True)
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(render_property("Initial Fixing Date", dates.get('initialFixingDate', 'N/A'), True), unsafe_allow_html=True)
                            st.markdown(render_property("Issue Date", dates.get('issueDate', 'N/A'), True), unsafe_allow_html=True)
                        with col2:
                            st.markdown(render_property("Final Fixing Date", dates.get('finalFixingDate', 'N/A'), True), unsafe_allow_html=True)
                            st.markdown(render_property("Redemption Date", dates.get('redemptionDate', 'N/A'), True), unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Underlyings
                    if result.get("underlyings") and isinstance(result["underlyings"], list):
                        st.markdown('<div class="data-card">', unsafe_allow_html=True)
                        st.markdown('<h3>Underlyings</h3>', unsafe_allow_html=True)
                        
                        # Create a DataFrame for better display
                        underlyings_data = []
                        for underlying in result["underlyings"]:
                            if underlying:
                                underlyings_data.append({
                                    "Name": underlying.get('name', 'N/A'),
                                    "Exchange": underlying.get('relatedExchange', 'N/A'),
                                    "Currency": underlying.get('referenceCurrency', 'N/A'),
                                    "Bloomberg Ticker": underlying.get('bloombergTicker', 'N/A'),
                                    "Initial Fixing Level": underlying.get('initialFixingLevel', 'N/A'),
                                    "Strike Level": underlying.get('strikeLevel', 'N/A')
                                })
                        
                        if underlyings_data:
                            df = pd.DataFrame(underlyings_data)
                            st.markdown('<div class="table-container">', unsafe_allow_html=True)
                            st.dataframe(df, use_container_width=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                
                with tab3:
                    # Coupon Information
                    if result.get("coupon"):
                        coupon = result["coupon"]
                        
                        st.markdown('<div class="data-card">', unsafe_allow_html=True)
                        st.markdown('<h3>Coupon Information</h3>', unsafe_allow_html=True)
                        st.markdown(render_property("Coupon Amount Formula", coupon.get('couponAmountFormula', 'N/A')), unsafe_allow_html=True)
                        st.markdown(render_property("Coupon Rate", coupon.get('couponRate', 'N/A')), unsafe_allow_html=True)
                        
                        # Coupon Payment Dates
                        if coupon.get("couponPaymentDates") and isinstance(coupon["couponPaymentDates"], list):
                            st.markdown("<h4>Coupon Payment Dates</h4>", unsafe_allow_html=True)
                            
                            coupon_data = []
                            for payment in coupon["couponPaymentDates"]:
                                if payment:
                                    coupon_data.append({
                                        "Payment #": payment.get("paymentNumber", ""),
                                        "Coupon Rate": payment.get("couponRate", "N/A"),
                                        "Payment Date": payment.get("paymentDate", "N/A")
                                    })
                            
                            if coupon_data:
                                df = pd.DataFrame(coupon_data)
                                st.markdown('<div class="table-container">', unsafe_allow_html=True)
                                st.dataframe(df, use_container_width=True)
                                st.markdown('</div>', unsafe_allow_html=True)
                                
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Early Redemption
                    if result.get("earlyRedemption"):
                        er = result["earlyRedemption"]
                        
                        st.markdown('<div class="data-card">', unsafe_allow_html=True)
                        st.markdown('<h3>Early Redemption</h3>', unsafe_allow_html=True)
                        st.markdown(render_property("Automatic Early Redemption Event", er.get('automaticEarlyRedemptionEvent', 'N/A')), unsafe_allow_html=True)
                        
                        # Redemption Events
                        if er.get("redemptionEvents") and isinstance(er["redemptionEvents"], list):
                            st.markdown("<h4>Redemption Events</h4>", unsafe_allow_html=True)
                            
                            redemption_data = []
                            for event in er["redemptionEvents"]:
                                if event:
                                    redemption_data.append({
                                        "Observation #": event.get("observationNumber", ""),
                                        "Autocall Level": event.get("autocallLevel", "N/A"),
                                        "Redemption Amount": event.get("earlyRedemptionAmount", "N/A"),
                                        "Observation Date": event.get("observationDate", "N/A"),
                                        "Redemption Date": event.get("redemptionDate", "N/A")
                                    })
                            
                            if redemption_data:
                                df = pd.DataFrame(redemption_data)
                                st.markdown('<div class="table-container">', unsafe_allow_html=True)
                                st.dataframe(df, use_container_width=True)
                                st.markdown('</div>', unsafe_allow_html=True)
                                
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Final Redemption
                    if result.get("redemption"):
                        redemption = result["redemption"]
                        
                        st.markdown('<div class="data-card">', unsafe_allow_html=True)
                        st.markdown('<h3>Final Redemption</h3>', unsafe_allow_html=True)
                        st.markdown(render_property("Redemption Formula", redemption.get('redemptionFormula', 'N/A')), unsafe_allow_html=True)
                        st.markdown(render_property("Final Fixing Level", redemption.get('finalFixingLevel', 'N/A')), unsafe_allow_html=True)
                        st.markdown(render_property("Performance Calculation", redemption.get('performanceCalculation', 'N/A')), unsafe_allow_html=True)
                        st.markdown(render_property("Worst Performance", redemption.get('worstPerformance', 'N/A')), unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                
                with tab4:
                    # Risk Factors
                    if result.get("riskFactors"):
                        rf = result["riskFactors"]
                        
                        st.markdown('<div class="data-card">', unsafe_allow_html=True)
                        st.markdown('<h3>Risk Factors</h3>', unsafe_allow_html=True)
                        st.markdown(render_property("Risk of Loss", rf.get('riskOfLoss', 'N/A')), unsafe_allow_html=True)
                        st.markdown(render_property("Additional Risk Factors", rf.get('additionalRiskFactors', 'N/A')), unsafe_allow_html=True)
                        st.markdown(render_property("Issuer Credit Risk", rf.get('issuerCreditRisk', 'N/A')), unsafe_allow_html=True)
                        st.markdown(render_property("Market Risks", rf.get('marketRisks', 'N/A')), unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Product Documentation
                    if result.get("productDocumentation") and isinstance(result["productDocumentation"], dict):
                        pd_doc = result["productDocumentation"]
                        
                        st.markdown('<div class="data-card">', unsafe_allow_html=True)
                        st.markdown('<h3>Product Documentation</h3>', unsafe_allow_html=True)
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(render_property("Unique Identifier", pd_doc.get('uniqueIdentifier', 'N/A')), unsafe_allow_html=True)
                            st.markdown(render_property("Notices", pd_doc.get('notices', 'N/A')), unsafe_allow_html=True)
                            st.markdown(render_property("Listing Exchange", pd_doc.get('listingExchange', 'N/A')), unsafe_allow_html=True)
                        with col2:
                            st.markdown(render_property("Business Day Convention", pd_doc.get('businessDayConvention', 'N/A')), unsafe_allow_html=True)
                            st.markdown(render_property("Secondary Market", pd_doc.get('secondaryMarket', 'N/A')), unsafe_allow_html=True)
                            st.markdown(render_property("Settlement Type", pd_doc.get('settlementType', 'N/A')), unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                
                with tab5:
                    # Raw JSON
                    st.markdown('<div class="data-card">', unsafe_allow_html=True)
                    st.markdown('<h3>Raw JSON Data</h3>', unsafe_allow_html=True)
                    st.json(result)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                # Footer
                st.markdown('<div class="footer">2Cents Capital Termsheet Parser | Powered by Llama Extract</div>', unsafe_allow_html=True)
                    
            except Exception as e:
                st.error(f"Error during extraction: {e}")
                # Remove the temporary file in case of error
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
                    
else:
    # Display empty state
    st.markdown('''
    <div style="text-align: center; padding: 2rem; color: #666;">
        <img src="https://cdn-icons-png.flaticon.com/512/5251/5251470.png" width="100">
        <h3>Upload a termsheet PDF file to get started</h3>
        <p>This tool will extract structured data from your termsheet into a well-organized format</p>
    </div>
    ''', unsafe_allow_html=True) 