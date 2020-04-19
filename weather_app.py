from tkinter import *
from tkinter import messagebox #?????????????????????????????? ^?
from configparser import ConfigParser
import requests
import base64

# Fuck it, not enjoying tkinter, and its not interesting or insightful.
# Yeah fine, I'll save the fucking images to file, what a great idea, and a waste of the fucking API
# Yeah okay, I won't have a class for the App or have it created by a function, fuck off.

def K_to_C(temp):
    return temp - 273.15


def K_to_F(temp):
    return temp * (9 / 5) - 459.67


def load_config(filename="config.ini"):
    config = ConfigParser()
    config.read(filename)
    return config


def get_api_key(config):
    return config['api_key']['key']


def search():
    city = city_text.get()
    # Simplified!
    weather = process_call(get_weather(api_query(api_key, city))) # I have literally done this in the dumbest possible way. :V
    if weather:
        location_label['text'] = f"{weather['city']}, {weather['country']}"
        temperature_label['text'] = f"{weather['C']}°C {weather['F']}°F"
        image['image'] = weather['icon']
        weather_label['text'] = weather['weather']
    else:
        messagebox.showerror("Error", f"Cannot find city: {city}")


def api_query(api_key, city_name, state=None, country_code=None):
    # Simple API call, just demonstrating use of API, not interested in trying every single type of call.
    # Example API calls:
    # api.openweathermap.org/data/2.5/weather?q={city name}&appid={your api key}
    # api.openweathermap.org/data/2.5/weather?q={city name},{state}&appid={your api key}
    # api.openweathermap.org/data/2.5/weather?q={city name},{state},{country code}&appid={your api key}
    # Oh no, how to write this prettily?
    query_components = ['http://api.openweathermap.org/data/2.5/weather?q=', f'&appid={api_key}']
    query = city_name
    if state is not None:
        query += f',{state}'
        if country_code is not None:
            query += f',{country_code}'
    return query.join(query_components)


def get_weather(query):
    # Ooh coulda used string.format(query, key)...oh well!
    result = requests.get(query)
    if result:
        return result.json()
    else:
        return None


def get_icon(icon_id):
    # Boy, it sure is a good thing I'm unnecessarily making a bunch of functions!
    icon_url = f'http://openweathermap.org/img/wn/{icon_id}@2x.png'
    icon = requests.get(icon_url).raw
    icon = base64.encodestring(icon)
    # icon = StringIO(icon)
    return icon


def process_call(answer):
    # Example answer
    # {"coord":{"lon":-0.13,"lat":51.51},
    # "weather":[{"id":300,"main":"Drizzle","description":"light intensity drizzle","icon":"09d"}],
    # "base":"stations",
    # "main":{"temp":280.32,"pressure":1012,"humidity":81,"temp_min":279.15,"temp_max":281.15},
    # "visibility":10000,
    # "wind":{"speed":4.1,"deg":80},
    # "clouds":{"all":90},
    # "dt":1485789600,
    # "sys":{"type":1,"id":5091,"message":0.0103,"country":"GB","sunrise":1485762037,"sunset":1485794875},
    # "id":2643743,
    # "name":"London",
    # "cod":200} 
    # JSON
    # We want: City, country, Weather, icon code, Temperature (C, F)
    if answer is None:
        return None
    else:
        city = answer['name']
        country = answer['sys']['country']
        weather = answer['weather'][0]['main']
        temp_K = answer['main']['temp']
        temp_C = round(K_to_C(temp_K), 1)
        temp_F = round(K_to_F(temp_K), 1)
        icon_code = answer['weather'][0]['icon']
        return {
            'city': city, 
            'country': country,
            'weather': weather,
            'C': temp_C,
            'F': temp_F,
            'icon': get_icon(icon_code)
        }


# AUGH
# # There is no definitive way to ask the root window for a list of all widgets. 
# You can use pack_slaves or grid_slaves to get a list of widgets managed by a 
# particular container, but depending on how you write your app that's no 
# guarantee you'll get all the widgets.

# God fucking damnit, root needs to not be returned, because fuck me with a rake that's goddamn why
# Fucking need to multithread. Not going to.
# Fuck tkinter (I understand, but I'm mad about other things, so fuck you, future me.)

config = load_config()
api_key = get_api_key(config)

app = Tk()
app.title("Weather app")
app.geometry('700x350')
# F U C K tkinter
app.bind('<Return>', lambda e: search())
app.bind('<Escape>', lambda x: app.destroy())

city_text = StringVar()
city_entry = Entry(app, textvariable=city_text)
city_entry.pack()

search_button = Button(app, text="Search weather", width=12, command=search)
search_button.pack()

location_label = Label(app, text="", font=('bold', 20))
location_label.pack()

image = Label(app, image='')
image.pack()

temperature_label = Label(app, text='', font=('bold', 20))
temperature_label.pack()

weather_label = Label(app, text='')
weather_label.pack()

app.mainloop()


