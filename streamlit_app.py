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

import matplotlib.pyplot as plt
import seaborn as sns

def exploratory_analysis(data):
    if data is not None:
        st.subheader("Базова статистика")
        st.write(data.describe())

        st.subheader("Візуалізація розподілу ключових змінних")
        for column in data.select_dtypes(include=[np.number]).columns:
            fig, ax = plt.subplots()
            sns.histplot(data[column], kde=True, ax=ax)
            st.pyplot(fig)

        st.subheader("Кореляційна матриця")
        corr = data.corr()
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

exploratory_analysis(data)