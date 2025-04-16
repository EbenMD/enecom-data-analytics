# enecom-data-analytics
README for Enecom IT-Data Analytics Web App
Enecom IT-Data Analytics Web App
The Enecom IT-Data Analytics Web App is a Streamlit-based application designed to visualize and analyze data uploaded by users. This web app allows users to upload CSV or Excel files and generate insightful visualizations, including histograms, boxplots, countplots, and pie charts. It provides easy-to-understand insights for both numerical and categorical data.

Features
Data Upload: Upload CSV or Excel files to the app.
Numerical Data Visualizations: Generates histograms and boxplots for numerical columns.
Categorical Data Visualizations: Generates countplots and pie charts for categorical columns.
Correlation Heatmap: Provides a heatmap of correlations between numerical columns.
Interactive Interface: Users can interact with the app through Streamlit's user interface to generate and view visualizations.

Installation:
Install required dependencies:
pip install -r requirements.txt

Run the app:
streamlit run app.py
Access the web app in your browser at http://localhost:8502.

Requirements
Streamlit: For building the web app interface.
Pandas: For handling data and creating DataFrames.
Matplotlib: For generating visualizations.
Seaborn: For creating statistical plots.

How to Use: 
Upload your dataset (CSV or Excel file).
Click the "Generate Insights" button to generate visualizations.
View the visualizations for both numerical and categorical columns.
The app will automatically display histograms, boxplots, countplots, and pie charts based on your data.

Contributions:
Contributions are welcome! If you have any suggestions or improvements, feel free to submit a pull request.
