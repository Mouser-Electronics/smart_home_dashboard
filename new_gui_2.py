import tkinter as tk
from tkinter import ttk
from datetime import datetime
import time
import sensorData_3

from pygame import mixer

HEIGHT = 480
WIDTH = 720

mixer.init()


root = tk.Tk()
style = ttk.Style()


global temperature_label
global degree_label
global temperature_name

global humidity_label
global humidity_name

global lux_label
global lux_name

global audio_label
global audio_name

global calendar_label

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, bg='#d3d2d2')
canvas.pack()


temperature_image = tk.PhotoImage(file = r"/home/pi/Smart Home dashboard/gui figures/temperature_2.png") 
button_temperature = tk.Button(canvas, image=temperature_image, borderwidth=0, bg='#d3d2d2', activebackground='#c5c5c5', command=lambda: show_temperature())
button_temperature.place(relx=0.017, rely=0.047, relwidth=0.25, relheight=0.45)

humidity_image = tk.PhotoImage(file = r"/home/pi/Smart Home dashboard/gui figures/humidity_2.png") 
button_humidity = tk.Button(canvas, image=humidity_image, borderwidth=0, bg='#d3d2d2', activebackground='#c5c5c5', command=lambda: show_humidity())
button_humidity.place(relx=0.257, rely=0.047, relwidth=0.25, relheight=0.45)


lux_image = tk.PhotoImage(file = r"/home/pi/Smart Home dashboard/gui figures/Lux_2.png") 
button_lux = tk.Button(canvas, image=lux_image, borderwidth=0, bg='#d3d2d2', activebackground='#c5c5c5', command=lambda: show_lux())
button_lux.place(relx=0.017, rely=0.5, relwidth=0.25, relheight=0.45)

audio_image = tk.PhotoImage(file = r"/home/pi/Smart Home dashboard/gui figures/audio_2.png") 
button_audio = tk.Button(canvas, image=audio_image, borderwidth=0, bg='#d3d2d2', activebackground='#c5c5c5', command=lambda: show_audio())
button_audio.place(relx=0.257, rely=0.5, relwidth=0.25, relheight=0.45)

rectangle_image = tk.PhotoImage(file = r"/home/pi/Smart Home dashboard/gui figures/rectangle_background_2.png")
rectangle_label = tk.Label(canvas, image=rectangle_image, borderwidth=0, bg='#d3d2d2', activebackground='#d3d2d2')
rectangle_label.place(relx=0.5, rely=0, relwidth=0.48, relheight=1)

time = tk.Label(canvas, font=("Helvetica 24 bold"), fg='white', bg='#3f66b0')
time.place(relx=0.67, rely=0.16, relwidth=0.15, relheight=0.08)

date = tk.Label(canvas, font=("Helvetica 22 bold"), fg='white', bg='#3f66b0')
date.place(relx=0.55, rely=0.24, relwidth=0.38, relheight=0.08)

calendar_image = tk.PhotoImage(file = r"/home/pi/Smart Home dashboard/gui figures/calendar.png")
calendar_label = tk.Label(canvas, image=calendar_image, borderwidth=0, bg='#d3d2d2', activebackground='#d3d2d2')
calendar_label.place(relx=0.5, rely=0.48, relwidth=0.48, relheight=0.45)


#################################################################

temperature_label = tk.Label(canvas, font=("Helvetica", 50), fg='#adffff', bg='#3f66b0')
degree_label = tk.Label(canvas, text="\u2103", font=("Helvetica", 30), fg='#adffff', bg='#3f66b0')
temperature_name = tk.Label(canvas, text="Temperature", font=("Arial", 30), fg='white', bg='#3f66b0')


humidity_label = tk.Label(canvas, font=("Helvetica", 50), fg='#adffff', bg='#3f66b0')
humidity_name = tk.Label(canvas, text="Humidity", font=("Arial", 30), fg='#adffff', bg='#3f66b0')

lux_label = tk.Label(canvas, font=("Helvetica", 50), fg='#adffff', bg='#3f66b0')
lux_name = tk.Label(canvas, text="Light", font=("Arial", 30), fg='#adffff', bg='#3f66b0')

audio_label = tk.Label(canvas, font=("Helvetica", 50), fg='#adffff', bg='#3f66b0')
audio_name = tk.Label(canvas, text="Sound", font=("Arial", 30), fg='#adffff', bg='#3f66b0')

motion_image = tk.PhotoImage(file = r"/home/pi/Smart Home dashboard/gui figures/motion_detected.png")
motion_label = tk.Label(canvas, image=motion_image, borderwidth=0)
motion_name = tk.Label(canvas, text="Motion Detected", font=("Arial", 30), fg='red', bg='#d3d2d2')

