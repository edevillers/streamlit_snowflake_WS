import streamlit as st
import pandas as pd
import requests
import snowflake.connector

st.title("My Parents New Healthy Diner")

st.header("Breakfast Favorites")
st.text("🥣 Omega 3 & Blueberry Oatmeal")
st.text("🥗 Kale, Spinach & Rocket Smoothie")
st.text("🐔 Hard-Boiled Free-range Egg")
st.text("🥑🍞 Avocado Toast")

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruit_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruit_selected]

st.dataframe(fruits_to_show)


st.header("Fruityvice Fruit Advice !")
fruit_choice = st.text_input('What fruit would you like information about?', 'Kiwi')
st.write('The user entered', fruit_choice)


fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)


#  normalise le fruityvice
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# et l'affiche come df
st.dataframe(fruityvice_normalized)

# essayer de se brancher à snowflake
my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchall()
st.header("The fruit load list contains:")
st.dataframe(my_data_row)

add_my_fruit = st.text_input('What fruit would you like to add?')
st.text('Thanks for adding ' + add_my_fruit)

#
my_cur.execute("insert into fruit_load_list values ('from streamlit')")