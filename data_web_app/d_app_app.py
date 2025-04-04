import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import requests
from PIL import Image

def generate_insights(df):
    insights = {}
    insights['Summary Statistics'] = df.describe()
    st.write("## Statistical Summary")
    st.dataframe(insights['Summary Statistics']) # Display statistical summary
    try:
        num_cols = df.select_dtypes(include=['number']).columns
        cat_cols = df.select_dtypes(exclude=['number']).columns

        if len(num_cols) > 0:
            st.write("## Numerical Column Visualizations")
            cols = st.columns(3)
            for i, col in enumerate(num_cols):
                with cols[i % 3]:
                    st.write(f"### Histogram for {col}")
                    fig, ax = plt.subplots()
                    sns.histplot(df[col], kde=True, ax=ax)
                    st.pyplot(fig)

                    st.write(f"### Boxplot for {col}")
                    fig, ax = plt.subplots()
                    sns.boxplot(y=df[col], ax=ax)
                    st.pyplot(fig)

        if len(num_cols) > 1:
            st.write("### Correlation Heatmap")
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(df[num_cols].corr(), annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)

        if len(cat_cols) > 0:
            st.write("## Categorical Column Visualizations")
            cols = st.columns(3)
            for i, col in enumerate(cat_cols):
                with cols[i % 3]:
                    st.write(f"### Countplot for {col}")
                    fig, ax = plt.subplots()
                    sns.countplot(x=df[col], ax=ax)
                    plt.xticks(rotation=45)
                    st.pyplot(fig)

                    st.write(f"### Pie Chart for {col}")
                    fig, ax = plt.subplots()
                    df[col].value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
                    ax.set_ylabel('')
                    st.pyplot(fig)
    except Exception as e:
        st.error(f"Error generating visualizations: {e}")

# Function to process payment using Paystack
PAYSTACK_SECRET_KEY = "sk_live_17db3ab8de86bc3b785ba8ca5ce5d1ce88c9d9f6"  # Your Paystack secret key
if "payment_unlocked" not in st.session_state:
    st.session_state.payment_unlocked = False
if "payment_reference" not in st.session_state:
    st.session_state.payment_reference = None

def initialize_payment():
    st.write("### Payment Required to Download/Print Report")
    if st.button("Pay Now (Paystack)"):
        payment_url = "https://api.paystack.co/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "email": "customer@example.com",  # Replace with a valid email
            "amount": 50000,  # Paystack uses kobo (500 NGN = 50000 kobo)
            "currency": "NGN",
            "callback_url": "https://yourwebsite.com/payment-success"  # Replace with your callback URL
        }
        try:
            response = requests.post(payment_url, json=payload, headers=headers)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            data = response.json().get("data", {})
            st.session_state.payment_reference = data.get("reference")
            payment_link = data.get("authorization_url")
            if payment_link:
                st.markdown(f"[Click here to complete payment]({payment_link})")
        except requests.exceptions.RequestException as e:
            st.error(f"Payment processing failed: {e}") # more specific error message.

def verify_payment():
    if st.session_state.payment_reference:
        verification_url = f"https://api.paystack.co/transaction/verify/{st.session_state.payment_reference}"
        headers = {"Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"}
        try:
            response = requests.get(verification_url, headers=headers)
            response.raise_for_status()
            data = response.json().get("data", {})
            if data.get("status") == "success":
                st.session_state.payment_unlocked = True
                st.success("Payment successful! You can now download or print your report.")
            else:
                st.error("Payment verification failed. Please try again.")
        except requests.exceptions.RequestException as e:
            st.error(f"Could not verify payment: {e}")

def main():
    st.set_page_config(page_title="Enecom IT-Data Analytics", layout="wide")
    image = Image.open('img/logo_enecom.png') #replace logo.png with your logo file.
    st.image(image, width=100)
    st.title("Enecom IT-Data Analytics Web App")
    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file)
            st.write("### Data Preview")
            st.dataframe(df.head())

            if st.button("Generate Insights"):
                generate_insights(df)
                initialize_payment()

            if st.session_state.payment_reference and not st.session_state.payment_unlocked:
                verify_payment()

            if st.session_state.payment_unlocked:
                if st.button("Download Report"):
                    towrite = io.BytesIO()
                    df.to_csv(towrite, index=False)
                    towrite.seek(0)
                    st.download_button(label="Download CSV", data=towrite, file_name="report.csv", mime="text/csv")

                if st.button("Print Report"):
                    st.write("Printing is enabled after payment.") # You can add print functionality here if needed.
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()