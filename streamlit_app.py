import pandas as pd
import streamlit as st
from io import StringIO
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px



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
numeric_columns = numeric_columns.fillna(numeric_columns.median())

# Кореляційний аналіз
st.header("Correlation Analysis")
correlation_matrix = numeric_columns.corr()

st.write("### Correlation Matrix")
st.dataframe(correlation_matrix)

st.write("### Heatmap of Correlations")
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
st.pyplot(fig)

# Streamlit app continuation from previous code

# 3. Geospatial Analysis
# 3. Geospatial Analysis
st.header("3. Геопросторовий аналіз")
st.subheader("Візуалізація епіцентрів землетрусів на карті")

# Ініціалізація змінної geo_data як порожнього DataFrame для уникнення помилок
geo_data = pd.DataFrame()

# Перевірка на наявність стовпців Latitude і Longitude
if 'Latitude' in data.columns and 'Longitude' in data.columns:
    # Видалення рядків з порожніми значеннями Latitude або Longitude
    geo_data = data.dropna(subset=['Latitude', 'Longitude'])

    # Карта епіцентрів землетрусів з позначенням магнітуди
    fig = px.scatter_mapbox(
        geo_data, lat="Latitude", lon="Longitude", hover_name="Location", 
        color="Magnitude", size="Magnitude",
        color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=1
    )
    fig.update_layout(mapbox_style="open-street-map")  # Використовуємо стиль, що не потребує API-ключа
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)
else:
    st.error("Стовпці Latitude та Longitude відсутні у даних.")

# Аналіз кластерів землетрусів (використання DBSCAN для кластеризації)
st.subheader("Аналіз кластерів землетрусів")

# Перевірка наявності даних для кластеризації
if not geo_data.empty:
    from sklearn.cluster import DBSCAN
    from sklearn.preprocessing import StandardScaler

    # Підготовка даних для кластеризації
    coords = geo_data[['Latitude', 'Longitude']]
    scaler = StandardScaler()
    coords_scaled = scaler.fit_transform(coords)

    # DBSCAN для кластеризації з візуалізацією результатів
    db = DBSCAN(eps=0.5, min_samples=5).fit(coords_scaled)
    geo_data['Cluster'] = db.labels_

    # Візуалізація кластерів на карті
    fig = px.scatter_mapbox(
        geo_data, lat="Latitude", lon="Longitude", hover_name="Location", 
        color="Cluster", size="Magnitude", zoom=1, size_max=10,
        color_continuous_scale=px.colors.sequential.Viridis
    )
    fig.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig)
else:
    st.error("Недостатньо даних для кластеризації.")

# Дослідження зв'язку між географічним положенням та силою землетрусів
st.subheader("Зв'язок між географічним положенням та силою землетрусів")

# Перевірка, що стовпці Latitude, Longitude і Magnitude існують і містять дані
if not geo_data.empty and 'Magnitude' in geo_data.columns:
    fig = px.scatter(
        geo_data, x="Longitude", y="Latitude", color="Magnitude",
        color_continuous_scale=px.colors.cyclical.IceFire, title="Зв'язок між місцем і силою землетрусу"
    )
    st.plotly_chart(fig)
else:
    st.error("Стовпець Magnitude відсутній або має некоректні дані.")


# 4. Time Series Analysis
st.header("4. Часовий аналіз")
st.subheader("Аналіз частоти землетрусів у часі")

# Перевірка та конвертація дати
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
data = data.dropna(subset=['Date'])  # Видалення некоректних дат

# Групування за датою для аналізу частоти
data['Year'] = data['Date'].dt.year
yearly_counts = data.groupby('Year').size()

# Графік частоти землетрусів по роках
fig, ax = plt.subplots()
yearly_counts.plot(kind='bar', ax=ax, color='skyblue')
ax.set_title("Кількість землетрусів по роках")
ax.set_xlabel("Рік")
ax.set_ylabel("Кількість землетрусів")
st.pyplot(fig)

# Виявлення сезонних паттернів
st.subheader("Сезонні паттерни землетрусів")
data['Month'] = data['Date'].dt.month
monthly_counts = data.groupby('Month').size()

# Графік частоти землетрусів по місяцях
fig, ax = plt.subplots()
monthly_counts.plot(kind='bar', ax=ax, color='coral')
ax.set_title("Кількість землетрусів по місяцях")
ax.set_xlabel("Місяць")
ax.set_ylabel("Кількість землетрусів")
st.pyplot(fig)

# Довгострокові тренди
st.subheader("Довгострокові тренди землетрусів")
fig, ax = plt.subplots()
yearly_counts.rolling(window=5).mean().plot(ax=ax, color='purple')
ax.set_title("5-річне ковзне середнє частоти землетрусів")
ax.set_xlabel("Рік")
ax.set_ylabel("Середнє значення частоти")
st.pyplot(fig)

# 5. Analysis of Magnitude and Depth
st.header("5. Аналіз магнітуди та глибини")
st.subheader("Розподіл землетрусів за магнітудою")

# Розподіл магнітуди
fig, ax = plt.subplots()
sns.histplot(data['Magnitude'], kde=True, ax=ax, color="blue")
ax.set_title("Розподіл магнітуди землетрусів")
ax.set_xlabel("Магнітуда")
ax.set_ylabel("Частота")
st.pyplot(fig)

# Зв'язок між глибиною та магнітудою
st.subheader("Зв'язок між глибиною та магнітудою")
fig, ax = plt.subplots()
sns.scatterplot(x=data['Depth'], y=data['Magnitude'], ax=ax, color="green")
ax.set_title("Глибина vs Магнітуда")
ax.set_xlabel("Глибина (км)")
ax.set_ylabel("Магнітуда")
st.pyplot(fig)

# Виявлення аномальних значень
st.subheader("Виявлення аномальних значень у магнітуді та глибині")
threshold = st.slider("Значення для виявлення аномальних значень", min_value=6.0, max_value=10.0, value=7.0)
outliers = data[data['Magnitude'] > threshold]
st.write("Землетруси з магнітудою більше", threshold)
st.write(outliers[['Date', 'Location', 'Magnitude', 'Depth']])

# Наступні розділи (Аналіз впливу на населення та Прогнозне моделювання) будуть додані нижче
