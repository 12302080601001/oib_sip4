import tkinter as tk
from tkinter import messagebox, ttk
import requests

# Function to fetch weather data
def get_weather_data(api_key, location):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP request errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return {}

# Function to validate location input
def validate_location(location):
    return location.strip() != ""

# Function to fetch and display weather
def fetch_weather():
    api_key = api_key_entry.get()
    location = location_entry.get()
    
    if not api_key:
        messagebox.showerror("Error", "API key is required")
        return
    
    if not validate_location(location):
        messagebox.showerror("Error", "Invalid location")
        return

    # Show loading indicator
    loading_indicator.start()
    fetch_button.config(state=tk.DISABLED)
    
    data = get_weather_data(api_key, location)
    
    # Hide loading indicator
    loading_indicator.stop()
    fetch_button.config(state=tk.NORMAL)
    
    if data.get("cod") != 200:
        messagebox.showerror("Error", "Location not found")
        return

    weather_description = data['weather'][0]['description']
    temperature = data['main']['temp']
    weather_label.config(text=f"Weather in {location}: {weather_description.capitalize()}\nTemperature: {temperature}°C")

# Create the main window
root = tk.Tk()
root.title("Weather App")
root.configure(bg='#87CEFA')  # Sky blue background

# API Key Entry
api_key_label = tk.Label(root, text="Enter API Key:", bg='#87CEFA', fg='#000080', font=("Arial", 12, "bold"))
api_key_label.pack(pady=10)

api_key_entry = tk.Entry(root, font=("Arial", 12), bg='#FFFFFF', fg='#000000', bd=2, relief="solid")
api_key_entry.pack(pady=5, padx=20, fill=tk.X)

# Location Entry
location_label = tk.Label(root, text="Enter Location:", bg='#87CEFA', fg='#000080', font=("Arial", 12, "bold"))
location_label.pack(pady=10)

location_entry = tk.Entry(root, font=("Arial", 12), bg='#FFFFFF', fg='#000000', bd=2, relief="solid")
location_entry.pack(pady=5, padx=20, fill=tk.X)

# Fetch Weather Button
fetch_button = tk.Button(root, text="Get Weather", command=fetch_weather, bg='#00BFFF', fg='#FFFFFF', font=("Arial", 12, "bold"), relief="raised", bd=2)
fetch_button.pack(pady=10, padx=20)

# Loading Indicator
loading_indicator = ttk.Progressbar(root, mode='indeterminate')
loading_indicator.pack(pady=10)

# Weather Display Label
weather_label = tk.Label(root, text="", font=("Arial", 14, "bold"), bg='#87CEFA', fg='#000080')
weather_label.pack(pady=10)

# Start the GUI event loop
root.mainloop()
