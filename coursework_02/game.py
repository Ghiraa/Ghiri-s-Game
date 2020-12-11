#1920 x 1080 resolution

#<------- Ghiri Studios ------>
from tkinter import Tk, Canvas, PhotoImage, Entry, Button, StringVar
from time import sleep
from random import randint as rand
import os

# The function which moves the player to the left
def move_left(event):
	global player
	global b # represents the boss state, if it is true, it means the boss pause is on
	global p # represents the pause state, if it is true, it means the pause is on

	if ( player in canvas.find_all() ): #if the player exist move it to the left
		xy = canvas.coords(player)
		if (xy[0] - 45 > 0 and not p and not b):#if it will not go outside the map if moved and the game is not paused or the boss pause
			canvas.move(player, -20, 0)

# The function which moves the player to the right
def move_right(event):
	global player
	global b
	global p

	if ( player in canvas.find_all() ):
		xy = canvas.coords(player)
		if (xy[0] + 45 < 1280 and not p and not b): # same as move_left function but we have to test if it will not go outside the map if moved right
			canvas.move(player, 20, 0)

def setWindowsDimensions(w, h): # setting the tkinter dimensions and positions
	window = Tk()
	window.title("Ghiri's Game")
	ws = window.winfo_screenwidth()# getting screen width
	hs = window.winfo_screenheight()# getting screen height
	x = (ws/2) - (w/2)
	y = (hs/2) - (h/2)
	window.geometry('%dx%d+%d+%d' % (w, h, x, y))
	return window

def place_first_obstacle(): # placing the first obstacles in the canvas
	global obstacles

	obstacles = []
	x = rand(10, 1130)  # generating a random spot for the hole between the obstacles

	obstacles.append( canvas.create_rectangle(0, 0, x, 40, fill="white") ) # this is the left half of an obstacle
	obstacles.append( canvas.create_rectangle(x+150,0 , 1280, 40, fill="white") )# this is the right half of an obstacle

def check_collision(i): # function which text if there is any collision between the player and the obstacles
	coords1 = canvas.coords(obstacles[i]) # getting the coordinates of the first half
	coords2 = canvas.coords(obstacles[i+1]) # getting the coordinates of the second half
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

def negation(): #this function will turn the cheat off it is on
	global cheat
	cheat = False

def spawning_obstacles(): # this function spawns the first obstacles and then just loop them through canvas
	global ok             # if an obstacle is at the end of the canvas, function deletes it and spawns at top
	global start
	global altitude
	global cheat
	global no_obstacles

	if (start == 5): # this means we spawned all five obstacles so we can start looping them
		ok = False

	if (ok): # first case when not all obstacles were spawned

		for i in range(0, start, 2): #going through those which are already spawned

			canvas.move(obstacles[i], 0, 10) # moving the obstacles down
			canvas.move(obstacles[i+1], 0, 10)

			altitude += 1 # increasing the altitude because we are moving
			height_text = "ALTITUDE: " + str(altitude) + " ft"
			canvas.itemconfig(txt, text=height_text) # reconfiguring the text displayed at top left
			canvas.tag_raise("height")

			if ( check_collision(i) and not cheat): # checking for collision with the obstacles and if the cheat is off so we have collissions
				return False

			if (cheat): # if cheat is on we have to count the number of obstacles we go through so we can turn it off
				if ( no_obstacles > 0 ): # if we still have obstacles we need to count
					cheat_obstacles(i) # check if we passed the current obstacle

					if ( no_obstacles == 0 ): # when we finished the number of obstacles we have to turn the cheat off
							window.after(2000,negation)

			xy_last = canvas.coords(obstacles[start-1]) # getting the coordinates of the last spawned obstacle

			if ( xy_last[1] > 300): # if there is enough space between the last obstacle and top of the window we can spawn the next one
				start+=2 # count the new obstacle too

				x = rand(10, 1130) # getting a random hole for the obstacle
				obstacles.append(canvas.create_rectangle(0, 0, x, 40, fill="white"))
				obstacles.append(canvas.create_rectangle(x+150,0 , 1280, 40, fill="white"))

		return True

	else: # all the obstacles are spawned

		for i in range(0, 6, 2): 

			if (i == 0):
				last_object = 5 # for the first obstacle the last obstacle is the third one

			else:
				last_object = i-1 # else is the one behind

			xy_last = canvas.coords(obstacles[last_object]) # getting the coordiantes of the last obstacle

			try: #if the current obstacle exist

				xy_obj = canvas.coords(obstacles[i]) # getting the coordinates of it

				if (xy_obj[1] < 720): # if we can move it down

					canvas.move(obstacles[i], 0, 10) # moving the obstacle down
					canvas.move(obstacles[i+1], 0, 10)

					altitude += 1 # increasing the altitude
					height_text = "ALTITUDE:" + str(altitude) + "ft"
					canvas.itemconfig(txt, text=height_text) # recondifugring the text displayed at top left
					canvas.tag_raise("height")

					if ( check_collision(i) and not cheat): # checking for collision between the player and teh current obstacle
					 	return False

					if (cheat): # if the cheat is on we have to count the number of obstacles we go through so we can turn it off
						if ( no_obstacles > 0 ): # if we still have obstacles we need to count
							cheat_obstacles(i) # check if we passed the current obstacle 

							if ( no_obstacles == 0 ): # when we finished the number of obstacles we have to turn the cheat off
								window.after(2000, negation)

				else: # it means the obstacle is at the bottom of the canvas so we have to delete it

					canvas.delete(obstacles[i])
					canvas.delete(obstacles[i+1])

			except: # it means the current obstacle is deleted from the canvas

					if (obstacles[i] not in canvas.find_all() and (xy_last[1] > 300) ): #if there is enough space between the last obstacle and the top of the canvas we have to spawn it

						x = rand(10, 1130) # generating a random hole for the obstacle
						obstacles[i]=canvas.create_rectangle(0, 0, x, 40, fill="white") # spawn the obstacles
						obstacles[i+1]=canvas.create_rectangle(x+150,0 , 1280, 40, fill="white")

		return True

