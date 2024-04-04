# Star Wars API (swapi)
# All the data is accessible through the HTTP web API
# No authentication is required to query and get data
# I have used the API to attain characters and starships along with their further info
# The random selections are selected by ID's of characters and starships
# Using the APIs search function '?search=', you can search with a string

# Import requests module. Used for making HTTP requests e.g. get
import requests

# Import randint (random integer) function from random module. Used for getting random characters and starships
from random import randint

# Import choice method from random module. Used for choosing a range of integers for randint to select from
from random import choice

# Print Star Wars decorative heading
# print(r) displays the text in raw form (as its displayed here)
print(r"""
  ___| |_ __ _ _ __  __      ____ _ _ __ ___ 
 / __| __/ _` | '__| \ \ /\ / / _` | '__/ __|
 \__ \ || (_| | |     \ V  V / (_| | |  \__ \
 |___/\__\__,_|_|      \_/\_/ \__,_|_|  |___/
""")

# Input for user to input their name. Used below in the story section
name = input("What is your name? ")

# Introduction to the story, your character (with inputted name) and your mission
# This is the traditional start to all Star Wars films.
# print(f) allows the user input name to be added into the text
print(rf"""
              .   A terrible civil war burns throughout the  .        .     .
                 galaxy: a rag-tag group of freedom fighters   .  .
     .       .  has risen from beneath the dark shadow of the            .
.        .     evil monster the Galactic Empire has become.                  .
   .             Imperial  forces  have  instituted  a reign of   .      .
             terror,  and every  weapon in its arsenal has  been
          . turned upon the Rebels  and  their  allies:  tyranny, .   .
   .       oppression, vast fleets, overwhelming armies, and fear.        .  .
.      .  Fear  keeps  the  individual systems in line,  and is the   .
         prime motivator of the New Order.             .
    .      Outnumbered and outgunned,  the Rebellion burns across the   .    .
.      vast reaches of space and a thousand-thousand worlds, with only     .
    . their great courage - and the mystical power known as the Force -
     flaming a fire of hope.                                    .
       A rebel hero rises from the ranks. You, Commander {name}, create a   .
 . plan to infiltrate the infamous Death Star and destroy it, knowing its your
  only hope for rebel survival. Now you have to pick two other rebels to join you  .
 on your quest, as well as a trusty Starship to stealthily take you on your mission.            .         .
""")

# 'Flight log' is the txt file that the selections are stored in
print("Once you've made your selections, you will be given a flight log with your team members, starship, and further "
      "info.")

# Root url of Star Wars API
url = "https://swapi.dev/api/"

# Empty list that will be filled throughout program
user_team = []


# Function that selects a character at random
def get_random_char():

    # Allows the randint function to select a random number from 1-81
    random_choice = randint(1, 81)

    # Sends request to the people section of the API with a random integer
    # .json() method converts received json data to python dictionary
    random_response = requests.get(f"{url}people/{random_choice}/").json()

    # Prints the name of the randomly chosen character
    # Using the key name from the dictionary of the character's information, the value is added
    print("Random choice: ", random_response['name'])

    # Creates the dictionary char_info and adds the key value pairs
    char_info = dict(name=random_response["name"], height=random_response["height"], mass=random_response["mass"])

    # Appends (or adds) the character information to the list 'user_team'
    user_team.append(char_info)


# Function that selects a starship at random
# Uses similar code to get_random_char with slightly different integer selection and url
def get_random_starship():

    # Many of the starship ID's on the API produced 404 errors, so I used ranges of ID's that worked
    # The choice() method returns a randomly selected element from the specified sequence
    r = choice([(2, 3), (9, 13), (21, 23), (27, 29), (31, 32), (39, 41)])
    random_choice = randint(*r)

    random_response = requests.get(f"{url}starships/{random_choice}/").json()

    print("Random choice: ", random_response['name'])

    starship_info = dict(name=random_response["name"], model=random_response["model"],
                         hyperdrive_rating=random_response["hyperdrive_rating"])

    user_team.append(starship_info)


