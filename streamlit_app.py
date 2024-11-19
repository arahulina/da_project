import streamlit as st
import pandas as pd
import numpy as np

def load_data():
    uploaded_file = st.file_uploader("Завантажте CSV файл з даними про землетруси", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write("Дані успішно завантажено!")
        return data
    return None

def check_data(data):
    if data is not None:
        st.write("Структура даних:")
        st.write(data.info())
        st.write("Пропущені значення:")
        st.write(data.isnull().sum())
        st.write("Типи даних:")
        st.write(data.dtypes)

st.title("Аналіз датасету про землетруси")
data = load_data()
check_data(data)
