#1920 x 1080 resolution

#<------- Ghiri Studios ------>
from tkinter import Tk, Canvas, PhotoImage, Entry, Button
from time import sleep
from random import randint as rand


def move_left(event):
	global player
	global p
	if ( player in canvas.find_all() ):
		xy = canvas.coords(player)
		if (xy[0] - 45 > 0 and not p):
			canvas.move(player, -15, 0)

def move_right(event):
	global player
	global p
	if ( player in canvas.find_all() ):
		xy = canvas.coords(player)
		if (xy[0] + 45 < 1280 and not p):
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

def check_collision(i):
	coords1 = canvas.coords(obstacles[i])
	coords2 = canvas.coords(obstacles[i+1])
	xy = canvas.coords(player)
	#check for frontal collision
	if ( (xy[0] - 10 <= coords1[2] and xy[1] - 30 == coords1[3]) or ( xy[0] + 8 >= coords2[0] and xy[1] - 30 == coords2[3] )  ):
		return True
	#check for right wing collision
	if ( xy[0] <= coords2[0] and xy[0] + 30 >= coords2[0] and xy[1] - 10 < coords2[3] and xy[1] - 10 >= coords2[1] ):
		return True
	#check for left wing collision
	if ( xy[0] >= coords1[2] and xy[0] - 30 <= coords1[2] and xy[1] - 10 < coords1[3] and xy[1] - 10 >= coords1[1] ):
		return True
	#check back collision for left wing
	if ( xy[1] + 25 >= coords1[1] and xy[1] + 25 <= coords1[3] and xy[0] - 30 <= coords1[2]):
		return True
	#check back collision for right wing
	if ( xy[1] + 25 >= coords2[1] and xy[1] + 25 <= coords2[3] and xy[0] + 30 >= coords2[0]):
		return True

	return False


def spawning_obstacles():
	global ok
	global start
	global altitude

	if (start == 5):
		ok = False

	if (ok):

		for i in range(0, start, 2):

			canvas.move(obstacles[i], 0, 5) # moving the obstacles down
			canvas.move(obstacles[i+1], 0, 5)
			altitude += 1
			height_text = "ALTITUDE: " + str(altitude) + " ft"
			canvas.itemconfig(txt, text=height_text)
			canvas.tag_raise("height")

			if ( check_collision(i) ):
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

					canvas.move(obstacles[i], 0, 5) # moving the obstacles to the left               NU UITA SA SCHIMBI VITEZA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
					canvas.move(obstacles[i+1], 0, 5)
					altitude += 5
					height_text = "ALTITUDE:" + str(altitude) + "ft"
					canvas.itemconfig(txt, text=height_text)
					canvas.tag_raise("height")

					if ( check_collision(i) ):
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

def pause(event):
	global p
	global pause_text
	global bg_pause
	if (event.char == 'p'):

		if (p):
			p = False

			if ( pause_text in canvas.find_all() and bg_pause in canvas.find_all() ):
				canvas.delete(pause_text)
				canvas.delete(bg_pause)

		else:
			bg_pause = canvas.create_rectangle(width/2-250, height/2 - 100, width/2 + 250, height/2 + 100, fill="#80bfff")
			pause_text = canvas.create_text(width/2, height/2, text = "GAME PAUSED", fill="white", font="OCRB 40 bold")
			p = True 

def bosskey(event):
	global b
	global boss_image
	global boss

	if (b):
		b = False
		if ( boss in canvas.find_all() ):
			canvas.delete(boss)

	else:
		boss_image = PhotoImage(file="boss2.PNG")
		boss = canvas.create_image(0, 0, image=boss_image, anchor="nw")
		b = True 

def getname():
	global name_input
	username = name_input.get()
	canvas.delete("all")

	global lost
	lost = PhotoImage(file="lose.png")
	canvas.create_image(0, 0, image=lost, anchor="nw")

	tryagain = Button(window, text="Try Again", font="OCRB 10 bold", command=game, background="grey", highlightthickness=0)
	canvas.create_window(width/2, height/2, window=tryagain)


def running():
	canvas.pack()
	canvas.config(bg="black")
	global GameOver
	global pause

	if (not p and not b):
		GameOver = spawning_obstacles()

	else:
		GameOver = True

	if (GameOver):
		window.after(100, running)

	else:
		canvas.delete("all")
		global name_input
		global lost
		lost = PhotoImage(file="lose.png")
		canvas.create_image(0, 0, image=lost, anchor="nw")

		canvas.create_text(width/2, height/2 - 60, text="You crashed the Spacecraft!\nPlease enter your name below:", font="OCRB 20 bold", fill="white")

		name_input = Entry(window, background="grey", highlightthickness = 0, font="OCRB 20 bold")
		canvas.create_window(width/2, height/2, window=name_input)

		button = Button(window, text="OK", command = getname, highlightthickness = 0, font="OCRB 10 bold", background="grey")
		canvas.create_window(width/2, height/2+50, window=button) 

def game():
	canvas.delete("all")
	global spacecraft
	global background

	spacecraft = PhotoImage(file="character.png")
	background = PhotoImage(file="background1.png")
	bg = canvas.create_image(0, 0, image=background, anchor="nw")

	global player
	player = canvas.create_image(width/2, height/2, image=spacecraft)

	global altitude
	global txt

	altitude = 0
	height_text = "ALTITUDE: " + str(altitude) + " ft"
	txt = canvas.create_text(20, 10, fill="#3F6370", font="OCRB 20 bold", text=height_text, tag="height", anchor="nw")

	canvas.bind("<Left>", move_left)
	canvas.bind("<Right>", move_right)
	canvas.bind("<Key>", pause)
	canvas.bind("<b>",bosskey)
	canvas.focus_set()

	place_first_obstacle()
	global ok
	global start
	global p
	global b

	ok = True
	start = 1
	p = False
	b = False

	running()

def bindings():
	return 1
def rules():
	return 1
def game2():
	return 1
def leaderboard():
	return 1

def quitting():
	canvas.destroy()
	window.quit()

def start_menu():
	canvas.pack()
	global background
	global spacecraft

	background = PhotoImage(file="background1.png")
	canvas.create_image(0, 0, image=background, anchor="nw")
	
	spacecraft = PhotoImage(file="character.png")
	canvas.create_image(width/2, height/2, image=spacecraft)

	#New Game Button
	start = Button(window, text="New Game", font="OCRB 10 bold", command=game)
	canvas.create_window(width/2, height/2-150, window=start)
	
	#Load Game Button
	load = Button(window, text="Load Game", font="OCRB 10 bold", command=game2)
	canvas.create_window(width/2, height/2-100, window=load)
	
	#Leaderboard Button
	lead = Button(window, text="Leaderboard", font="OCRB 10 bold", command=leaderboard)
	canvas.create_window(width/2, height/2-50, window=lead)
	
	#How to Play Button
	howto = Button(window, text="How to Play", font="OCRB 10 bold", command=rules)
	canvas.create_window(width/2, height/2+50, window=howto)

	#Change Control Button
	settings = Button(window, text="Control Settings", font="OCRB 10 bold", command=bindings)
	canvas.create_window(width/2, height/2+100, window=settings)

	#Quit Button
	quit = Button(window, text="Quit Game", font="OCRB 10 bold", command=quitting)
	canvas.create_window(width/2, height/2+150, window=quit)





width =1280
height =720
window = setWindowsDimensions(width, height)
canvas = Canvas(window, width=width, height=height, highlightthickness=0)

start_menu()

window.mainloop()