# Defines function that allows user to choose a character
def get_character(user_char):

    # Sends get request to the url, requesting a specific character from the people section of the API
    # Converts information to dictionary using .json() method
    response = requests.get(f"{url}people/?search={user_char}").json()

    # If else statement to determine character selection based on results amount
    # If there are no characters matching the name searched, run the following:
    if response["count"] == 0:

        # Try and except loop
        # Test to see if user team contains 2 elements
        try:
            print(f"This is your team so far:\n{user_team[0]} and {user_team[1]}")

        # When an index error occurs running the previous line, this section will run
        except IndexError:

            print("\nNo character exists with that name, please choose again.")

            # Input to allow user to select another character
            user_char_att2 = input("Please type in your chosen character or type random for a random selection: ")

            # If the user chooses to select a random character, run the random character function
            if user_char_att2.lower() == "random":
                get_random_char()
            # If the user chooses a character, run the character selection function using their input as argument
            else:
                get_character(user_char_att2)

    # If there is only 1 character
    elif response["count"] == 1:

        # Selects the dictionary at the 0th index of the response results (the character data)
        char_data = response["results"][0]

        # Creates the dictionary char_info and adds the key value pairs
        char_info = dict(name=char_data["name"], height=char_data["height"], mass=char_data["mass"])

        user_team.append(char_info)

    # If more than 1 character
    elif response["count"] >= 2:
        char_data = response["results"]

        # Loops through the several characters that have matched the inputted name
        for char in char_data:
            # Displays the characters full names, prompting the user to choose one
            print(char["name"])

        # Run the character selection function using their input as argument
        get_character(
            input("These are the multiple characters for your search term, please enter your chosen full name: "))


# Same as get_character() but with starships
def get_starship(starship_choice):
    response = requests.get(f"{url}starships/?search={starship_choice}").json()
    if response["count"] == 0:
        try:
            print(f"This is your team so far:\n{user_team[0]} and {user_team[1]}, flying in {user_team[2]}")
        except IndexError:
            print("No starship exists with that name, please choose again.")
            user_starship_att2 = input("Please type in your chosen starship or type random for a random selection: ")
            if user_starship_att2.lower() == "random":
                get_random_starship()
            else:
                get_starship(user_starship_att2)
    elif response["count"] == 1:
        starship_data = response["results"][0]
        starship_info = dict(name=starship_data["name"], model=starship_data["model"],
                             hyperdrive_rating=starship_data["hyperdrive_rating"])
        user_team.append(starship_info)
    elif response["count"] >= 2:
        starship_data = response["results"]
        for starship in starship_data:
            print(starship["name"])
        get_starship(
            input("These are the multiple starships for your search term, please enter your chosen full name: "))


# User input as a string with '\n' as a new line break for usability
user_char1 = input("\nWhich Star Wars character would you like as your first team member? "
                   "\nType a name or write random for a random character selection: ")

# If the user types random, run the get_random_char function
if user_char1.lower() == "random":
    get_random_char()
# If the character is chosen instead, run the get_character function using their input as the argument
else:
    get_character(user_char1)

# Prints the 0th index of the user_team list specifying the name key
print(f"Your team so far is: {user_team[0]["name"]}")

user_char2 = input("\nWhich Star Wars character would you like as your second team member? "
                   "\nType a name or write random for a random character selection: ")

# Second character selection
if user_char2.lower() == "random":
    get_random_char()
else:
    get_character(user_char2)

print(f"Your team so far is: {user_team[0]["name"]} and {user_team[1]["name"]}")

user_starship = input("\nWhich Star Wars starship would you like as your ride? "
                      "\nType a name or write random for a random starship selection: ")

if user_starship.lower() == "random":
    get_random_starship()
else:
    get_starship(user_starship)

print(f"\nYour final team is: {user_team[0]["name"]} and {user_team[1]["name"]}, "
      f"flying in a {user_team[2]["name"]}")

# Creates and writes a txt file called flight_log
# 'w' creates a file if none exist in that name and edits it if it does exist
with open("flight_log.txt", "w") as f:

    # f.write writes to the file
    f.write(r"""
  ___| |_ __ _ _ __  __      ____ _ _ __ ___ 
 / __| __/ _` | '__| \ \ /\ / / _` | '__/ __|
 \__ \ || (_| | |     \ V  V / (_| | |  \__ \
 |___/\__\__,_|_|      \_/\_/ \__,_|_|  |___/
""")

    # Write to file the following statement, including the user input name
    f.write(f"\nGood luck Commander {name} on your mission to destroy the Death Star! \nHere is your flight log with "
            f"information about your team members and starship:\n")

    # Writes the user_team list to the txt file
    # loops through the list and the dictionaries within it
    for data in user_team:

        # Iterates over each dictionary and extracts keys and values using items method
        for key, value in data.items():

            # Writes the information to the file
            f.write('\n%s:%s' % (key, value))

            # If the key is mass, go onto a new line for document readability
            if key == "mass":
                f.write("\n")
                
