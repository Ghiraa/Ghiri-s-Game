#1920 x 1080 resolution

#<------- Ghiri Studios ------>
from tkinter import Tk, Canvas
from time import sleep


def up(event):
	x = 0
	y = -10
	canvas.move(player, x, y)


window=Tk()

canvas = Canvas(window, width=1920, height=1080)
canvas.pack()
canvas.config(bg="black")

player = canvas.create_rectangle(500, 500, 550, 550, fill="red")
window.bind("<Key>", up)

while True:
	xy = canvas.coords(player)

	if (xy[3] > 1080):
		break

	canvas.move(player, 0, 3)
	sleep(0.02)
	window.update()

window.mainloop()