def cheat_obstacles(i): # this function counts the number of obstacles you go through when you have the cheat on
	global no_obstacles

	coords1 = canvas.coords(obstacles[i]) #coordinates of the first half of the obstacle i
	coords2 = canvas.coords(obstacles[i+1]) # coordinates of the second half of the obstacle i
	xy = canvas.coords(player)# coordinates of the spacecraft

	#check to see if you pass obstacle i
	if ( xy[1] - 30 >= coords1[3] and xy[1] - 30 <= coords2[3]):
		no_obstacles -= 1 # we passed obstacle i so we count


def cheatcode(event): # this function checks if the cheat is off and turns it on
	global cheat
	global no_obstacles

	if ( not cheat ):
		cheat = True
		no_obstacles = 3 # initialising the numbers of obstacles we can go through

def deletesave():
	global save_img
	global go_back
	global saved
	global save_button
	canvas.delete("savebuttons")
	canvas.delete(save_img)
	canvas.delete(go_back)

	saved = canvas.create_window(width/2, height/2 + 50, window = save_button)
	canvas.bind("<p>", pause)
	canvas.bind("<b>",bosskey)

def deletesavepage():
	canvas.delete(go_back2)
	canvas.delete(name_save_submit)
	canvas.delete(name_save_window)
	canvas.delete(warning)

	canvas.itemconfig(saveBTN1, state="normal")
	canvas.itemconfig(saveBTN2, state="normal")
	canvas.itemconfig(saveBTN3, state="normal")
	canvas.itemconfig(saveBTN4, state="normal")
	canvas.itemconfig(saveBTN5, state="normal")
	canvas.itemconfig(go_back,  state="normal")

def renamefile(a):
	name = name_save.get()
	global p
	global saved

	for file in os.listdir():
		if (file == a):

			save = open(file, "w")
			save.write( str(altitude) )
			
			os.rename(file, name)

	canvas.delete(name_save_window)
	canvas.delete(go_back2)
	canvas.delete(name_save_submit)
	canvas.delete(warning)
	canvas.delete("savebuttons")
	canvas.delete(save_img)
	canvas.delete(go_back)
	saved = canvas.create_window(width/2, height/2 + 50, window = save_button)
	canvas.bind("<b>", bosskey)
	canvas.bind("<p>", pause)
	canvas.focus_set()



def limit2(*args):
	text = savename.get()
	savename.set(savename.get().upper())
	if ( not text.isalpha() ):
		savename.set(text[:(len(text)-1)])
	if ( len(text) > 5):
		savename.set(text[:5])

