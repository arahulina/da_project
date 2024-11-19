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

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Заголовок
st.title("Earthquake Dataset Analysis: Exploratory Data Analysis (EDA)")

# Розрахунок базової статистики
st.header("Basic Statistics")
st.write("### Summary for Numerical Columns")
st.dataframe(data.describe())

# Візуалізація розподілу ключових змінних
st.header("Distribution of Key Variables")
numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
selected_column = st.selectbox("Select a numeric column to visualize distribution:", numeric_columns)

if selected_column:
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(data[selected_column].dropna(), kde=True, ax=ax, bins=30)
    ax.set_title(f"Distribution of {selected_column}")
    st.pyplot(fig)

# Кореляційний аналіз
st.header("Correlation Analysis")
correlation_matrix = data.corr()
st.write("### Correlation Matrix")
st.dataframe(correlation_matrix)

st.write("### Heatmap of Correlations")
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
st.pyplot(fig)
