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

   # Перевірка пропущених значень
    st.subheader("Перевірка пропущених значень")
    missing_values = df.isnull().sum()
    st.write(missing_values[missing_values > 0])

    # Вибір методу заповнення пропущених значень
    st.subheader("Заповнення пропущених значень")
    fill_method = st.selectbox("Оберіть метод заповнення", ["Не заповнювати", "Середнє значення", "Медіана", "Мода", "Інтерполяція"])

    if fill_method == "Середнє значення":
        df.fillna(df.mean(), inplace=True)
        st.write("Пропущені значення заповнено середнім значенням.")
    elif fill_method == "Медіана":
        df.fillna(df.median(), inplace=True)
        st.write("Пропущені значення заповнено медіаною.")
    elif fill_method == "Мода":
        for column in df.columns:
            df[column].fillna(df[column].mode()[0], inplace=True)
        st.write("Пропущені значення заповнено модою.")
    elif fill_method == "Інтерполяція":
        df.interpolate(method='linear', inplace=True)
        st.write("Пропущені значення заповнено методом інтерполяції.")
    
    # Перевірка типів даних
    st.subheader("Перевірка типів даних")
    st.write(df.dtypes)

