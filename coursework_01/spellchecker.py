import time, os
#dramatic starting
print("Starting the program . . .")
time.sleep(2)
os.system('clear')

#function which checks if the words given exist in EnglishWords.txt
#and if not do the actions on it
def checking(list):
	#printing the words of the sentence  
	print("\n ")
	for word in list:
		print(word +" ")
	print("\n")

	#copying the dictionary in a list for easier operations
	with open('EnglishWords.txt') as file:
		dictionary=file.read().split()
		file.close()
	#checking every word given
	for index in range(len(list)):
		word=list[index]

		if (word in dictionary):
			print("\n"+word)

		else: #the word is not in dictionary
			print("\nOops, it seems that the word: '" + word +"' does not exist\n")
			print()
			
			while True:
				cond=input("What do you want to do with this word?\n (1) Ignore it\n (2) Mark it\n (3) Add it to the dictionary\n (4) See a sugestion for this word \n")
				
				if (cond == '1'): #ignore the word and go further
					break

				elif (cond == '2'): #marking the word
					list[index] = "?" + word + "?"
					break

				elif (cond == '3'): #adding the word to the dictionary
					#adding it to the list to sort it so we have
					#the words alphabetically ordered

					dictionary.append(word)
					dictionary.sort()

					#rewriting the list in the dictionary files ("English.txt")
					file=open("EnglishWords.txt", "w")
					file.write("")
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
							break
						#just ignore it
						elif (cond == '2'):
							break

						else: #if the input is not a command
							print("The command you just typed is not an actual command! Please type again!\n")
					break

				else: # if the input is not given
					print("The action you just typed is not an actual command, please try again!\n")



# The actual start of the program
print("Hello! What action do you want to execute today?\n") #welcome

while True:
	print("(0) Quit the program\n" + "(1) Spellcheck a sentence\n" + "(2) Spellcheck a file\n")
	#asking for which action do you want to execute
	option=input("Enter the number of the action you want to be executed: ")
	
	if (option == '0'):
		#quiting
		print("\nQuitting the program. . .")
		time.sleep(2)

		os.system('clear')
		os._exit(0)
	
	elif (option == '1'):
		#asking for the sentence
		prop = input("\n Please enter the sentence you want to check: ")
		
		#splitting the sentence in words
		words = prop.split()

		#checking if the words exist
		checking(words)


	elif (option == '2'):

		while True:
			#asking for the name of the file you want to check
			file=input("\nPlease enter the name of the file you want to check( don't forget the extension): ")

			#checking if the file exist or not
			#if yes, check it, if not asking what do you want to do

			try:

				f=open(file,"r")
				sentence=f.read()
				words=sentence.split()

				checking(words)
				file.close()

			except:
				print("The file you just enterd does not exist. ")

				while True:
					#asking what do you want to do now, go back to checking or to main menu
					cond = input("\n\nDo you want to type file's name again (1) or return to main menu? (2): ")

					if (cond == '1'):
						break

					elif (cond == '2'):
						break

					else:
						print("This is not an actual command.")

				#executing the operation typed
				if (cond == '1'):
					continue

				else:
					break

	else:

		print("\nThe input you just typed is not an actual command, please try again!")
		

	