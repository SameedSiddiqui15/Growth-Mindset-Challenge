import streamlit as st
import pandas as pd
import os 
from io import BytesIO
st.set_page_config(page_title="Sameed Python Growth Mindset",layout='wide')
# Custom CSS

st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# title & description
st.title("Datasweeper Sterling Integrator ⚙️ By Muhammad Sameed 🧑‍💻")
st.write("Effortlessly convert your files between CSV 📂 and Excel 📊 formats while leveraging built-in tools for data cleaning 🧹 and visualization 📈. This project is being developed for Quarter 3! 🚀")

# file Uploader
uplaode_files=st.file_uploader("📤 Upload Your Files (Accepts CSV 📂 or Excel 📊):",type=["csv","xlsx"],accept_multiple_files=(True))
if uplaode_files:
    for file in uplaode_files:
        file_ext =os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df =pd.read_csv(file)
        elif file_ext ==".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"unsupported file type : {file_ext}")
            continue

        st.write("🔍 Preview the first few rows of the DataFrame")
        st.dataframe(df.head())

        # data cleaning options
        st.subheader("🧹 Data Cleaning Tools & Options")
        if st.checkbox(f"🛠️ Refined Data for: {file.name} 📑"):
            col1,col2 = st.columns(2)

            with col1:
                if st.button(f"🗑️ Removing repeated entries from: {file.name} 📂"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicate entries successfully removed!")

            with col2:
                if st.button(f"📝 Fill missing data in: {file.name} 📊"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ All missing values successfully filled!")

        st.subheader("📌  Pick Columns to Keep")  
        columns = st.multiselect(f"📊 Choose columns for {file.name}" ,df.columns, default=df.columns) 
        df =df[columns]

        # data visualization
        # st.subheader("📊 Data Insights & Visualization")
        # if st.checkbox(f"📈 Display visualization for {file.name}"):
        #     st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])
        if not df.empty:
        numeric_cols = df.select_dtypes(include=['number'])
        if not numeric_cols.empty:
            st.bar_chart(numeric_cols)
        else:
            st.error("No numeric columns available for visualization.")
    else:
        st.error("Uploaded dataset is empty.")



        # conversion options    
        st.subheader("🔄 File Conversion Options")  
        conversion_type = st.radio(f"🔃 Convert {file.name} to:", ["CSV", "Excel"],key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to.csv(buffer,index=False)
                file_name = file.name.replace(file_ext,".csv")
                mime_type= "text/csv"
            elif conversion_type == "Excel":
                df.to.excel(buffer,index=False)
                file_name = file.name.replace(file_ext,".xlsx")
                mime_type= "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            st.download_button(
                label="⬇️ Downlaod " +file_name+ " as " +conversion_type,
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
st.success("All files Proceed Succesfully!")
