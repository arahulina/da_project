import streamlit as st
import pandas as pd

# Заголовок додатку
st.title("Аналіз даних землетрусів 1995-2023")

# Завантаження файлу
uploaded_file = "data/earthquake_1995-2023.csv"

# Перевірка, чи завантажений файл
if uploaded_file is not None:
    # Завантаження даних
    df = pd.read_csv(uploaded_file)

    # Відображення перших кількох рядків даних
    st.subheader("Перегляд даних")
    st.write(df.head())

    # Перевірка структури даних
    st.subheader("Структура даних")
    st.write(df.info())

    # Перевірка пропущених значень
    st.subheader("Перевірка пропущених значень")
    missing_values = df.isnull().sum()
    st.write(missing_values[missing_values > 0])

    # Заповнення або видалення пропущених значень (опційно)
    if st.button("Заповнити пропущені значення"):
        df.fillna(0, inplace=True)
        st.write("Пропущені значення замінено на 0.")
        st.write(df.isnull().sum())

    # Перевірка типів даних
    st.subheader("Перевірка типів даних")
    st.write(df.dtypes)

    # Вибіркове перетворення типів (опційно)
    st.write("Коригування типів даних, якщо потрібно:")
    for col in df.select_dtypes(include=['object']).columns:
        if st.checkbox(f"Перетворити '{col}' на числовий тип"):
            df[col] = pd.to_numeric(df[col], errors='coerce')
            st.write(f"Колонка '{col}' перетворена на числовий тип.")
else:
    st.write("Будь ласка, завантажте файл CSV для аналізу.")
