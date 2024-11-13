import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium

# Завантаження даних
#data = pd.read_csv('data/earthquake_1995-2023.csv')
@st.cache_data
def load_data():
    return pd.read_csv('data/earthquake_1995-2023.csv')

data = load_data()

# Перетворення колонки з датами на формат datetime
data['date_time'] = pd.to_datetime(data['date_time'], errors='coerce')
# Додавання колонки для року
data['year'] = data['date_time'].dt.year

# Вибір мови
language = st.sidebar.selectbox("Select Language / Виберіть мову:", ["English", "Українська"])

# Тексти інтерфейсу для двох мов
text = {
    "English": {
        "title_histogram": "Histogram of Earthquake Magnitude Distribution",
        "year_selection": "Select Year:",
        "xlabel_magnitude": "Magnitude",
        "ylabel_count": "Count",
        "title_trend": "Earthquake Trend by Year",
        "yearly_count": "Number of Earthquakes Each Year",
        "scatter_depth_magnitude": "Scatter Plot: Magnitude vs. Depth of Earthquakes",
        "tsunami_relation": "Relationship Between Tsunami Occurrence, Depth, and Magnitude",
        "continent_selection": "Select Continent:",
        "year_all": "All Years",
        "continent_all": "All Continents",
        "map_title": "Interactive Earthquake Distribution Map",
        "warning_no_data": "No data for the selected continent and year.",
        "legend_title": "Legend:",
        "legend_low": "Magnitude < 4.0",
        "legend_moderate": "4.0 ≤ Magnitude < 5.0",
        "legend_high": "5.0 ≤ Magnitude < 6.0",
        "legend_very_high": "Magnitude ≥ 6.0",
        "continent_year": "Continent: {0}, Year: {1}",
        "comparison_title": "Comparison of Earthquake Counts by Country or Continent",
        "group_by": "Group by:",
        "country": "Country",
        "continent": "Continent",
        "top_countries": "Earthquake Counts by Country (Top 10)",
        "by_continent": "Earthquake Counts by Continent",
    },
    "Українська": {
        "title_histogram": "Гістограма розподілу магнітуд землетрусів",
        "year_selection": "Оберіть рік:",
        "xlabel_magnitude": "Магнітуда",
        "ylabel_count": "Кількість",
        "title_trend": "Тренд кількості землетрусів за роками",
        "yearly_count": "Кількість землетрусів за кожен рік",
        "scatter_depth_magnitude": "Розсіювання: Магнітуда проти глибини землетрусів",
        "tsunami_relation": "Залежність виникнення цунамі від глибини та магнітуди",
        "continent_selection": "Оберіть континент:",
        "year_all": "Всі роки",
        "continent_all": "Всі континенти",
        "map_title": "Інтерактивна карта розподілу землетрусів",
        "warning_no_data": "Немає даних для вибраного континенту та року.",
        "legend_title": "Легенда:",
        "legend_low": "Магнітуда < 4.0",
        "legend_moderate": "4.0 ≤ Магнітуда < 5.0",
        "legend_high": "5.0 ≤ Магнітуда < 6.0",
        "legend_very_high": "Магнітуда ≥ 6.0",
        "continent_year": "Континент: {0}, Рік: {1}",
        "comparison_title": "Порівняння кількості землетрусів за країнами або континентами",
        "group_by": "Групувати за:",
        "country": "Країною",
        "continent": "Континентом",
        "top_countries": "Кількість землетрусів за країнами (Топ-10)",
        "by_continent": "Кількість землетрусів за континентами",
    }
}

# Використання тексту відповідно до вибору мови
t = text[language]

# Заголовок для гістограми
st.title(t["title_histogram"])


# Заголовок додатку
#st.title("Гістограма розподілу магнітуд землетрусів")


# Вибір року
years = sorted(data['year'].dropna().unique())
selected_year = st.selectbox("Оберіть рік:", years)

# Фільтрація даних за вибраним роком
filtered_data = data[data['year'] == selected_year]

# Побудова гістограми
plt.figure(figsize=(10, 6))
plt.hist(filtered_data['magnitude'], bins=20, color='skyblue', edgecolor='black')
plt.title(f"Розподіл магнітуд землетрусів у {selected_year} році")
plt.xlabel("Магнітуда")
plt.ylabel("Кількість")

# Відображення гістограми у Streamlit
st.pyplot(plt)

# Перетворення колонки з датами на формат datetime та створення колонки року
data['date_time'] = pd.to_datetime(data['date_time'], errors='coerce')
data['year'] = data['date_time'].dt.year

# Підрахунок кількості землетрусів за роками
yearly_counts = data['year'].value_counts().sort_index()
yearly_counts_df = yearly_counts.reset_index()
yearly_counts_df.columns = ['Рік', 'Кількість землетрусів']

# Транспонування таблиці для горизонтального відображення
horizontal_table = yearly_counts_df.set_index('Рік').T

# Заголовок додатку
st.title("Тренд кількості землетрусів за роками")

# Побудова трендової лінії
fig, ax = plt.subplots()
ax.plot(yearly_counts.index, yearly_counts.values, marker='o', color='b')
ax.set_title('Кількість землетрусів за роками')
ax.set_xlabel('Рік')
ax.set_ylabel('Кількість землетрусів')
st.pyplot(fig)

# Виведення горизонтальної таблиці з кількістю землетрусів за роками
st.write("### Кількість землетрусів за кожен рік")
st.table(horizontal_table)

# Заголовок додатку
st.title("Розсіювання: Магнітуда проти глибини землетрусів")

