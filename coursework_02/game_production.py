#1920 x 1080 resolution

#<------- Ghiri Studios ------>
from tkinter import Tk, Canvas
from time import sleep
from random import randint as rand

def up(event): # function for the binding key which make the character jump
	xy = canvas.coords(player)

	if (xy[1] > 10): # checking where the character is located so it can't leave the map when going up
		canvas.move(player, 0, -60)
		sleep(0.01)

	window.update()


window=Tk()
canvas = Canvas(window, width=1280, height=720) # creating the map
canvas.pack()
canvas.config(bg="black")

window.bind("<Key>", up) # binding the key

player = canvas.create_rectangle(500, 500, 520, 520, fill="red") # creating the character

obstacles = [] 
y = rand(10, 500) # creating random obstacles
obstacles.append(canvas.create_rectangle(1240, 0, 1280, y, fill="green")) # an obstacle is built up from 2 pieces, one coming from the ceiling and another from below
obstacles.append(canvas.create_rectangle(1240,y+150 , 1280, 720, fill="green"))

ok = 1 # indexes for the first few steps of spawning the obstacles
start = 1

while True:

	if (start == 7): # when all the obstacles are spawned
		ok = 0

	if (ok == 1):#spawning the obstacles

		for i in range(0, start):

			xy = canvas.coords(player) # gravity system so the player is going down consatntly
			if (xy[3] < 720):
				canvas.move(player, 0, 4)
				sleep(0.03)
				window.update()

			canvas.move(obstacles[i-1], -10, 0) # moving the obstacles to the left
			canvas.move(obstacles[i], -10, 0)
			#sleep(0.03)
			window.update()

		xy_last = canvas.coords(obstacles[start-1]) #checking where is the last spawned obstacle so we can spawn another one
		y = rand(10, 500)
		if (1240 - xy_last[0] > 150):
		 	obstacles.append(canvas.create_rectangle(1240, 0, 1280, y, fill="green"))
		 	obstacles.append(canvas.create_rectangle(1240,y+150 , 1280, 720, fill="green"))
		 	start += 2

	else: # the obstacles are now spawned and now we are just rotating them

		for i in range(0, 8, 2): 

			if (i == 0):
				last_object = 7
			else:
				last_object = i-1

			if (xy[3] < 720):
				canvas.move(player, 0, 2)
				sleep(0.02)
				window.update()

			xy_last = canvas.coords(obstacles[last_object])
			try: 
				xy_obj = canvas.coords(obstacles[i])
				if (xy_obj[0] > 0):
					canvas.move(obstacles[i], -5, 0)
					canvas.move(obstacles[i+1], -5, 0)
					#sleep(0.03)
					window.update()

				else:
					canvas.delete(obstacles[i])
					canvas.delete(obstacles[i+1])
			except:

				if (obstacles[i] not in canvas.find_all() and (1240 - xy_last[0] > 200) ):
					y = rand(10, 500)
					obstacles[i] = canvas.create_rectangle(1240, 0, 1280, y, fill="green")
					obstacles[i+1] = canvas.create_rectangle(1240,y+150 , 1280, 720, fill="green")


window.mainloop()


