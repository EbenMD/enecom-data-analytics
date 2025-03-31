import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

def generate_insights(df):
    insights = {}
    insights['Summary Statistics'] = df.describe()
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
            fig, ax = plt.subplots(figsize=(8,6))
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

def main():
    st.set_page_config(page_title="Enecom IT-Data Analytics", layout="wide")
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
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
