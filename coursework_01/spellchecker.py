
import time, os
import datetime

#dramatic starting
os.system('clear')
print("\n\nStarting the program . . .")
time.sleep(2)
os.system('clear')



#this function creates or rewrites the results folder
def folder(list,total,correct,incorrect,added,changed,moment,end_time,start_time):
	f = input("\nPlease insert the name of the file where you want to have the result (do not forget the extension) :")
	
	file = open(f,"w")
	file.write("")
	# be sure that if the folder already exists, it will be empty
	file.close()

	file = open(f, "a")
	#append the statistics
	file.write("The total number of words: " + str(total) + "\n")

	file.write("\nThe number of word spelt correctly: " + str(correct) + "\n")

	file.write("\nThe number of incorrect spelt words: " + str(incorrect) + "\n")
	
	file.write("\nThe number of words added to the dictionary: " + str(added) + "\n")
	
	file.write("\nThe number of words changed by the user accepting the suggested word: " + str(changed) + "\n")
	
	file.write("The time and date the input was spellchecked : ")
	
	file.write(moment.strftime("%H:%M:%S  %Y-%m-%d") + "\n")
	
	file.write(f"\nThe amount of time elapsed to spellcheck the input: {end_time - start_time}\n\n")
	
	#append the input
	for word in list: 
		file.write(word + " ")

	file.close()






#function which checks if the words given exist in EnglishWords.txt
#and if not, do the actions on it
def checking(list):
	total = len(list) #total number of word
	correct = 0 # number of correct words
	incorrect = 0 # number of incorrect words
	added = 0 # number of added words
	changed = 0 # number of changed words

	start_time = time.time() #the moment the spellchecking begins

	#copying the dictionary in a list for easier operations
	with open("EnglishWords.txt") as file:
		dictionary=file.read().split()
		file.close()
	ok1 = 1#checking every word given to see if it is in the dictionary or not
	for char in list:
		print(char +" ")

	for index in range(len(list)):
		word=list[index]
		 # contor to verify if we have some incorrect spelling words
		if (word in dictionary):
			if (ok1 == 0):
				for char in list:
					print(char +" ")

			print("\n")
			correct += 1
			ok1 = 1

		else: #the word is not in dictionary
			os.system('clear')
			#printing the words of the sentence
			for char in list:
				print(char +" ")
			ok1 = 0
			while True:

				print("\nOops, it seems that the word: '" + word +"' does not exist \U0001F625")
				cond=input("\nWhat do you want to do with this word?\n (1) Ignore it\n (2) Mark it\n (3) Add it to the dictionary\n (4) See a sugestion for this word \n ")
				
				if (cond == '1'): #ignore the word and go further
					incorrect += 1
					break

				elif (cond == '2'): #marking the word
					list[index] = "?" + word + "?"
					incorrect += 1
					break

				elif (cond == '3'): #adding the word to the dictionary
					#adding it to the list to sort it so we have
					#the words alphabetically ordered
					correct += 1
					added += 1

					dictionary.append(word)
					dictionary.sort()

					#rewriting the list in the dictionary files ("English.txt")
					file=open("EnglishWords.txt", "w")
					file.write("") #make sure the file is empty
					file.close()

					file=open("EnglishWords.txt", "a")

					for line in dictionary:
						file.write(line)
						file.write("\n")

					file.close()
					break

				elif (cond == '4'):#searching for a suggestion
					from difflib import SequenceMatcher

					maxim=-1 #we have a contor to memorise the maximum ratio between 2 words

					for suggestion in dictionary:
						#trying each word to see which one is the most simmilar
						similarity = SequenceMatcher(None, suggestion, word).ratio()
						if (maxim < similarity*100):
							#every time we have a new maximum, we memorise the word 
							maxim=similarity*100
							similarWord=suggestion
					
					#asking the user for the suggestion
					while True:
						
						cond=input("\nDid you want to type: '" + similarWord +"' ?\n (1) Yes\n (2)No\n")
						
						#changing the word in the list if yes
						if (cond == '1'):
							list[index]=similarWord
							correct += 1
							changed += 1
							break

						#just ignore it
						elif (cond == '2'):
							incorrect += 1
							break

						else: #if the input is not a command
							os.system('clear')
							print("\nThe command you just typed is not an actual command! Please type again! \U0001F615\n")
					break

				else: # if the input is not given
					os.system('clear')# ilustration purposes

					print("\nThe action you just typed is not an actual command, please try again! \U0001F615\n")
					for char in list:
						print(char +" ")

	end_time = time.time() #the moment of the end of spellchecking
	
	time.sleep(1.5)
	os.system('clear') # only ilustration purposes
	#printing the statistics
	print("The total number of words: " + str(total) + "\n")
	time.sleep(0.5)
	print("\nThe number of word spelt correctly: " + str(correct) + "\n")
	time.sleep(0.5)
	print("\nThe number of incorrect spelt words: " + str(incorrect) + "\n")
	time.sleep(0.5)
	print("\nThe number of words added to the dictionary: " + str(added) + "\n")
	time.sleep(0.5)
	print("\nThe number of words changed by the user accepting the suggested word: " + str(changed) + "\n")
	time.sleep(0.5)

	moment = datetime.datetime.now() #actual moment
	print ("The time and date the input was spellchecked : ")
	print(moment.strftime("%H:%M:%S  %Y-%m-%d") + "\n")
	
	time.sleep(0.5)
	#time elapsed
	print(f"\nThe amount of time elapsed to spellcheck the input: {end_time - start_time}")

	folder(list,total,correct,incorrect,added,changed,moment,end_time,start_time)
	os.system('clear') #ilustration purposes
	#after spellchecking the input menu
	while True:
		cond = input("\nDo you want to go back to (1) Main Menu or (2) Quit ? ")
		if (cond == '2'):
			print("\nQuitting the program. . . \U0001F634")
			time.sleep(2)

			os.system('clear')
			os._exit(0)

		elif (cond == '1'):
			break

		else:
			os.system('clear')
			print("\nThe command you just typed does not work, try again! \U0001F615")


