from source.utilities import *
import source.monitor as pywatcher
import json


__version__ = "1"


def load_watchers():
    """Loads watchers from the watchers.json file."""
    # An empty dictionary we can store the the watchers in once we finish unpacking them.
    watchers_in_prep = {}

    # Load the watchers from the watchers.json file.
    with open("./source/watchers.json", "r") as j:
        jsonified_watchers = json.load(j)   # Jasonify is a word, I just made it up.

    # Takes each watcher that was just loaded and un-jasonifies it.
    for k, v in jsonified_watchers.items():
        watchers_in_prep[k] = \
            pywatcher.Monitor(pywatcher.Host(v["target_host"]["ip"], v["target_host"]["friendly_name"]),
                              v["interval"], v["tolerance"], messages=v["logger"])

    return watchers_in_prep


# Now we load the actual watcher objects into a dictionary that we can work with.
watchers = load_watchers()


def save_watchers():
    """Packs watchers and stores them in watchers.json"""
    # An empty dictionary where we can store the watchers once we turn them to json compatible dictionaries.
    jsonified_watchers = {}

    # Go through all the watchers and pack them up.
    for k, v, in watchers.items():
        jsonified_watchers[k] = v.pack()

    # Save them to a file.
    with open("./source/watchers.json", "w") as w:
        json.dump(jsonified_watchers, w)


# Putting this first because it's the first step in creating a watcher.
def create_host() -> pywatcher.Host:
    """Creates a host object."""
    i = input("Host ip address: ")
    f = input("Host friendly name (optional): ")
    if f:
        return pywatcher.Host(i, f)
    else:
        return pywatcher.Host(i)


# This is the second step in creating a watcher so it goes second.
def register_watcher(watcher: pywatcher.Monitor):
    """Names watcher and adds it to the watchers list."""
    watcher_name = check_name("Name: ", watchers)
    watchers[watcher_name] = watcher


# This actually implements those steps and puts everything together.
def create_watcher():
    """Creates a watcher object."""
    host = create_host()
    interval = int_input("Time between pings: ")
    tolerance = int_input("Number of fails before host is reported down: ")
    output_file = input("Output file (leave blank for default): ")

    if output_file:
        watcher = pywatcher.Monitor(host, interval, tolerance, output_file)
    else:
        watcher = pywatcher.Monitor(host, interval, tolerance)

    register_watcher(watcher)
    input("Created watcher!")


def get_watchers_and_states() -> dict:
    """Creates a list of watchers with their current status."""

    # An empty dictionary to fill with the data that will be collected below.
    watchers_and_states = {}

    i = 1   # Iterator

    # Goes through each of the watchers and assigns them an index number starting at one,
    # Each key in the dictionary holds another dictionary with the name, status, and the watcher object.
    for k, v in watchers.items():
        watchers_and_states[i] = {"Name": k, "Status": v.get_state(), "watcher": v}
        i += 1

    return watchers_and_states


def present_watchers_and_states(watchers_and_states: dict):
    """
    Presents the current watchers along with their current states.
    States are Running or Stopped
    """

    # Goes through each watcher and prints it's index, name, and status.
    # Displays in this format: [1, CloudFlare, Running.]
    for k, v in watchers_and_states.items():
        print(f"{k}, {v['Name']}, {v['Status']}.")
    print("\n")


def present_watchers(watchers_and_states: dict):
    """"""

    for k, v in watchers_and_states.items():
        print(f"{k}, {v['Name']}.")
    print("\n")


def toggle_watcher_state(watcher):
    """Toggles watcher state.
    Will stop running watchers and start stopped watchers."""
    # Get the state of the watcher
    if watcher.get_state() == "Running":
        watcher.stop()      # If the watcher was running, stop it.
        print("Stopped")
    else:
        watcher.start()     # If the watcher wasn't runnig, start it.
        print("Started")


def list_and_toggle_watchers():
    """
    Lists watchers and accepts user input.
    Can turn watchers on or off.
    """
    # Instructions
    print("Please choose a watcher to start/stop or enter 0 to go back.")

    # Fetches the watcher's and their states, presents them, and prompts user for an answer
    options = get_watchers_and_states()
    present_watchers_and_states(options)
    answer = int_input("> ")

    if answer == 0:
        pass    # Returns to main menu if user submits a 0
    else:
        try:    # Attempts to toggle the watcher
            toggle_watcher_state(options[answer]["watcher"])
        except KeyError:      # If the user inputs an index number out of range, it will exit to the main menu.
            print(f"Sorry, that was an invalid entry.")
            input()


def list_and_delete_watcher():
    """
    Lists watchers and accepts user input.
    Can turn watchers on or off.
    """
    # Instructions
    print("Please choose a watcher to delete or enter 0 to go back.")

    # Fetches the watcher's and their states, presents them, and prompts user for an answer
    options = get_watchers_and_states()
    present_watchers(options)
    answer = int_input("> ")

    if answer == 0:
        pass    # Returns to main menu if user submits a 0
    else:
        try:    # Attempts to toggle the watcher
            del(watchers[options[answer]["Name"]])
        except KeyError:      # If the user inputs an index number out of range, it will exit to the main menu.
            print("Sorry, that was an invalid entry.")
            input()


def main():
    """The main CLI for interacting with watchers"""
    print("==============================================================")
    print(f"PyWatcher v{__version__}")
    print("By: Created by Andrew G, with help from Ashton Webster")
    print("And of course, big thanks to Stack Overflow")
    print("==============================================================")

    while True:
        # Main Menu
        print("Please choose an option")
        print("C - Create new watcher")
        print("L - List watchers and Start/Stop watchers")
        print("D - Delete watcher")
        print("S - Save watchers")
        print("Q - Save watchers and quit")
        command = input("> ").lower()
        clear()

        if command == "c":
            create_watcher()   # Creates a new watcher object
            clear()

        elif command == "l":
            list_and_toggle_watchers()
            clear()

        elif command == "d":
            list_and_delete_watcher()
            clear()
        elif command == "s":
            save_watchers()
            clear()

        elif command == "q":
            save_watchers()
            quit(0)

        else:
            print(f"\x1b[0;31;40m Sorry, that wasn't a valid command \x1b[0m")
    # End of main loop


if __name__ == "__main__":
    main()
