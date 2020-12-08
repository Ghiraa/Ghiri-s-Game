#1920 x 1080 resolution

#<------- Ghiri Studios ------>
from tkinter import Tk, Canvas, PhotoImage
from time import sleep
from random import randint as rand


def move_left(event):
	canvas.move(player, -15, 0)

def move_right(event):
	canvas.move(player, 15, 0)

def setWindowsDimensions(w, h):
	window = Tk()
	window.title("Ghiri's Game")
	ws = window.winfo_screenwidth()
	hs = window.winfo_screenheight()
	x = (ws/2) - (w/2)
	y = (hs/2) - (h/2)
	window.geometry('%dx%d+%d+%d' % (w, h, x, y))
	return window

def place_first_obstacle():
	x = rand(10, 1130)
	global obstacles
	obstacles = []
	obstacles.append( canvas.create_rectangle(0, 0, x, 40, fill="white") )
	obstacles.append( canvas.create_rectangle(x+150,0 , 1280, 40, fill="white") )

def collision(i):
	coords1 = canvas.coords(obstacles[i])
	coords2 = canvas.coords(obstacles[i+1])
	xy = canvas.coords(player)
	
	if ( (xy[0] <= coords1[2] and xy[1] - 30 == coords1[3]) or ( xy[0] >= coords2[0] and xy[1] - 30 == coords2[3] )  ):
		return True

	return False

def spawning_obstacles():
	global ok
	global start

	if (start == 5):
		ok = 0

	if (ok):

		for i in range(0, start, 2):

			canvas.move(obstacles[i], 0, 5) # moving the obstacles to the left
			canvas.move(obstacles[i+1], 0, 5)
			
			if ( collision(i) ):
				return False

			xy_last = canvas.coords(obstacles[start-1])

			if ( xy_last[1] > 250):
				start+=2
				x = rand(10, 1130)
				obstacles.append(canvas.create_rectangle(0, 0, x, 40, fill="white"))
				obstacles.append(canvas.create_rectangle(x+150,0 , 1280, 40, fill="white"))

		return True

	else:

		for i in range(0, 6, 2): 

			if (i == 0):
				last_object = 5
			else:
				last_object = i-1

			xy_last = canvas.coords(obstacles[last_object])

			try:

				xy_obj = canvas.coords(obstacles[i])

				if (xy_obj[1] < 720):

					canvas.move(obstacles[i], 0, 5) # moving the obstacles to the left
					canvas.move(obstacles[i+1], 0, 5)

					if ( collision(i) ):
					 	return False

				else:

					canvas.delete(obstacles[i])
					canvas.delete(obstacles[i+1])

			except:
					if (obstacles[i] not in canvas.find_all() and (xy_last[1] > 250) ):
						x = rand(10, 1130)
						obstacles[i]=canvas.create_rectangle(0, 0, x, 40, fill="white")
						obstacles[i+1]=canvas.create_rectangle(x+150,0 , 1280, 40, fill="white")

		return True


def running():
	canvas.pack()
	canvas.config(bg="black")

	global GameOver
	GameOver = spawning_obstacles()
	if (GameOver):
		window.after(100, running)


width =1280
height =720
window = setWindowsDimensions(width, height)
canvas = Canvas(window, width=width, height=height)

spacecraft = PhotoImage(file="character.png")
background = PhotoImage(file="pule.png")
bg = canvas.create_image(0, 0, image=background)

player = canvas.create_image(width/2, height/2, image=spacecraft)

score = 0
score_text = "Score:" + str(score)
txt = canvas.create_text(40, 30, fill="black", font="Times 20 italic bold", text=score_text)

canvas.bind("<Left>", move_left)
canvas.bind("<Right>", move_right)
canvas.focus_set()

place_first_obstacle()

global ok
global start
ok = 1
start = 1

running()

window.mainloop()
