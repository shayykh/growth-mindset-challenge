import streamlit as st
import pandas as pd
import os
import openpyxl as pxl

st.set_page_config(page_title="Growth Mindset Challenge", page_icon="🎯", layout="centered")
st.title("Growth Mindset Challenge: Web App with Streamlit")

st.header("Welcome to the Growth Mindset Challenge!")
st.write("Remember, your journey in education isn’t just about proving your intelligence—it’s about developing it. By adopting a growth mindset, you empower yourself to overcome challenges, innovate, and continuously improve. Every step you take, whether forward or backward, is part of the learning process. Embrace your potential and never stop striving to be better.")

upload_files= st.file_uploader("⬆️ Upload your files (CSV or Excel)", type=['csv','xlsx'], accept_multiple_files=True)

if upload_files:
    for file in upload_files:
        file_ext= os.path.splitext(file.name)[-1].lower()
        
        if file_ext == '.csv':
            df= pd.read_csv(file)
        elif file_ext == '.xlsx':
            df= pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext} Please upload a CSV or Excel file.")
            continue

        st.write(f"**File name:** {file.name}")
        st.write(f"**File size:** {file.size/1024} bytes")
        
        st.write("📷 Preview the head of the dataframe")
        st.dataframe(df.head())
        
        st.subheader("🧹 Data cleaning options")
        if st.checkbox(f"Clean data from {file.name}"):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"Remove duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates removed.")
            
            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols]= df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values filled.")
                    
        st.subheader("🎯 Select columns to convert")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]
        
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show data visualization for {file.name}"):
            st.write("Select the type of plot")
            plot_type = st.selectbox("Plot type", ["Line", "Bar", "Pie", "Scatter", "Histogram"])
            
            if plot_type == "Line":
                st.line_chart(df)
            elif plot_type == "Bar":
                st.bar_chart(df)
            elif plot_type == "Pie":
                st.write("Select the column to plot")
                pie_col = st.selectbox("Column", df.columns)
                st.write(df[pie_col].value_counts().plot.pie(autopct="%1.1f%%"))
            elif plot_type == "Scatter":
                st.write("Select the columns to plot")
                scatter_x = st.selectbox("X-axis", df.columns)
                scatter_y = st.selectbox("Y-axis", df.columns)  
                st.write(df.plot.scatter(x=scatter_x, y=scatter_y))
            elif plot_type == "Histogram":
                st.write("Select the column to plot")
                hist_col = st.selectbox("Column", df.columns)
                st.write(df[hist_col].plot.hist())
                
        st.subheader("🔁 Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to", ["CSV", "Excel"], key=file.name)
        
        if st.button(f"Convert {file.name} to {conversion_type}"):
            if conversion_type == "CSV":
                
                converted_data = df.to_csv(index=False)
                st.success(f"{file.name} converted to CSV")
            elif conversion_type == "Excel":
                
                converted_data = df.to_excel(index=False)
                st.success(f"{file.name} converted to Excel")

            if conversion_type == "CSV":
                st.download_button(label="⬇️ Download the converted CSV file", data=converted_data, file_name=f"{file.name}_converted.csv", mime="text/csv")
            elif conversion_type == "Excel":
                st.download_button(label="⬇️ Download the converted Excel file", data=converted_data, file_name=f"{file.name}_converted.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")