#################################################################

def time_and_date():
	
    time_now = datetime.now().strftime('%H:%M')
    time.config(text= time_now)
    date_today = datetime.now().strftime("%a, %d. %B %Y")
    date.config(text= date_today)
    root.after(1000, time_and_date)


def sensor_data_update():
	sensorData_3.read_sensor_data()
	#print(sensorData_3.read_sensor_data.temperatureC)
	temperature_final=sensorData_3.read_sensor_data.temperatureC
	temperature_label.config(text= (temperature_final, '\u2103'))
	
	humidity_final=sensorData_3.read_sensor_data.Humidity
	humidity_label.config(text= (humidity_final, '%'))
	
	light_final=sensorData_3.read_sensor_data.light
	lux_label.config(text= (light_final, 'Lux'))
	
	audio_final=sensorData_3.read_sensor_data.audio
	audio_label.config(text= (audio_final, 'dB'))

	if (sensorData_3.read_sensor_data.motion == True):
		print('Motion DETECTED')
		motion_detected()

	root.after(1000, sensor_data_update)

def motion_detected():
	
	motion_label.place(relx=0.3, rely=0.3, relwidth=0.6, relheight=0.6)
	motion_name.place(relx=0.25, rely=0.7, relwidth=0.5, relheight=0.1)
	motion_name.after(5000, motion_name.place_forget)
	motion_label.after(5000, motion_label.place_forget)
	mixer.music.load('Alarm_Clock.mp3')
	mixer.music.play()

def show_temperature():

	calendar_label.place_forget()
	humidity_label.place_forget()
	humidity_name.place_forget()

	lux_label.place_forget()
	lux_label.place_forget()

	audio_label.place_forget()
	audio_name.place_forget()

	temperature_label.place(relx=0.54, rely=0.65, relwidth=0.4, relheight=0.2)
	temperature_name.place(relx=0.56, rely=0.5, relwidth=0.35, relheight=0.15)
	
	temperature_label.after(5000, temperature_label.place_forget)
	temperature_name.after(5000, temperature_name.place_forget)
	calendar_label.after(5000, show_calendar)

	# calendar_label.place(relx=0.5, rely=0.48, relwidth=0.48, relheight=0.45)

def show_humidity():

	calendar_label.place_forget()

	temperature_label.place_forget()
	temperature_name.place_forget()	

	lux_label.place_forget()
	lux_name.place_forget()
	
	audio_label.place_forget()
	audio_name.place_forget()


	humidity_label.place(relx=0.6, rely=0.65, relwidth=0.3, relheight=0.2)
	humidity_name.place(relx=0.56, rely=0.5, relwidth=0.35, relheight=0.15)

	humidity_label.after(5000, humidity_label.place_forget)
	humidity_name.after(5000, humidity_name.place_forget)
	calendar_label.after(5000, show_calendar)

	
def show_lux():

	calendar_label.place_forget()

	temperature_label.place_forget()
	temperature_name.place_forget()	

	humidity_label.place_forget()
	humidity_name.place_forget()

	audio_label.place_forget()
	audio_name.place_forget()


	lux_label.place(relx=0.56, rely=0.65, relwidth=0.35, relheight=0.2)
	lux_name.place(relx=0.57, rely=0.5, relwidth=0.35, relheight=0.15)

	lux_label.after(5000, lux_label.place_forget)
	lux_name.after(5000, lux_name.place_forget)
	calendar_label.after(5000, show_calendar)
	

def show_audio():

	calendar_label.place_forget()

	temperature_label.place_forget()
	temperature_name.place_forget()	

	humidity_label.place_forget()
	humidity_name.place_forget()

	lux_label.place_forget()
	lux_label.place_forget()

	audio_label.place(relx=0.6, rely=0.65, relwidth=0.3, relheight=0.2)
	audio_name.place(relx=0.57, rely=0.5, relwidth=0.35, relheight=0.15)

	audio_label.after(5000, audio_label.place_forget)
	audio_name.after(5000, audio_name.place_forget)
	calendar_label.after(5000, show_calendar)

def show_calendar():

	humidity_label.place_forget()
	humidity_name.place_forget()

	lux_label.place_forget()
	lux_label.place_forget()

	audio_label.place_forget()
	audio_name.place_forget()

	temperature_label.place_forget()
	temperature_name.place_forget()

	calendar_label.place(relx=0.5, rely=0.48, relwidth=0.48, relheight=0.45)


sensor_data_update()
time_and_date()
root.mainloop()
