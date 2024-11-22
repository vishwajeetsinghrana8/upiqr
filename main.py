import streamlit as st
import qrcode
from io import BytesIO


def generate_upi_qr(name, upi_id, amount):
    # Create the UPI URL format
    upi_string = f"upi://pay?pa={upi_id}&pn={name}&am={amount}&cu=INR"

    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(upi_string)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    return img


# Streamlit app
st.title("UPI QR Code Generator")
st.write("Generate a QR code for UPI transactions by filling in the details below.")

# Sidebar for Dark/Light Mode Toggle
st.sidebar.title("User Details")


# Layout using columns
col1, col2, _ = st.columns([1, 2, 1])  # Left column for inputs, center for QR code

# Inputs on the left
with col1:
    name = st.sidebar.text_input("Enter your Name")
    upi_id = st.sidebar.text_input("Enter your UPI ID (e.g., example@upi)")
    amount = st.sidebar.text_input("Enter the Transaction Amount (INR)")
    generate_qr = st.sidebar.button("Generate QR Code")

# Center area for QR code display
with col2:
    if generate_qr:
        if name and upi_id and amount:
            try:
                amount = float(amount)  # Convert amount to a float
                qr_image = generate_upi_qr(name, upi_id, amount)

                # Create a buffer to store the QR code
                buffer = BytesIO()
                qr_image.save(buffer, format="PNG")
                buffer.seek(0)

                # Display the QR code in the center
                st.image(buffer, caption="UPI QR Code", use_container_width=False, width=250)

                # Provide download option below the QR code
                st.download_button(
                    label="Download QR Code",
                    data=buffer,
                    file_name="upi_qr_code.png",
                    mime="image/png"
                )
            except ValueError:
                st.error("Please enter a valid amount.")
        else:
            st.error("Please fill in all the fields.")
