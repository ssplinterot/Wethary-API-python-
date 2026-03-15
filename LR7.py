"""
Программа «Погода онлайн» с визуализацией 
Получение данных при помощи парсинга, визуализация температуры, давления,
иконки погоды и обновление данных.
"""
import tkinter as tk
from PIL import Image, ImageTk #библиотека обработки изображений.
import requests #Отправляет HTTP-запросы к веб-серверам
from bs4 import BeautifulSoup #«разбор» (парсинг) полученного HTML-кода
import io #Для работы с картинкой в памяти (без сохранения на диск)
  

def get_data_weather():
    url = "https://www.gismeteo.by/weather-novopolotsk-11026/now/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'} #Чтобы сайт думал, что зашел человек с браузера, а не робот
    current_icon = None

    try:
       response = requests.get(url, headers=headers) 

       if response.status_code != 200:
           print(f"Ошибка доступа! Сайт вернул HTTP-код: {response.status_code}")
           return "err", "err"
       
       soup = BeautifulSoup(response.text, "html.parser")

       # --- Температура ---
       temp_node = soup.find("temperature-value")
       temp = temp_node.get("value") if temp_node else "?" # Берем данные из атрибута value        
       if temp != "?" and int(temp) > 0:
            temp = f"+{temp}"# добавим плюс, если температура больше нуля

        # --- Ветер ---
       wind_node = soup.find("speed-value")
       wind = wind_node.get("value") if wind_node else "?"

       # --- Давление ---
       pressure_node = soup.find("pressure-value")
       pressure = pressure_node.get("value") if pressure_node else "?"

       # --- Описание ---
       desc_node = soup.find(class_="now-desc")
       desc = desc_node.text.strip() if desc_node else "?"#stip() для удаление пробелов

       return temp, wind, pressure, desc
    except Exception as e:
       print(f"Произошла ошибка: {e}")
       return "?", "?", "?", "?"

def update_display():
   temp, wind, pressure, desc = get_data_weather()

   temp_label.config(text=f"{temp} °C")
   wind_label.config(text = f"скорость ветра {wind} км/ч")
   pressure_label.config(text=f"давление {pressure} мм рт. ст.")
   desc_label.config(text=f"{desc}")

   filename = ""
   if "Ясно" in desc or "Безоблачно" in desc:
       filename = "sun.png"
   elif "Пасмурно" in desc or "Облачно" in desc or "Малооблачно" in desc:
       filename = "cloudy.png"
   elif "Дождь" in desc or "Ветренно" in desc:
       filename = "rain.png"

   if filename:
       try:
           img = Image.open(filename)
           img = img.resize((100,100))
           tk_img = ImageTk.PhotoImage(img)
           icon_label.config(image= tk_img)
           icon_label.image = tk_img

       except Exception as e:
        print(f"Не удалось загрузить картинку: {e}")

root = tk.Tk() 
root.title("Погодка В НП")
root.geometry("400x350")
title = tk.Label(root, text="Новополцк", font=("JMH Typewriter", 20))
title.pack(pady=10)

icon_label = tk.Label(root)
icon_label.pack()

temp_label = tk.Label(root, text="-- °C", font=("JMH Typewriter", 20))
temp_label.pack()

desc_label = tk.Label(root, text="описание", font=("JMH Typewriter", 20))
desc_label.pack()

wind_label = tk.Label(root, text="скорость ветра --", font=("JMH Typewriter", 20))
wind_label.pack()

pressure_label = tk.Label(root, text="давление --", font=("JMH Typewriter", 20))
pressure_label.pack()

btn = tk.Button(root, text="Обновить", command=update_display)
btn.pack()

root.mainloop()

