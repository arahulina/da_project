import pandas as pd
import streamlit as st
from io import StringIO

# Завантаження даних
file_path = 'data/earthquake_1995-2023.csv'
data = pd.read_csv(file_path)

# Заголовок додатку
st.title("Earthquake Dataset Analysis: Data Preparation")

# Виведення загальної інформації про датасет
st.header("Dataset Overview")
st.write("### First 5 Rows of the Dataset")
st.dataframe(data.head())

st.write("### Dataset Dimensions")
st.write(f"Rows: {data.shape[0]}, Columns: {data.shape[1]}")

st.write("### Dataset Information")
# Використання StringIO для виводу data.info()
buffer = StringIO()
data.info(buf=buffer)
st.text(buffer.getvalue())  # Виводимо результат у Streamlit

# Перевірка пропущених значень
st.header("Missing Values")
missing_values = data.isnull().sum()
st.write("### Count of Missing Values in Each Column")
st.dataframe(missing_values[missing_values > 0].rename("Missing Count"))

# Основні статистичні показники
st.header("Basic Statistical Summary")
st.write("### Numerical Columns Summary")
st.dataframe(data.describe())

# Унікальні значення в ключових стовпцях
st.header("Unique Values in Key Columns")
key_columns = ['year', 'latitude', 'longitude', 'depth', 'magnitude']  # Оновіть список за потреби
selected_column = st.selectbox("Select a column to view unique values:", key_columns)

if selected_column in data.columns:
    unique_values = data[selected_column].dropna().unique()
    st.write(f"### Unique Values in `{selected_column}` (first 10):")
    st.write(unique_values[:10])  # Показуємо перші 10 значень
else:
    st.write("Selected column is not in the dataset.")

