import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

def generate_insights(df):
    """Generates insights from the DataFrame."""

    insights = {}

    insights['Summary Statistics'] = df.describe()

    # Basic visualizations
    try:
        num_cols = df.select_dtypes(include=['number']).columns
        cat_cols = df.select_dtypes(exclude=['number']).columns

        if len(num_cols) > 0:
            insights['Histograms'] = {}
            for col in num_cols:
                fig, ax = plt.subplots()
                sns.histplot(df[col], ax=ax)
                insights['Histograms'][col] = fig

            if len(num_cols) >= 2:
                fig, ax = plt.subplots()
                sns.scatterplot(data=df, x=num_cols[0], y=num_cols[1], ax=ax)
                insights['Scatterplot'] = fig

            if len(num_cols) > 0 and len(cat_cols) > 0:
                fig, ax = plt.subplots()
                sns.boxplot(data=df, x=cat_cols[0], y=num_cols[0], ax=ax)
                insights['Boxplot'] = fig

        if len(cat_cols) > 0:
            insights['Value Counts'] = {}
            for col in cat_cols:
                insights['Value Counts'][col] = df[col].value_counts()
                fig, ax = plt.subplots()
                sns.countplot(x=df[col], ax=ax)
                insights['Countplot_'+col] = fig

        if len(num_cols) > 1:
            fig, ax = plt.subplots()
            sns.heatmap(df[num_cols].corr(), annot=True, ax=ax)
            insights['Correlation Heatmap'] = fig

    except Exception as e:
        insights['Visualization Error'] = f"Error generating visualizations: {e}"

    return insights

def display_insights(insights):
    """Displays the generated insights."""

    for key, value in insights.items():
        st.subheader(key)
        if isinstance(value, pd.DataFrame) or isinstance(value, pd.Series):
            st.dataframe(value)
        elif isinstance(value, dict):
            for sub_key, sub_value in value.items():
                st.write(f"**{sub_key}**")
                if isinstance(sub_value, pd.Series):
                    st.dataframe(sub_value)
                elif isinstance(sub_value, plt.Figure):
                     st.pyplot(sub_value)
        elif isinstance(value, plt.Figure):
            st.pyplot(value)
        else:
            st.write(value)

def main():
    st.title("Enecom IT Solutions - Data Analytics Web App")

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
                insights = generate_insights(df)
                display_insights(insights)

            if st.button("Download Report as CSV"):
                insights_df = pd.DataFrame()
                for key, value in generate_insights(df).items():
                    if isinstance(value, pd.DataFrame) or isinstance(value, pd.Series):
                        flattened_data = value.to_frame().reset_index()
                        flattened_data['report_section'] = key
                        insights_df = pd.concat([insights_df, flattened_data], ignore_index = True)
                csv_buffer = io.StringIO()
                insights_df.to_csv(csv_buffer, index=False)
                st.download_button(
                    label="Download Report as CSV",
                    data=csv_buffer.getvalue(),
                    file_name="data_report.csv",
                    mime="text/csv",
                )
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