def saving(no):
	canvas.itemconfig(go_back, state="hidden")
	global go_back2
	global name_save_submit
	global name_save_window
	global warning
	global name_save
	global savename

	warning =canvas.create_text(width/2, 40, text="")

	canvas.itemconfig(saveBTN1, state="hidden")
	canvas.itemconfig(saveBTN2, state="hidden")
	canvas.itemconfig(saveBTN3, state="hidden")
	canvas.itemconfig(saveBTN4, state="hidden")
	canvas.itemconfig(saveBTN5, state="hidden")

	savename = StringVar()
	savename.trace("w", limit2)

	name_save = Entry(window, background="grey", highlightthickness = 0, font="OCRB 20 bold", textvariable=savename)
	name_save_window = canvas.create_window(width/2, height/2, window=name_save)
	
	go_back_btn2 = Button(window, text="Go back", highlightthickness = 0, font="OCRB 10 bold", background="grey", command = deletesavepage)# button for submiting the nickname
	go_back2 = canvas.create_window(50, 700, window = go_back_btn2)
	
	if ( no == 1 ):

		if ( save1["text"][:4] != "save" ):
			canvas.itemconfig(warning, text="Be careful! Here already exists a save. Proceeding can result in losing the initial save!")

		name_save_btn = Button(window, text="Complete", command = (lambda a=save1["text"]: renamefile(a)), highlightthickness = 0, font="OCRB 10 bold", background="grey")# button for submiting the nickname
		name_save_submit = canvas.create_window(width/2, height/2+50, window=name_save_btn) 

	if ( no == 2 ):

		if ( save2["text"][:4] != "save" ):
			canvas.itemconfig(warning, text="Be careful! Here already exists a save. Proceeding can result in losing the initial save!")

		name_save_btn = Button(window, text="Complete", command = (lambda a=save2["text"]: renamefile(a)), highlightthickness = 0, font="OCRB 10 bold", background="grey")# button for submiting the nickname
		name_save_submit = canvas.create_window(width/2, height/2+50, window=name_save_btn)

	if ( no == 3 ):

		if ( save3["text"][:4] != "save" ):
			canvas.itemconfig(warning, text="Be careful! Here already exists a save. Proceeding can result in losing the initial save!")

		name_save_btn = Button(window, text="Complete", command = (lambda a=save3["text"]: renamefile(a)), highlightthickness = 0, font="OCRB 10 bold", background="grey")# button for submiting the nickname
		name_save_submit = canvas.create_window(width/2, height/2+50, window=name_save_btn)

	if ( no == 4 ):

		if ( save4["text"][:4] != "save" ):
			canvas.itemconfig(warning, text="Be careful! Here already exists a save. Proceeding can result in losing the initial save!")

		name_save_btn = Button(window, text="Complete", command = (lambda a=save4["text"]: renamefile(a)), highlightthickness = 0, font="OCRB 10 bold", background="grey")# button for submiting the nickname
		name_save_submit = canvas.create_window(width/2, height/2+50, window=name_save_btn)

	if ( no == 5 ):

		if ( save5["text"][:4] != "save" ):
			canvas.itemconfig(warning, text="Be careful! Here already exists a save. Proceeding can result in losing the initial save!")

		name_save_btn = Button(window, text="Complete", command = (lambda a=save5["text"]: renamefile(a)), highlightthickness = 0, font="OCRB 10 bold", background="grey")# button for submiting the nickname
		name_save_submit = canvas.create_window(width/2, height/2+50, window=name_save_btn)

def save():
	global saved
	global save_bg
	global save_img
	global go_back_btn
	global go_back
	global saveF
	global no_files
	global saveBTN1
	global saveBTN2
	global saveBTN3
	global saveBTN4
	global saveBTN5
	global save1
	global save2
	global save3
	global save4
	global save5

	canvas.delete(saved)
	canvas.unbind("<b>")
	canvas.unbind("<p>")

	save_bg = PhotoImage(file="background1.png") # game's background
	save_img = canvas.create_image(0, 0, image=background, anchor="nw")

	go_back_btn = Button(window, text="Go back", highlightthickness = 0, font="OCRB 10 bold", background="grey", command = deletesave)# button for submiting the nickname
	go_back = canvas.create_window(50, 700, window = go_back_btn) 

	x = -100
	no_files = 0
	for files in os.listdir():

		if ( len(files) == 3 ):
			no_files += 1
			x += 50
			if (no_files == 1):
				save1 = Button(window, text=files, highlightthickness = 0, font="OCRB 10 bold", background="grey", command = (lambda no = no_files: saving(no) ) )# button for submiting the nickname
				saveBTN1 = canvas.create_window(width/2 , height/2 + x, window = save1, tag="savebuttons")
			
			if (no_files == 2):
				save2 = Button(window, text=files, highlightthickness = 0, font="OCRB 10 bold", background="grey", command = (lambda no = no_files: saving(no) ))# button for submiting the nickname
				saveBTN2 = canvas.create_window(width/2 , height/2 + x, window = save2, tag="savebuttons")
			
			if (no_files == 3):
				save3 = Button(window, text=files, highlightthickness = 0, font="OCRB 10 bold", background="grey", command = (lambda no = no_files: saving(no) ))# button for submiting the nickname
				saveBTN3 = canvas.create_window(width/2 , height/2 + x, window = save3, tag="savebuttons")
			
			if (no_files == 4):
				save4 = Button(window, text=files, highlightthickness = 0, font="OCRB 10 bold", background="grey", command = (lambda no = no_files: saving(no) ))# button for submiting the nickname
				saveBTN4 = canvas.create_window(width/2 , height/2 + x, window = save4, tag="savebuttons")
			
			if (no_files == 5):
				save5 = Button(window, text=files, highlightthickness = 0, font="OCRB 10 bold", background="grey", command = (lambda no = no_files: saving(no) ))# button for submiting the nickname
				saveBTN5 = canvas.create_window(width/2 , height/2 + x, window = save5, tag="savebuttons")
			 


