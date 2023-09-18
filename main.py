import tkinter as tk
from os import path
import schedule

import argparse
parser = argparse.ArgumentParser(description='Offline debug mode without BME280 hardware')
parser.add_argument('--OD', action='store_true', help='Enable offline debug mode')
args = parser.parse_args()

if args.OD: # When --OD is given as parameter, Offline Debug mode
    pass
else:
    from BME280 import bme280_sample_mod

class GUI(tk.Frame, object):
    def __init__(self, master=None):
        super(GUI, self).__init__(master)
        self.master = master
        master.geometry("640x480+0+0")
        master.title("Thermo-hygrometer")

        self.test = tk.Frame(self.master)
        self.test.pack()

        if args.OD: # When --OD is given as parameter, Offline Debug mode
            temperature = 25.5
            temperatureF = 1.8 * temperature + 32.0
            pressure = 108888
            humidity = 55.5

        else:

            bme280_sample_mod.setup()
            bme280_sample_mod.get_calib_param()
            sensor_result = bme280_sample_mod.readData()

            if sensor_result:
                temperature = sensor_result[0]
                temperatureF = 1.8 * temperature + 32.0
                pressure = sensor_result[1]
                humidity = sensor_result[2]

        self.canvas = tk.Canvas(master, width=640, height=480)
        self.canvas.pack()

        def make_rounded_rectangle(xcord1, ycord1, xcord2, ycord2, radius = 25, **kwargs):
            points = [xcord1 + radius, ycord1,
                      xcord1 + radius, ycord1,
                      xcord2 - radius, ycord1,
                      xcord2 - radius, ycord1,
                      xcord2, ycord1,
                      xcord2, ycord1 + radius,
                      xcord2, ycord1 + radius,
                      xcord2, ycord2 - radius,
                      xcord2, ycord2 - radius,
                      xcord2, ycord2,
                      xcord2 - radius, ycord2,
                      xcord2 - radius, ycord2,
                      xcord1 + radius, ycord2,
                      xcord1 + radius, ycord2,
                      xcord1, ycord2,
                      xcord1, ycord2 - radius,
                      xcord1, ycord2 - radius,
                      xcord1, ycord1 + radius,
                      xcord1, ycord1 + radius,
                      xcord1, ycord1]

            return self.canvas.create_polygon(points, smooth=True,
                                              **kwargs), self.canvas.create_polygon(
                points, smooth=True, **kwargs)

        self.rounded_rectangle = make_rounded_rectangle(20, 20, 300, 170, radius=20,
                                                        fill="orange")
        self.rounded_rectangle = make_rounded_rectangle(320, 20, 620, 170, radius=20,
                                                        fill="salmon")
        self.rounded_rectangle = make_rounded_rectangle(20, 190, 300, 360, radius=20,
                                                        fill="cyan2")
        self.rounded_rectangle = make_rounded_rectangle(320, 190, 620, 360, radius=20,
                                                        fill="khaki1")

        self.canvas.create_text(170, 90, text=" %-6.1f°C" % (temperature),
                                font=('Helvetica 40 bold'), tag="tempC")
        self.canvas.create_text(485, 90, text=" %-6.1f °F" % (temperatureF),
                                font=('Helvetica 40 bold'), tag="tempF")
        self.canvas.create_text(150, 275, text=" %6.1f %%" % (humidity),
                                font=('Helvetica 40 bold'), tag="hum")
        self.canvas.create_text(460, 275, text=" %7.1f hPa" % (pressure / 100),
                                font=('Helvetica 40 bold'), tag="press")

        ImagePath_hum = path.join(path.dirname(__file__), "Hum_icon.png")
        ImagePath_Ctemp = path.join(path.dirname(__file__),
                                    "../Thermo-Hygrometer-BME280-RaspberryPi4/Temp_Icon.png")
        ImagePath_Ftemp = path.join(path.dirname(__file__), "Ftemp.png")
        ImagePath_Press = path.join(path.dirname(__file__), "Press_Icon.png")

        self.img_hum = tk.PhotoImage(file=ImagePath_hum, width=50, height=50)
        self.canvas.create_image(50, 275, image=self.img_hum)

        self.img_Ctemp = tk.PhotoImage(file=ImagePath_Ctemp, width=50,
                                       height=50)
        self.canvas.create_image(50, 90, image=self.img_Ctemp)

        self.img_Ftemp = tk.PhotoImage(file=ImagePath_Ftemp, width=50,
                                       height=50)
        self.canvas.create_image(350, 90, image=self.img_Ftemp)

        self.img_Press = tk.PhotoImage(file=ImagePath_Press, width=50,
                                       height=50)
        self.canvas.create_image(350, 225, image=self.img_Press)

        self.canvas.pack()

        schedule.every(5).seconds.do(self.update)
        self.sc()

    def sc(self):
        schedule.run_pending()
        self.after(60, self.sc)

    def update(self):

        if args.OD: # When --OD is given as parameter, Offline Debug mode
            temperature = 25.5
            temperatureF = 1.8 * temperature + 32.0
            pressure = 108888
            humidity = 55.5

        else:
            sensor_result = bme280_sample_mod.readData()

            if sensor_result:
                temperature = sensor_result[0]
                temperatureF = 1.8 * temperature + 32.0
                pressure = sensor_result[1]
                humidity = sensor_result[2]

        self.canvas.delete("tempC")
        self.canvas.delete("tempF")
        self.canvas.delete("hum")
        self.canvas.delete("press")

        self.canvas.create_text(170, 90, text=" %-6.1f°C" % (temperature),
                                font=('Helvetica 40 bold'), tag="tempC")
        self.canvas.create_text(485, 90, text=" %-6.1f °F" % (temperatureF),
                                font=('Helvetica 40 bold'), tag="tempF")
        self.canvas.create_text(150, 275, text=" %6.1f %%" % (humidity),
                                font=('Helvetica 40 bold'), tag="hum")
        self.canvas.create_text(460, 275, text=" %7.1f hPa" % (pressure / 100),
                                font='Helvetica 40 bold', tag="press")

        self.canvas.pack()


if __name__ == '__main__':
    gui = tk.Tk()
    app = GUI(master=gui)
    app.mainloop()
