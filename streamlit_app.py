# Код для створення додатку Streamlit для аналізу землетрусів

## 1. Підготовка даних


import streamlit as st
import pandas as pd
import numpy as np
import os

# Load and display data
@st.cache
def load_data():
    data = pd.read_csv('data/earthquake_1995-2023.csv')
    return data

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


## 2. Розвідувальний аналіз даних


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


## 3. Геопросторовий аналіз


import folium
from streamlit_folium import folium_static

def geo_analysis(data):
    if data is not None and 'latitude' in data.columns and 'longitude' in data.columns:
        st.subheader("Карта епіцентрів землетрусів")
        m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=2)
        for idx, row in data.iterrows():
            folium.CircleMarker([row['latitude'], row['longitude']], 
                                radius=5, 
                                popup=f"Magnitude: {row['magnitude']}",
                                color="red", 
                                fill=True).add_to(m)
        folium_static(m)

geo_analysis(data)


## 4. Часовий аналіз


def time_analysis(data):
    if data is not None and 'date' in data.columns:
        data['date'] = pd.to_datetime(data['date'])
        data.set_index('date', inplace=True)

        st.subheader("Частота землетрусів у часі")
        fig, ax = plt.subplots()
        data.resample('M').size().plot(ax=ax)
        st.pyplot(fig)

        st.subheader("Сезонний аналіз")
        seasonal = data.groupby(data.index.month).size()
        fig, ax = plt.subplots()
        seasonal.plot(kind='bar', ax=ax)
        st.pyplot(fig)

time_analysis(data)


## 5. Аналіз магнітуди та глибини


def magnitude_depth_analysis(data):
    if data is not None and 'magnitude' in data.columns and 'depth' in data.columns:
        st.subheader("Розподіл землетрусів за магнітудою")
        fig, ax = plt.subplots()
        sns.histplot(data['magnitude'], kde=True, ax=ax)
        st.pyplot(fig)

        st.subheader("Зв'язок між глибиною та магнітудою")
        fig, ax = plt.subplots()
        sns.scatterplot(x='depth', y='magnitude', data=data, ax=ax)
        st.pyplot(fig)

        st.subheader("Аномальні значення")
        Q1 = data['magnitude'].quantile(0.25)
        Q3 = data['magnitude'].quantile(0.75)
        IQR = Q3 - Q1
        outliers = data[(data['magnitude'] < (Q1 - 1.5 * IQR)) | (data['magnitude'] > (Q3 + 1.5 * IQR))]
        st.write(outliers)

magnitude_depth_analysis(data)


## 6. Аналіз впливу на населення


def impact_analysis(data):
    if data is not None and 'magnitude' in data.columns and 'casualties' in data.columns:
        st.subheader("Зв'язок між силою землетрусу та кількістю постраждалих")
        fig, ax = plt.subplots()
        sns.scatterplot(x='magnitude', y='casualties', data=data, ax=ax)
        st.pyplot(fig)

        if 'economic_loss' in data.columns:
            st.subheader("Аналіз економічних збитків")
            fig, ax = plt.subplots()
            sns.scatterplot(x='magnitude', y='economic_loss', data=data, ax=ax)
            st.pyplot(fig)

impact_analysis(data)


## 7. Прогнозне моделювання


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def predictive_modeling(data):
    if data is not None and 'magnitude' in data.columns:
        st.subheader("Прогнозне моделювання")
        
        features = ['depth', 'latitude', 'longitude']
        X = data[features]
        y = data['magnitude']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = LinearRegression()
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        st.write("Середньоквадратична помилка:", mean_squared_error(y_test, y_pred))
        st.write("R2 score:", r2_score(y_test, y_pred))

        st.write("Коефіцієнти моделі:")
        for feature, coef in zip(features, model.coef_):
            st.write(f"{feature}: {coef}")

predictive_modeling(data)


## 8. Висновки та рекомендації


def conclusions():
    st.subheader("Висновки та рекомендації")
    st.write("На основі проведеного аналізу можна зробити наступні висновки:")
    conclusions = st.text_area("Введіть ваші висновки тут")
    st.write("Рекомендації для зменшення ризиків:")
    recommendations = st.text_area("Введіть ваші рекомендації тут")
    st.write("Напрямки для подальших досліджень:")
    future_research = st.text_area("Введіть напрямки для подальших досліджень тут")

conclusions()

if __name__ == "__main__":
    st.sidebar.title("Навігація")
    pages = {
        "Підготовка даних": load_data,
        "Розвідувальний аналіз": exploratory_analysis,
        "Геопросторовий аналіз": geo_analysis,
        "Часовий аналіз": time_analysis,
        "Аналіз магнітуди та глибини": magnitude_depth_analysis,
        "Аналіз впливу на населення": impact_analysis,
        "Прогнозне моделювання": predictive_modeling,
        "Висновки та рекомендації": conclusions
    }
    selection = st.sidebar.radio("Перейти до", list(pages.keys()))
    page = pages[selection]
    page()
