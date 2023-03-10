import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title("My Parents New Healthy Diner")

streamlit.header("Breakfast Favorites")
streamlit.text("Omega 3 & Blueberry Oatmeal 🥣")
streamlit.text("Kale, Spinach and Rocket Smoothie 🥗")
streamlit.text("Hard-Boiled  Free-Range Egg 🍳")
streamlit.text("Avocado Toast 🥑🍞")

streamlit.header("🍌🍍 Build your Own Fruit Smoothie 🥝")

my_fruit_df = pandas.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')

#Let's put a pick list here so they can pick the fruits they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_df['Fruit']),['Avocado','Lemon'])
fruits_to_show = my_fruit_df[my_fruit_df['Fruit'].isin(fruits_selected)]

#display the table on the page
streamlit.dataframe(fruits_to_show)

#New Section to display fruityvice api response

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

streamlit.header('Fruity Vice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:    
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)

except URLError as e:
  streamlit.error()
 
streamlit.write('The user entered ', fruit_choice)


# take the json version of the response and normalize it


# output it the screen as a table


# don't run anything past here while we troubleshoot
#streamlit.stop()

streamlit.header("View Our Fruit List - Add Your Favorites!")

def get_load_fruit_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()
 
#Add a button to load the fruit
if streamlit.button('Get fruit load list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_load_fruit_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)
           
# Allow the end user to add a fruit to the list

def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('" + new_fruit + "')")
    return "Thanks for adding " + new_fruit
  
add_my_fruit = streamlit.text_input('What fruit would you like to add','jackfruit')
if streamlit.button('Add a fruit to the list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  streamlit.text(back_from_function)


