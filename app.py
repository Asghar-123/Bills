import streamlit as st
from fpdf import FPDF
import io

# Page config
st.set_page_config(page_title="Monthly Utilities", layout="centered")

# App title
st.title("🏠 Monthly Utility Divider")

# Utility inputs
st.header("Enter Utility Bills")
ke = st.number_input("KE (Electricity)", min_value=0.0, step=1.0)
ssgc = st.number_input("SSGC (Gas)", min_value=0.0, step=1.0)
water = st.number_input("Water", min_value=0.0, step=1.0)
net = st.number_input("Internet", min_value=0.0, step=1.0)
sweeper = st.number_input("Sweeper", min_value=0.0, step=1.0)

# Additional utility
st.subheader("Additional Utility (Optional)")
additional_label = st.text_input("Description")
additional_amount = st.number_input("Amount", min_value=0.0, step=1.0)
assigned_to = st.selectbox("Assign to", ["None", "Razi", "Zaki"])

# Calculate shares
base_total = ke + ssgc + water + net + sweeper
shared_total = base_total / 2

razi_share = shared_total
zaki_share = shared_total

if assigned_to == "Razi":
    razi_share += additional_amount
elif assigned_to == "Zaki":
    zaki_share += additional_amount

# Display results
st.markdown("## 🧮 Results")
st.write(f"**Total Shared Utilities:** Rs. {base_total}")
st.write(f"**Razi's Share:** Rs. {razi_share}")
st.write(f"**Zaki's Share:** Rs. {zaki_share}")

# Generate PDF
if st.button("📄 Generate PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Monthly Utility Report", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"KE (Electricity): Rs. {ke}", ln=True)
    pdf.cell(200, 10, txt=f"SSGC (Gas): Rs. {ssgc}", ln=True)
    pdf.cell(200, 10, txt=f"Water: Rs. {water}", ln=True)
    pdf.cell(200, 10, txt=f"Internet: Rs. {net}", ln=True)
    pdf.cell(200, 10, txt=f"Sweeper: Rs. {sweeper}", ln=True)

    if additional_label and additional_amount > 0 and assigned_to != "None":
        pdf.cell(200, 10, txt=f"Additional Utility ({assigned_to}): {additional_label} - Rs. {additional_amount}", ln=True)

    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Total Shared Utilities: Rs. {base_total}", ln=True)
    pdf.cell(200, 10, txt=f"Razi's Share: Rs. {razi_share}", ln=True)
    pdf.cell(200, 10, txt=f"Zaki's Share: Rs. {zaki_share}", ln=True)

    # Output PDF to memory
    pdf_output = io.BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    pdf_output.write(pdf_bytes)
    pdf_output.seek(0)

    # Streamlit download button
    st.download_button(
        label="⬇️ Download PDF",
        data=pdf_output,
        file_name="monthly_utilities.pdf",
        mime="application/pdf"
    )