# this function transforms the original word in alpha characters
def transform (initial):
	modified = "" #initialise a string

	for letter in initial:
		if (letter.isalpha()):
			letter = letter.lower()
			modified = modified + letter

	return modified




#------------------------------- The actual start of the program -----------------------------

print("Hello! How can I help you today?\U0001F600\n") #welcome

while True:
	print("\n(0) Quit the program\n" + "(1) Spellcheck a sentence\n" + "(2) Spellcheck a file\n")
	
	#asking for which action do you want to execute
	option=input("\nEnter the number of the action you want to be executed: ")
	
	if (option == '0'):
		#quiting
		print("\nQuitting the program. . . \U0001F634")
		time.sleep(2)

		os.system('clear')
		os._exit(0)
	
	elif (option == '1'):
		#asking for the sentence
		prop = input("\n Please enter the sentence you want to check: ")
		
		#splitting the sentence in words
		original_input = prop.split()
		words = []
		for char in original_input:
			words.append( transform(char) )
		#checking if the words exist

		checking(words)


	elif (option == '2'):

		while True:
			#asking for the name of the file you want to check
			file=input("\nPlease enter the name of the file you want to check( don't forget the extension): ")

			#checking if the file exist or not
			#if yes, check it, if not asking what do you want to do
			
			ok=0 # a contor for remebering the option

			try:
				f=open(file,"r")
				sentence=f.read()
				original_input=sentence.split()
				ok=1
				words = []
				for char in original_input:
					words.append( transform(char) )

				checking(words)

				file.close()

			except:

				if (ok == 1): # if we already did other staff
					break
				os.system('clear')
				print("\nThe file you just enterd does not exist. Please be sure that the file you wanted to type exists in the program folder\U0001F615")

				while True:
					#asking what do you want to do now, go back to checking or to main menu
					cond = input("\n\nDo you want to type file's name again (1) or return to main menu? (2): ")

					if (cond == '1'):
						break

					elif (cond == '2'):
						break

					else:
						os.system('clear')
						print("\nThis is not an actual command. \U0001F615")

				#executing the operation typed
				if (cond == '1'):
					continue

				else:
					break

	else:
		os.system('clear')
		print("\nThe input you just typed is not an actual command, please try again! \U0001F615")
		
#--------------------------------------------END-----------------------------------------------
# just to be 300 lines	