import time, os

#function which checks if the words given exist in EnglishWords.txt
def checking(list):

	for word in list:
		with open('EnglishWords.txt') as file:

				if (word in file.read()):
					print(word + "\n")
	file.close()


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
		


	