import streamlit

streamlit.title("My Parents New Healthy Diner")

streamlit.header("Breakfast Favorites")
streamlit.text("Omega 3 & Blueberry Oatmeal 🥣")
streamlit.text("Kale, Spinach and Rocket Smoothie 🥗")
streamlit.text("Hard-Boiled  Free-Range Egg 🍳")
streamlit.text("Avocado Toast 🥑🍞")

streamlit.header("🍌🍍 Build your Own Fruit Smoothie 🥝")

import pandas
my_fruit_df = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')

#Let's put a pick list here so they can pick the fruits they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_df['Fruit']),['Avocado','Lemon'])
fruits_to_show = my_fruit_df[my_fruit_df['Fruit'].isin(fruits_selected)]

#display the table on the page
streamlit.dataframe(fruits_to_show)

#New Section to display fruityvice api response

streamlit.header('Fruity Vice Fruit Advice!')
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

import requests

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

# take the json version of the response and normalize it
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

# output it the screen as a table
streamlit.dataframe(fruityvice_normalized)

import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST")
my_data_rows = my_cur.fetchall()
streamlit.dataframe(my_data_rows)