# Побудова графіка розсіювання
plt.figure(figsize=(10, 6))
plt.scatter(data['depth'], data['magnitude'], alpha=0.5, c='skyblue', edgecolor='k')
plt.title("Залежність магнітуди від глибини землетрусів")
plt.xlabel("Глибина (км)")
plt.ylabel("Магнітуда")
plt.grid(True)

# Відображення графіка у Streamlit
st.pyplot(plt)

# Перевірка наявності необхідних колонок
if 'tsunami' not in data.columns or 'magnitude' not in data.columns or 'depth' not in data.columns:
    st.error("Дані не містять необхідних колонок для аналізу (tsunami, magnitude, depth).")
else:
    # Видалення пропущених значень у важливих колонках
    data = data.dropna(subset=['tsunami', 'magnitude', 'depth'])

    # Заголовок додатку
    st.title("Залежність виникнення цунамі від глибини та магнітуди землетрусу")

    # Створення графіка розсіювання
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Відображення землетрусів без цунамі
    no_tsunami = data[data['tsunami'] == 0]
    ax.scatter(no_tsunami['depth'], no_tsunami['magnitude'], color='blue', alpha=0.5, label='Без цунамі')
    
    # Відображення землетрусів з цунамі
    tsunami = data[data['tsunami'] == 1]
    ax.scatter(tsunami['depth'], tsunami['magnitude'], color='red', alpha=0.7, label='З цунамі')
    
    # Налаштування графіка
    ax.set_title("Залежність виникнення цунамі від глибини та магнітуди")
    ax.set_xlabel("Глибина (км)")
    ax.set_ylabel("Магнітуда")
    ax.legend()
    
    # Відображення графіка у Streamlit
    st.pyplot(fig)


# Перетворення колонки з датами на формат datetime та створення колонки року
data['date_time'] = pd.to_datetime(data['date_time'], errors='coerce')
data['year'] = data['date_time'].dt.year

# Заголовок додатку
st.title("Інтерактивна карта розподілу землетрусів")

# Вибір континенту з можливістю вибору всіх континентів
continents = sorted(data['continent'].dropna().unique())
continents.insert(0, "Всі континенти")
selected_continent = st.selectbox("Оберіть континент:", continents, key="continent_select")

# Вибір року з можливістю вибору всіх років
years = sorted(data['year'].dropna().unique())
years.insert(0, "Всі роки")
selected_year = st.selectbox("Оберіть рік:", years, key="year_select")

# Фільтрація даних за вибраними континентом і роком
if selected_continent == "Всі континенти":
    filtered_data = data
else:
    filtered_data = data[data['continent'] == selected_continent]

if selected_year != "Всі роки":
    filtered_data = filtered_data[filtered_data['year'] == selected_year]

# Перевірка наявності даних після фільтрації
if filtered_data.empty:
    st.warning("Немає даних для вибраного континенту та року.")
else:
    # Функція для визначення кольору залежно від магнітуди
    def magnitude_color(magnitude):
        if magnitude < 4.0:
            return 'green'
        elif 4.0 <= magnitude < 5.0:
            return 'orange'
        elif 5.0 <= magnitude < 6.0:
            return 'red'
        else:
            return 'darkred'

    # Створення базової карти з фокусом на середні координати
    m = folium.Map(location=[filtered_data['latitude'].mean(), filtered_data['longitude'].mean()], zoom_start=3)

    # Вставка CSS для зменшення білого простору після карти
    st.markdown(
    """
    <style>
    iframe {
        height: 500px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

    # Додавання точок землетрусів на карту
    for _, row in filtered_data.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=5,
            popup=f"Магнітуда: {row['magnitude']}\nГлибина: {row['depth']} км",
            color=magnitude_color(row['magnitude']),
            fill=True,
            fill_opacity=0.6
        ).add_to(m)

    # Додавання легенди на карту
    legend_html = """
         <div style="position: fixed;
                     bottom: 50px; left: 50px; width: 150px; height: 150px;
                     background-color: white; border:2px solid grey; z-index:9999; font-size:14px;
                     ">
         &nbsp; <b>Легенда:</b> <br>
         &nbsp; <i style="color:green;">●</i> Магнітуда < 4.0 <br>
         &nbsp; <i style="color:orange;">●</i> 4.0 ≤ Магнітуда < 5.0 <br>
         &nbsp; <i style="color:red;">●</i> 5.0 ≤ Магнітуда < 6.0 <br>
         &nbsp; <i style="color:darkred;">●</i> Магнітуда ≥ 6.0
         </div>
         """
    m.get_root().html.add_child(folium.Element(legend_html))

    # Відображення карти у Streamlit
    st.write(f"Континент: {selected_continent}, Рік: {selected_year}")
    st_folium(m, width=700, height=500)

# Заголовок додатку
st.title("Порівняння кількості землетрусів за країнами або континентами")

# Вибір групування: за країнами або континентами
group_by_option = st.radio("Групувати за:", ['Країною', 'Континентом'])

# Групування та підрахунок
if group_by_option == 'Країною':
    data_grouped = data['country'].value_counts().dropna().head(10)  # Топ-10 країн
    ylabel = "Кількість землетрусів"
    title = "Кількість землетрусів за країнами (Топ-10)"
else:
    data_grouped = data['continent'].value_counts().dropna()
    ylabel = "Кількість землетрусів"
    title = "Кількість землетрусів за континентами"

# Побудова стовпчикової діаграми
plt.figure(figsize=(10, 6))
data_grouped.plot(kind='bar', color='skyblue', edgecolor='black')
plt.xlabel(group_by_option)
plt.ylabel(ylabel)
plt.title(title)
plt.xticks(rotation=45)

# Відображення графіка у Streamlit
st.pyplot(plt)