def pause(event): # this function checks if the pause is on and turn it off and vice-versa
	global p
	global pause_text
	global bg_pause
	global saved
	global save_button
	if (p):
		p = False

		if ( pause_text in canvas.find_all() and bg_pause in canvas.find_all() and saved in canvas.find_all() ): # we turn off the pause so we delete the pause text
			
			canvas.delete(pause_text)
			canvas.delete(bg_pause)
			canvas.delete(saved)
		
	else: # we turn on the pause so we spawn the pause text and the save button
		p = True
		
		bg_pause = canvas.create_rectangle(width/2 - 250, height/2 - 100, width/2 + 250, height/2 + 100, fill="#80bfff")
		pause_text = canvas.create_text(width/2, height/2, text = "GAME PAUSED", fill="white", font="OCRB 40 bold")
		
		save_button = Button(window, text="Save the game", highlightthickness = 0, font="OCRB 10 bold", background="grey", command = save)# button for submiting the nickname
		saved = canvas.create_window(width/2, height/2 + 50, window = save_button) 



def bosskey(event): # this function checks if the "boss key" is activated and spawn the image
	global b
	global boss_image
	global boss

	if (b): # checks if the boss key is active so turn it off
		b = False
		if ( boss in canvas.find_all() ): #deleting the "boss" image
			canvas.delete(boss)

	else:# turn on the boss key and spawn the "boss" image
		if (not p):
			boss_image = PhotoImage(file="boss2.PNG") 
			boss = canvas.create_image(0, 0, image=boss_image, anchor="nw")
			b = True 


def leaderboard_create(user):
	list = []
	with open("LEADERBOARD","r") as file:
		list= file.readlines()

	current_place = str(altitude) + " " + user
	with open("LEADERBOARD","w") as file:
		file.write("")


	for i in range(0,5):
		if ( len(list[i]) >= 3):
			
			nr1 = str(current_place[:(len(current_place)-6)])
			nr2 = str(list[i][:len(list[i])-6])

			if ( int(nr1) >= int(nr2) ):
				if (i<4):
					with open("LEADERBOARD","a") as file:
						file.write(current_place.rstrip())
						file.write("\n")
				else:
					with open("LEADERBOARD","a") as file:
						file.write(current_place.rstrip())

				current_place = list[i]
			else:
				if (i<4):
					with open("LEADERBOARD","a") as file:
						file.write(list[i].rstrip())
						file.write("\n")
				else:
					with open("LEADERBOARD","a") as file:
						file.write(list[i].rstrip())

		else:
			if (i<4):
				with open("LEADERBOARD","a") as file:
					file.write(current_place.rstrip())
					file.write("\n")
			else:
				with open("LEADERBOARD","a") as file:
					file.write(current_place.rstrip())
			current_place="0"


