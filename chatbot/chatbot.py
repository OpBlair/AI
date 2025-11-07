#the Brain
import json
import random
import datetime
import nltk
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
BOT_NAME = "Friday"
# 1. SETUP
# load intents data once when scripts starts
try:
	with open('intents.json') as file:
		intents = json.load(file)
except FileNotFoundError:
	print("Erro: intents.json not found. Make sure the file is in the same directory.")
	intents = {"intents": []}

#Processing the Input
#def preprocess_input(user_input):
	#convert input to lowercase and remove leading/trailing spaces
#	return user_input.lower().strip()

def preprocess_input(user_input):
    # 1. Tokenize (split sentence into individual words)
    tokens = nltk.word_tokenize(user_input)
    
    # 2. Lemmatize and lowercase each word
    lemmas = [lemmatizer.lemmatize(word.lower()) for word in tokens]
    
    # 3. Join them back into a string for matching
    return ' '.join(lemmas)

#time based response
def get_time_based_greeting():
	current_hour = datetime.datetime.now().hour
	if 5 <= current_hour < 12:
		return "Good morning!"
	elif 12 <= current_hour < 18:
		return "Good afternoon!"
	else:
		return "Good evening!"
def get_current_time():
	now = datetime.datetime.now()
	return now.strftime("The current time is %I:%M %p.")


#Finding the response
def chatbot_response(user_input):
	processed_input = preprocess_input(user_input)

	#Loop through every intent
	for intent in intents['intents']:
		#Loop through every pattern within the current intent
		for pattern in intent.get('patterns', []):
			#Check if the exact pattern is found inside the user's cleaned input
			if pattern in processed_input:
				#Found a match! Pick a random response and stop the function immediately
				response = random.choice(intent['responses'])

				#check for name placeholder and format if necessary
				if "{BOT_NAME}" in response:
					return response.format(BOT_NAME=BOT_NAME)
				#=== time/context logic
				if intent['tag'] == 'greeting':
					return get_time_based_greeting()
				elif intent['tag'] == 'time_query':
					#if user asks for time
					return get_current_time()
				#Default logic	
				return response
				

	# === FALLBACK ===
	#If the code reaches this point, no match was found.
	#We find and return a response from the 'fallback' intent.
	for intent in intents['intents']:
		if intent['tag'] == 'noanswer':
			return random.choice(intent['responses'])
	return "Error: Fallback intent not defined."

#Main chat Loop
def chat():
	print("Chatbot: Hi there! Type 'exit' to end the conversation.")
	while True:
		user_input = input("You: ")

		#Check for exit condition
		if user_input.lower() == 'exit':
			print("Chatbot: Goodbye!")
			break

		#Get response using the main logic
		response = chatbot_response(user_input)
		print("Chatbot:", response)

if __name__ == "__main__":
	chat()