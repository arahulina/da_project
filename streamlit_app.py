import pandas as pd
import streamlit as st
from io import StringIO
import seaborn as sns
import matplotlib.pyplot as plt


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



# Заголовок
st.title("Earthquake Dataset Analysis: Exploratory Data Analysis (EDA)")

# Вибір числових колонок
numeric_columns = data.select_dtypes(include=['float64', 'int64'])

# Заповнення пропущених значень
# Заповнюємо середнім для кожної числової колонки
numeric_columns = numeric_columns.fillna(numeric_columns.mean())

# Кореляційний аналіз
st.header("Correlation Analysis")
correlation_matrix = numeric_columns.corr()

st.write("### Correlation Matrix")
st.dataframe(correlation_matrix)

st.write("### Heatmap of Correlations")
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
st.pyplot(fig)

