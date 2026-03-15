import tkinter as tk
from PIL import Image, ImageTk
import requests
from bs4 import BeautifulSoup
import io

# МОДЕЛЬ
def get_data_weather():
    url = "https://www.gismeteo.by/weather-novopolotsk-11026/"
    headers = {'User-Agent': 'Mozilla/5.0'} 

    try:
       response = requests.get(url, headers=headers) 
       soup = BeautifulSoup(response.text, "html.parser")
       
       # Пытаемся найти данные. Если классы изменятся, вернем дефолт
       temp_tag = soup.select_one(".unit_temperature_c")
       wind_tag = soup.select_one(".wind-unit .speed-value") # Уточненный путь для ветра

       temp = temp_tag.text if temp_tag else "?"
       wind = wind_tag.text if wind_tag else "?"

       return temp, wind
    except Exception as e:
       print(f"Произошла ошибка при парсинге: {e}")
       return "err", "err"

# КОНТРОЛЛЕР
def update_display():
   temp, wind = get_data_weather()
   temp_label.config(text=f"{temp} C")
   wind_label.config(text=f"скорость ветра {wind} м/с")

# ВИД
root = tk.Tk() 
root.title("Погодка В НП")
root.geometry("350x300")

# Используем Arial, так как он точно есть на твоем Mac
title = tk.Label(root, text="Новополоцк", font=("Arial", 20, "bold"))
title.pack(pady=10)

temp_label = tk.Label(root, text="-- C", font=("Arial", 30))
temp_label.pack()

wind_label = tk.Label(root, text="скорость ветра --", font=("Arial", 14))
wind_label.pack(pady=10)

btn = tk.Button(root, text="Обновить данные", command=update_display)
btn.pack(pady=20)

# Запуск
root.mainloop()