def getname(): #this functions gets the name the player is asked for
	global name_input
	if ( len(name_input.get()) <5 ):
		username = "XXXXX"
	else:
		username = name_input.get()

	leaderboard_create(username)
	canvas.delete("all") #delete all we have in canvas so we can create a new background

	global lost
	lost = PhotoImage(file="lose.png") # creating the "game lost" background
	canvas.create_image(0, 0, image=lost, anchor="nw")
	global altitude
	altitude = 0
	#Try Again button
	tryagain = Button(window, text="Try Again", font="OCRB 30 bold", command=game, background="grey", highlightthickness=0)
	canvas.create_window(width/2, height/2, window=tryagain)

	#Main Menu
	main = Button(window, text="Main Menu", font="OCRB 30 bold", command=start_menu, background="grey", highlightthickness=0)
	canvas.create_window(width/2, height/2+100, window=main)

	#Quit Button
	quit = Button(window, text="Quit Game", font="OCRB 30 bold", command=quitting, background="grey", highlightthickness=0)
	canvas.create_window(width/2, height/2+200, window=quit)

def limit(*args):
	text = nickname.get()
	nickname.set(nickname.get().upper())
	if ( not text.isalpha() ):
		nickname.set(text[:(len(text)-1)])

	if ( len(text) > 5 ):
		nickname.set(text[:5])

def running(): # this functions is recursive and runs the game continuosly
	canvas.pack()
	canvas.config(bg="black")

	global GameOver
	global pause

	if (not p and not b): # if the pause is not on or the "boss key" is not activated we can move the obstacles
		GameOver = spawning_obstacles()

	else: 
		GameOver = True

	if (GameOver): # even if the pause is on or we didn't detect any form of collision we loop again
		# print(p)
		window.after(100, running)

	else: # we detected a form of collision so we delte all and ask the player for their nickname
		canvas.delete("all")

		global name_input
		global lost
		global nickname
		lost = PhotoImage(file="lose.png") # "game lost" background
		canvas.create_image(0, 0, image=lost, anchor="nw")

		canvas.create_text(width/2, height/2 - 60, text="You crashed the Spacecraft!\nPlease enter your name below:", font="OCRB 20 bold", fill="grey") # asking the player for the nickname

		nickname = StringVar()
		nickname.trace("w", limit)

		name_input = Entry(window, background="grey", highlightthickness = 0, font="OCRB 20 bold", textvariable=nickname) # creating the text box to enter a nickname
		canvas.create_window(width/2, height/2, window=name_input)
		
		button = Button(window, text="OK", command = getname, highlightthickness = 0, font="OCRB 10 bold", background="grey")# button for submiting the nickname
		canvas.create_window(width/2, height/2+50, window=button) 


def game(): # this is the main function where we initialise all the values, create game's background, etc
	canvas.delete("all")
	global spacecraft
	global background

	spacecraft = PhotoImage(file="character.png") # spacecraft
	background = PhotoImage(file="background1.png") # game's background
	bg = canvas.create_image(0, 0, image=background, anchor="nw")

	global player
	player = canvas.create_image(width/2, height/2, image=spacecraft) # creating the player

	global altitude
	global txt

	#altitude = 0 # initialising the altitude to 0 and spawning the text
	height_text = "ALTITUDE: " + str(altitude) + " ft"
	txt = canvas.create_text(20, 10, fill="#3F6370", font="OCRB 20 bold", text=height_text, tag="height", anchor="nw")

	canvas.bind("<Left>", move_left) 
	canvas.bind("<Right>", move_right)

	canvas.bind("<p>", pause) # binding "p" for the pause function
	canvas.bind("<b>",bosskey)# binding "b" for the "boss key" function
	canvas.bind("<Control-Shift-H>",cheatcode)# binding the combinations of keys for the cheat code
	canvas.focus_set()

	place_first_obstacle() # placing the first obstacle on the canvas
	global ok 
	global start
	global p
	global b
	global cheat

	ok = True # we didn't spawn all the objects so we initialise ok with True
	start = 1 # start is one bc we have 2 halves in the lsit of objects
	p = False # at first pause is turned off
	b = False # at first "boss key" is turned off
	cheat = False # at first "cheat code" is not activated

	running() # starting the game

def bindings():
	return 1
def rules():
	return 1

def load_buttons(no):
	canvas.itemconfig(saveBTN1, state="hidden")
	canvas.itemconfig(saveBTN2, state="hidden")
	canvas.itemconfig(saveBTN3, state="hidden")
	canvas.itemconfig(saveBTN4, state="hidden")
	canvas.itemconfig(saveBTN5, state="hidden")
	
	go_back_btn2 = Button(window, text="Go back", highlightthickness = 0, font="OCRB 10 bold", background="grey", command = deletesavepage)# button for submiting the nickname
	go_back2 = canvas.create_window(50, 700, window = go_back_btn2)
	
	global altitude

	if ( no == 1 ):
		with open(save1["text"]) as file:
			altitude = int(file.read())
		game() 

	if ( no == 2 ):
		with open(save2["text"]) as file:
			altitude = int(file.read())
		game()
		
	if ( no == 3 ):
		with open(save3["text"]) as file:
			altitude = int(file.read())
		game()
		
	if ( no == 4 ):
		with open(save4["text"]) as file:
			altitude = int(file.read())
		game()
		
	if ( no == 5 ):
		with open(save5["text"]) as file:
			altitude = int(file.read())
		game()
		


