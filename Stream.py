import streamlit as st
import pymysql
import pandas as pd

# Function to get a database connection
def get_connection():
    return pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='2210',
        db='redbusproject',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# Function to fetch data from the database
def fetch_data(query):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return pd.DataFrame(result)
    finally:
        connection.close()

# Streamlit app
st.title("RedBus Data")

# Fetch unique values for filters
bustype_query = "SELECT DISTINCT bustype FROM redbusdetails"
route_query = "SELECT DISTINCT route_name FROM redbusdetails"
bustypes = fetch_data(bustype_query)['bustype'].tolist()
routes = fetch_data(route_query)['route_name'].tolist()

# Sidebar filters
st.sidebar.header("Filter options")
selected_bustype = st.sidebar.selectbox("Bus Type", ["All"] + bustypes)
selected_route = st.sidebar.selectbox("Route", ["All"] + routes)
price_range = st.sidebar.slider("Price Range", 0, 5000, (0, 5000))
min_rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 0.0)
available_seats = st.sidebar.slider("Minimum Seats Available", 0, 50, 0)

# Base query
query = "SELECT id, Transport, route_name, route_link, Date, busname, bustype, departing_time, duration, bp_time, star_rating, price, seats_available FROM redbusdetails WHERE 1=1"

# Apply filters to query
if selected_bustype != "All":
    query += f" AND bustype = '{selected_bustype}'"
if selected_route != "All":
    query += f" AND route_name = '{selected_route}'"
query += f" AND price BETWEEN {price_range[0]} AND {price_range[1]}"
query += f" AND star_rating >= {min_rating}"
query += f" AND seats_available >= {available_seats}"

# Fetch and display data
data = fetch_data(query)
st.write("Filtered data from redbusdetails table:")
st.dataframe(data)
