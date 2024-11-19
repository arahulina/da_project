import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Завантаження даних
@st.cache
def load_data(file):
    df = pd.read_csv(file)
    return df

st.title("Аналіз даних про землетруси")
st.sidebar.title("Навігація")
menu = st.sidebar.selectbox("Розділи", [
    "1. Підготовка даних",
    "2. Розвідувальний аналіз даних",
    "3. Геопросторовий аналіз",
    "4. Часовий аналіз",
    "5. Аналіз магнітуди та глибини",
    "6. Аналіз впливу на населення",
    "7. Прогнозне моделювання",
    "8. Висновки та рекомендації"
])

uploaded_file = st.sidebar.file_uploader("Завантажте файл з даними", type=["csv"])
if uploaded_file is not None:
    data = load_data(uploaded_file)

    if menu == "1. Підготовка даних":
        st.header("Підготовка даних")
        st.subheader("1. Завантаження датасету")
        st.write(data.head())

        st.subheader("2. Перевірка структури даних")
        st.write(data.info())

        st.subheader("3. Обробка пропущених значень")
        missing_data = data.isnull().sum()
        st.write(missing_data[missing_data > 0])
        st.write("Заповнення пропущених значень...")
        data = data.fillna(data.median())
        st.write("Пропущені значення оброблені.")

        st.subheader("4. Перевірка типів даних")
        st.write(data.dtypes)

    elif menu == "2. Розвідувальний аналіз даних":
        st.header("Розвідувальний аналіз даних")
        st.subheader("1. Базова статистика")
        st.write(data.describe())

        st.subheader("2. Візуалізація розподілу ключових змінних")
        selected_var = st.selectbox("Оберіть змінну", data.columns)
        sns.histplot(data[selected_var], kde=True)
        st.pyplot()

        st.subheader("3. Аналіз кореляцій між змінними")
        corr_matrix = data.corr()
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm")
        st.pyplot()

    elif menu == "3. Геопросторовий аналіз":
        st.header("Геопросторовий аналіз")
        st.subheader("1. Візуалізація епіцентрів землетрусів на карті")
        fig = px.scatter_mapbox(data, lat="latitude", lon="longitude", size="magnitude", color="depth",
                                mapbox_style="carto-positron")
        st.plotly_chart(fig)

    elif menu == "4. Часовий аналіз":
        st.header("Часовий аналіз")
        st.subheader("1. Частота землетрусів у часі")
        data["date"] = pd.to_datetime(data["date"])
        time_data = data.set_index("date").resample("M")["magnitude"].count()
        time_data.plot()
        st.pyplot()

    elif menu == "5. Аналіз магнітуди та глибини":
        st.header("Аналіз магнітуди та глибини")
        st.subheader("1. Розподіл землетрусів за магнітудою")
        sns.boxplot(data["magnitude"])
        st.pyplot()

    elif menu == "6. Аналіз впливу на населення":
        st.header("Аналіз впливу на населення")
        st.subheader("1. Зв'язок між силою землетрусу та кількістю постраждалих")
        sns.scatterplot(x=data["magnitude"], y=data["fatalities"])
        st.pyplot()

    elif menu == "7. Прогнозне моделювання":
        st.header("Прогнозне моделювання")
        st.subheader("1. Підготовка даних")
        X = data[["depth", "latitude", "longitude"]]
        y = data["magnitude"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        st.subheader("2. Навчання моделі")
        model = RandomForestRegressor()
        model.fit(X_train, y_train)

        st.subheader("3. Оцінка точності моделі")
        y_pred = model.predict(X_test)
        st.write("R²:", r2_score(y_test, y_pred))
        st.write("MSE:", mean_squared_error(y_test, y_pred))

    elif menu == "8. Висновки та рекомендації":
        st.header("Висновки та рекомендації")
        st.write("Проаналізуйте результати та додайте рекомендації для попередження наслідків землетрусів.")
else:
    st.info("Будь ласка, завантажте файл з даними.")

