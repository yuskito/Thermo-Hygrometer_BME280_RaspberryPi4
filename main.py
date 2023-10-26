import tkinter as tk
from os import path
import schedule

import argparse
parser = argparse.ArgumentParser(description='Offline debug mode without BME280 hardware and size factor')
parser.add_argument('--OD', action='store_true', help='Enable offline debug mode')
parser.add_argument('--size', type = float, default = 1.0, help='window size factor')
args = parser.parse_args()

if args.OD: # When --OD is given as parameter, Offline Debug mode
    pass
else:
    from BME280 import bme280_sample_mod

if args.size: # When size is defined.
    multiply = args.size
else: multiply =1


class GUI(tk.Frame, object):
    def __init__(self, master=None):
        super(GUI, self).__init__(master)
        self.master = master



        window_width = int(640 * multiply)
        window_height = int (480 * multiply)
        master.geometry(f'{window_width}x{window_height}+0+0')
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

        self.canvas = tk.Canvas(master, width=window_width, height=window_height)
        self.canvas.pack()

        def make_rounded_rectangle(xcord1, ycord1, xcord2, ycord2, radius = 25*multiply, **kwargs):
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

        self.rounded_rectangle = make_rounded_rectangle(20*multiply, 20*multiply, 300*multiply, 170*multiply, radius=25*multiply,
                                                        fill="orange")
        self.rounded_rectangle = make_rounded_rectangle(320*multiply, 20*multiply, 620*multiply, 170*multiply, radius=25*multiply,
                                                        fill="salmon")
        self.rounded_rectangle = make_rounded_rectangle(20*multiply, 190*multiply, 300*multiply, 360*multiply, radius=25*multiply,
                                                        fill="cyan2")
        self.rounded_rectangle = make_rounded_rectangle(320*multiply, 190*multiply, 620*multiply, 360*multiply, radius=25*multiply,
                                                        fill="khaki1")

        self.canvas.create_text(170*multiply, 90*multiply, text=" %-6.1f°C" % (temperature),
                                font = font, tag="tempC")
        self.canvas.create_text(485*multiply, 90*multiply, text=" %-6.1f °F" % (temperatureF),
                                font = font, tag="tempF")
        self.canvas.create_text(150*multiply, 275*multiply, text=" %6.1f %%" % (humidity),
                                font = font, tag="hum")
        self.canvas.create_text(460*multiply, 275*multiply, text=" %7.1f hPa" % (pressure / 100),
                                font = font, tag="press")

        ImagePath_hum = path.join(path.dirname(__file__), "Hum_icon.png")
        ImagePath_Ctemp = path.join(path.dirname(__file__),
                                    "./Temp_Icon.png")
        ImagePath_Ftemp = path.join(path.dirname(__file__), "Ftemp.png")
        ImagePath_Press = path.join(path.dirname(__file__), "Press_Icon.png")

        self.img_hum = tk.PhotoImage(file=ImagePath_hum, width=50, height=50)
        self.canvas.create_image(50*multiply, 275*multiply, image=self.img_hum)

        self.img_Ctemp = tk.PhotoImage(file=ImagePath_Ctemp, width=50,
                                       height=50)
        self.canvas.create_image(50*multiply, 90*multiply, image=self.img_Ctemp)

        self.img_Ftemp = tk.PhotoImage(file=ImagePath_Ftemp, width=50,
                                       height=50)
        self.canvas.create_image(350*multiply, 90*multiply, image=self.img_Ftemp)

        self.img_Press = tk.PhotoImage(file=ImagePath_Press, width=50,
                                       height=50)
        self.canvas.create_image(350*multiply, 225*multiply, image=self.img_Press)

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

        fontsize = int (40*multiply)
        font = ('Helvetica', fontsize, 'bold')

        self.canvas.create_text(170*multiply, 90*multiply, text=" %-6.1f°C" % (temperature),
                                font = font, tag="tempC")
        self.canvas.create_text(485*multiply, 90*multiply, text=" %-6.1f °F" % (temperatureF),
                                font = font, tag="tempF")
        self.canvas.create_text(150*multiply, 275*multiply, text=" %6.1f %%" % (humidity),
                                font = font, tag="hum")
        self.canvas.create_text(460*multiply, 275*multiply, text=" %7.1f hPa" % (pressure / 100),
                                font= font, tag="press")

        self.canvas.pack()


if __name__ == '__main__':
    gui = tk.Tk()
    app = GUI(master=gui)
    app.mainloop()
