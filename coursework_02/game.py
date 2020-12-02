#1920 x 1080 resolution

#<------- Ghiri Studios ------>
from tkinter import Tk, Canvas
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
	obstacles.append( canvas.create_rectangle(0, 0, x, 40, fill="green") )
	obstacles.append( canvas.create_rectangle(x+150,0 , 1280, 40, fill="green") )


def spawning_obstacles():
	global ok
	global start

	if (start == 5):
		ok = 0

	if (ok):

		for i in range(0, start, 2):

			canvas.move(obstacles[i], 0, 5) # moving the obstacles to the left
			canvas.move(obstacles[i+1], 0, 5)

			xy_last1 = canvas.coords(obstacles[i])
			xy_last2 = canvas.coords(obstacles[i+1])
			xy = canvas.coords(player)
			print(i)
			if ( (xy[0] <= xy_last1[2] and xy[1] == xy_last1[3]) or (xy[0] >= xy_last2[0] and xy[1] == xy_last2[3]) ):
				return 0

			xy_last = canvas.coords(obstacles[start-1])
			if ( xy_last[1] > 250):
				start+=2
				x = rand(10, 1130)
				obstacles.append(canvas.create_rectangle(0, 0, x, 40, fill="green"))
				obstacles.append(canvas.create_rectangle(x+150,0 , 1280, 40, fill="green"))
		return 1
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
					canvas.move(obstacles[i], 0, 5)
					canvas.move(obstacles[i+1], 0, 5)
					xy_last1 = canvas.coords(obstacles[i])
					xy_last2 = canvas.coords(obstacles[i+1])
					xy = canvas.coords(player)

					if ( (xy[0] <= xy_last1[2] and xy[1] == xy_last1[3]) or (xy[0] >= xy_last2[0] and xy[1] == xy_last2[3]) ):
						return 0

				else:

					canvas.delete(obstacles[i])
					canvas.delete(obstacles[i+1])

			except:
					if (obstacles[i] not in canvas.find_all() and (xy_last[1] > 250) ):
						x = rand(10, 1130)
						obstacles[i]=canvas.create_rectangle(0, 0, x, 40, fill="green")
						obstacles[i+1]=canvas.create_rectangle(x+150,0 , 1280, 40, fill="green")
		return 1


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

player = canvas.create_rectangle(width/2-10, height/2-10, width/2+10, height/2+10, fill="red") # creating the character

score = 0
score_text = "Score:" + str(score)
txt = canvas.create_text(40, 30, fill="white", font="Times 20 italic bold", text=score_text)

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
# def movement(event): # function for the binding key which make the character jump
# 	xy = canvas.coords(player)

# 	if (event.char == "a"):
# 		canvas.move(player, -10, 0)
# 		sleep(0.02)

# 	if (event.char == "d"):
# 		canvas.move(player, 10, 0)
# 		sleep(0.02)

# 	window.update()


# window=Tk()
# window.title("Ghiri's Game")
# canvas = Canvas(window, width=1280, height=720) # creating the map
# canvas.pack()
# canvas.config(bg="black")

# window.bind("<Key>", movement) # binding the key

# player = canvas.create_rectangle(500, 500, 520, 520, fill="red") # creating the character


# def tubes_movement():
	# for i in range(0, start):
	# 	canvas.move(obstacles[i-1], 0, 10) # moving the obstacles to the left
	# 	canvas.move(obstacles[i], 0, 10)
	# 	sleep(0.05)
	# 	window.update()

	# 	xy_last = canvas.coords(obstacles[start-1]) #checking where is the last spawned obstacle so we can spawn another one
	# 	if ( xy_last[1] > 100):
	# 		start+=2
	# 		x = rand(10, 1130)
	# 		obstacles.append(canvas.create_rectangle(0, 0, x, 40, fill="green"))
	# 		obstacles.append(canvas.create_rectangle(x+150,0 , 1280, 40, fill="green"))

# ok = 1 # indexes for the first few steps of spawning the obstacles
# start = 1
# obstacles = [] 
# x = rand(10, 1130) # creating random obstacles
# obstacles.append(canvas.create_rectangle(0, 0, x, 40, fill="green")) # an obstacle is built up from 2 pieces, one coming from the ceiling and another from below
# obstacles.append(canvas.create_rectangle(x+150,0 , 1280, 40, fill="green"))

# window.after(10, tubes_movement)
# if True:

# 	if (start == 7): # when all the obstacles are spawned
# 		ok = 0
# 		#break

# 	if (ok == 1):#spawning the obstacles


	# else: # the obstacles are now spawned and now we are just rotating them
	# 	for i in range(0, 8, 2): 

	# 		if (i == 0):
	# 			last_object = 7
	# 		else:
	# 			last_object = i-1

	# 		xy_last = canvas.coords(obstacles[last_object])

	# 		try: 
	# 			xy_obj = canvas.coords(obstacles[i])
	# 			if (xy_obj[0] > 0):
	# 				canvas.move(obstacles[i], 0, 5)
	# 				canvas.move(obstacles[i+1], 0, 5)
	# 				#sleep(0.01)
	# 				window.update()

	# 			else:
	# 				canvas.delete(obstacles[i])
	# 				canvas.delete(obstacles[i+1])
	# 		except:
	# 			if (obstacles[i] not in canvas.find_all() and (xy_last[1] > 100) ):
	# 				x = rand(10, 1130)
	# 				obstacles.append(canvas.create_rectangle(0, 0, x, 40, fill="green"))
	# 				obstacles.append(canvas.create_rectangle(x+150,0 , 1280, 40, fill="green"))


#window.mainloop()


