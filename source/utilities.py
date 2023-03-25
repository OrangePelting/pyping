import platform
from os import system


def int_input(prompt: str = None) -> int:
    """
    Takes user input and attempts to convert it to an int.
    Will not progress until user provides a valid input.
        Parameters:
            prompt (str): The prompt that will be presented to the user.
    """
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter an integer.")
            continue


def check_name(prompt: str, taken_names: [dict, list]):
    """
    Takes user input and checks it against a list of names.
    Will not allow the user to leave until they enter a valid name.
        Parameters:
            prompt (str): The prompt that will be presented to the user.
            taken_names (dict, list): The list or dictionary with names to check for the user input again.
    """
    while True:     # This couldn't possibly go wrong...
        name = input(prompt)    # Asks user to propose a name.
        if name in taken_names:
            print("Sorry, that name is already taken!")     # Try again.
        else:
            return name


def clear():
    """Clears the terminal."""
    if platform.system().lower() == "windows":
        system("cls")       # For Windows
    else:
        system("clear")     # For Unix