def game2():
	global save_bg
	global save_img
	global go_back_btn
	global go_back
	global saveBTN1
	global saveBTN2
	global saveBTN3
	global saveBTN4
	global saveBTN5
	global save1
	global save2
	global save3
	global save4
	global save5

	canvas.delete("all")
	save_bg = PhotoImage(file="background1.png") # game's background
	save_img = canvas.create_image(0, 0, image=background, anchor="nw")

	go_back_btn = Button(window, text="Go back", highlightthickness = 0, font="OCRB 10 bold", background="grey", command = start_menu)# button for submiting the nickname
	go_back = canvas.create_window(50, 700, window = go_back_btn) 


	x = -100
	no_files = 0
	for files in os.listdir():

		if ( len(files) == 3 ):
			no_files += 1
			x += 50
			if (no_files == 1):
				save1 = Button(window, text=files, highlightthickness = 0, font="OCRB 10 bold", background="grey", command = (lambda no = no_files: load_buttons(no) ) )# button for submiting the nickname
				saveBTN1 = canvas.create_window(width/2 , height/2 + x, window = save1, tag="savebuttons")
			
			if (no_files == 2):
				save2 = Button(window, text=files, highlightthickness = 0, font="OCRB 10 bold", background="grey", command = (lambda no = no_files: load_buttons(no) ))# button for submiting the nickname
				saveBTN2 = canvas.create_window(width/2 , height/2 + x, window = save2, tag="savebuttons")
			
			if (no_files == 3):
				save3 = Button(window, text=files, highlightthickness = 0, font="OCRB 10 bold", background="grey", command = (lambda no = no_files: load_buttons(no) ))# button for submiting the nickname
				saveBTN3 = canvas.create_window(width/2 , height/2 + x, window = save3, tag="savebuttons")
			
			if (no_files == 4):
				save4 = Button(window, text=files, highlightthickness = 0, font="OCRB 10 bold", background="grey", command = (lambda no = no_files: load_buttons(no) ))# button for submiting the nickname
				saveBTN4 = canvas.create_window(width/2 , height/2 + x, window = save4, tag="savebuttons")
			
			if (no_files == 5):
				save5 = Button(window, text=files, highlightthickness = 0, font="OCRB 10 bold", background="grey", command = (lambda no = no_files: load_buttons(no) ))# button for submiting the nickname
				saveBTN5 = canvas.create_window(width/2 , height/2 + x, window = save5, tag="savebuttons")



def leaderboard():
	canvas.delete("all")
	global background
	global go_back_btn
	background = PhotoImage(file="background1.png") # background of the start menu
	canvas.create_image(0, 0, image=background, anchor="nw")

	go_back_btn = Button(window, text="Go back", highlightthickness = 0, font="OCRB 10 bold", background="grey", command = start_menu)# button for submiting the nickname
	go_back = canvas.create_window(50, 700, window = go_back_btn)

	list = []
	with open("LEADERBOARD","r") as file:
		list= file.readlines()
	x = -200
	for i in range(0,5):
		if(len(list[i]) >= 3):
			place = str(i+1) + ". " + list[i]
		else:
			place = str(i+1) + ". ---------"
		canvas.create_text(width/2, height/2+x, text=place, font="OCRB 30 bold", fill="dark blue")
		x += 100



def quitting(): # this functions quits the game
	canvas.destroy()
	window.quit()

def start_menu():# this function creates the start menu
	canvas.pack()
	canvas.delete("all")
	global background
	global spacecraft
	global altitude
	altitude = 0
	background = PhotoImage(file="background1.png") # background of the start menu
	canvas.create_image(0, 0, image=background, anchor="nw")
	
	spacecraft = PhotoImage(file="character.png") # spawning the spacecraft for design purposed
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


#<----------------- Actual start of the program ----------------------->

width =1280 # setting the width
height =720 # setting the height
window = setWindowsDimensions(width, height)
canvas = Canvas(window, width=width, height=height, highlightthickness=0)

start_menu() 

window.mainloop()
