import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
from fpdf import FPDF
from PIL import Image

# Set page title and favicon
st.set_page_config(page_title="Enecom IT Solutions - Data Analytics", page_icon="logo_enecom.png", layout="wide")

# Center company logo and name using HTML and markdown
# Load and display company logo at the top
logo = Image.open("logo_enecom.png")
st.image(logo, width=200)

st.title("Data Analytics Web App")

def generate_insights(df):
    """Generates insights from the DataFrame with updated visualizations."""
    insights = {"Summary Statistics": df.describe()}

    num_cols = df.select_dtypes(include=['number']).columns
    cat_cols = df.select_dtypes(exclude=['number']).columns

    visualizations = []
    
    if len(num_cols) > 0:
        for col in num_cols:
            fig, ax = plt.subplots()
            sns.barplot(x=df.index, y=df[col], ax=ax)
            ax.set_title(f'Bar Chart - {col}')
            visualizations.append(fig)

            fig, ax = plt.subplots()
            sns.kdeplot(df[col], fill=True, ax=ax)
            ax.set_title(f'Density Plot - {col}')
            visualizations.append(fig)
    
    if len(cat_cols) > 0:
        for col in cat_cols:
            fig, ax = plt.subplots()
            df[col].value_counts().plot.pie(autopct='%1.1f%%', wedgeprops={'linewidth': 2, 'edgecolor': 'white'}, ax=ax)
            ax.set_title(f'Donut Chart - {col}')
            ax.set_ylabel('')
            visualizations.append(fig)
    
    if len(num_cols) > 1:
        fig, ax = plt.subplots()
        sns.heatmap(df[num_cols].corr(), annot=True, cmap='coolwarm', ax=ax)
        ax.set_title('Correlation Heatmap')
        visualizations.append(fig)
        
        fig, ax = plt.subplots()
        sns.scatterplot(x=df[num_cols[0]], y=df[num_cols[1]], ax=ax)
        ax.set_title('Scatter Plot')
        visualizations.append(fig)
    
    insights["Visualizations"] = visualizations
    return insights

def display_insights(insights):
    """Displays the generated insights in a grid format."""
    st.subheader("Summary Statistics")
    st.dataframe(insights['Summary Statistics'])
    
    st.subheader("Visualizations")
    cols = st.columns(2)
    for i, fig in enumerate(insights['Visualizations']):
        with cols[i % 2]:
            st.pyplot(fig)

def generate_pdf(insights):
    """Generates a PDF report of insights."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, "Data Analysis Report", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Summary Statistics", ln=True)
    pdf.ln(5)
    
    for col in insights['Summary Statistics'].columns:
        pdf.multi_cell(0, 10, f"{col}: {insights['Summary Statistics'][col].to_dict()}")
        pdf.ln(3)
    
    pdf.ln(10)
    pdf.cell(200, 10, "Visualizations (Check output images separately)", ln=True)
    
    # Generate PDF as a string and convert to BytesIO
    pdf_output = pdf.output(dest='S').encode('latin1')
    return io.BytesIO(pdf_output)

def validate_file(file):
    """Validates if the uploaded file is a valid CSV or Excel file."""
    try:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        elif file.name.endswith(".xlsx"):
            df = pd.read_excel(file)
        else:
            st.error("Invalid file format! Please upload a CSV or Excel file.")
            return None

        if df.empty:
            st.error("The uploaded file is empty. Please upload a valid dataset.")
            return None

        if df.isnull().sum().sum() > 0:
            st.warning("The dataset contains missing values. Consider cleaning your data before analysis.")
        
        return df

    except Exception as e:
        st.error(f"Error reading file: {e}")
        return None

def main():
    uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        df = validate_file(uploaded_file)
        if df is not None:
            st.write("### Data Preview")
            st.dataframe(df.head())

            if st.button("Generate Insights"):
                insights = generate_insights(df)
                display_insights(insights)

                pdf_data = generate_pdf(insights)
                st.download_button(
                    label="Download Report as PDF",
                    data=pdf_data,
                    file_name="data_analysis_report.pdf",
                    mime="application/pdf"
                )

if __name__ == "__main__":
    main()
