
# Importing string module
import string

def reading_words() -> set:
    "Reading the words from a file (words_alpha.txt)."
    # Using a context manager to read words from file
    with open('words_alpha.txt') as file:
        # Reading the words into a list
        readed = file.readlines()
    file.closed

    # Excluding the '\n' from the words while creating a set with a comprehension
    words = {word.replace('\n', '') for word in readed}
    # Returning the set of words
    return words


def count_letters(letters: set, words: set) -> list:
    "Count how many times each letter in the letters set argument shows in the words set argument."
    # Getting letters
    # Building a dictionary with how many times each letter shows in the words set
    letters_count = {letter: 0 for letter in letters} # Empty dict to add uppon 
    # Iterating over words and counting letters
    for letter in letters_count.keys(): 
        for word in words:
            # Adding occurencies of specific letter in a specific word 
            letters_count[letter] += word.lower().count(letter) 

    # Returning a list of tuples created by the items() method executed on a dict
    return letters_count.items()


if __name__ == "__main__":
    ##### BEGIN THE GAME #####
    # Getting all the words in the english vocabulary
    words = reading_words() # Type: set
    # Getting all the letters from the alphabet with the string module
    letters = set(string.ascii_lowercase)  # Type: set

    try:
        # Getting word size from the player, needs to be an int
        word_size = int(input("What's the size of the word? ")) # Converting input into an int
    # In case player digits some value there is not an int
    except ValueError:
        # Printing error message to the player
        print("\nPlease, select only valid numbers.\n")
        # Ending the script
        exit()

    # Rebuilding the words set with only words that have the same size as the player's word size(word_size)
    words = {word for word in words if len(word) == word_size}
    # Word that needs to be guessed (final string), builded as a list
    final_word = word_size * "_,".rstrip(',').split(',') # Will be used to print the word while guessing

    # Values to measure the performance of the algorithm
    # TODO: Tries limit logic
    tries = 0 # How many times the algorithm tried to guess 
    tries_limit = 10 # How many tries the algorithm has to guess the word
    rights = 0 # How many letters it got right
    
    # Guessing algorithm core, keep guessing while rights < word_size or tries > 10
    while rights < word_size:
        # Getting the information of how many times each letter shows in the entire words set
        # Sorting returned tuple by the second position [1] and reversing it
        """
         count_letters(letters, words)[0] == Letter
         count_letters(letters, words)[1] == How many times the letter repeats in the words set
        """
        letters_count = sorted(count_letters(letters, words), key = lambda letters_tuple: letters_tuple[1], reverse = True) # List of tuples
        # The first letter in the letters_count is the most repeated letter in the words set
        most_repeated_letter = letters_count[0][0]

        # Guess the letter by asking if the player word has the most repeated letter
        answer = input(f"Does your word have the letter '{most_repeated_letter.upper()}'? y/n ").lower()

        # Check if the word has the letter or not
        if answer == 'y':

            try:
                # Getting the positions of the letter from the player
                positions = input("This letter is in which positions? (write like this: x, x, x) ").split(', ') # List
                # Converting the input into an int list with the map function
                positions = list(map(lambda x: int(x), positions))
            # In case of the player digits somithing that is not an valid int
            except ValueError:
                # Print an error message
                print("\nPlease, write only valid numbers in the format that was presented (x, x, x)\n")
                # Ending the script
                exit()

            # Looping through positions
            for pos in positions:
                # Check if the positions are valid
                if pos > word_size:
                    # Printing error message if the position is greater than the word_size
                    print("\nYour word doesn't have that many letters. Please, select only valid positions\n")
                    # Ending the script
                    exit()

                # Rebuilding the words set with words that has the most_repeated_letter in the positions defined
                words = {word for word in words if word[pos - 1] == most_repeated_letter} # Rebuilding the set with a comprehension

                # Building the word into the final_word list
                # Replacing '_' with the most_repeated_letter in its respective positions
                final_word[pos - 1] = most_repeated_letter 

            # Adding to the rights variable
            # Using positions length to get how many positions were guessed right
            rights += len(positions) 

            # Only print the guessed letters if the letter guessed is not the last one
            if rights < word_size:
                # Writing the actual structure of the final_word to the player at the end of every right guess
                print('\n' + ''.join(final_word), '\n')

        # In case of the player word doesn't contain the letter that the algorithm guessed
        elif answer == 'n':
            # Rebuild the words set with words that doesn't have the most_repeated_letter in any position
            words = {word for word in words if word.count(most_repeated_letter) == 0}

            # Implementing the tries limit logic 
            tries += 1
            # If the number of tries is greater than the tries limit value, exit the program
            if tries > tries_limit:
                print("\nThis was my last try, I was unable to guess your word, I'm sorry...\n")
                # Ending the script
                exit()
            # If it is less, print the number of tries left and continue the loop
            else:
                # Print the number of tries left
                print(f"\n{tries_limit - tries} tries left.\n")
                # Continue the while loop
                continue
        
        # In case of the player doesn't responde with a valid option (y, n)
        else:
            # Break the loop and exit if the player doesn't type 'y' or 'n'
            print("\nPlease, next time select 'y' (yes) or 'n' (no)\n")
            # Ending the script
            exit()

        # Excluding the most repeated letter from the letters set
        letters.remove(most_repeated_letter)
    
    # Print the word guessed
    print(f"Your word is {''.join(final_word).upper()}!")