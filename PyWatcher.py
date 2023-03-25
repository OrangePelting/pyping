from os import system, name
import source.monitor as pywatcher
import json


def create_host():
    i = input("Host ip address: ")
    f = input("Host friendly name (optional): ")
    if f:
        return pywatcher.Host(i, f)
    else:
        return pywatcher.Host(i)


def int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter an integer.")
            continue


def create_watcher(h):
    tbp = int_input("Time between pings: ")
    nofbhird = int_input("Number of fails before host is reported down: ") # Because fuck you! That's why.
    output_file = input("Output file (leave blank for default): ")
    if output_file:
        return pywatcher.Monitor(h, tbp, nofbhird, output_file)
    else:
        return pywatcher.Monitor(h, tbp, nofbhird)


def check_name(prompt, check_against):

    while True:
        n = input(prompt)
        if n in check_against:
            print("Sorry, that name is already taken!")
            continue
        else:
            return n


def list_watchers():
    watcher_list = ""
    for w in watchers:
        watcher_list += f"{w}\n"
    return watcher_list


def clear():
    if name == "nt":
        system("cls")
    else:
        system("clear")


def load_watchers():
    watchers_in_prep = {}
    with open("./source/watchers.json", "r") as j:
        jsonified_watchers = json.load(j)
    for k, v in jsonified_watchers.items():
        watchers_in_prep[k] = \
            pywatcher.Monitor(pywatcher.Host(v["target_host"]["ip"], v["target_host"]["friendly_name"]),
                              v["interval"], v["tolerance"], messages=v["logger"])
    return watchers_in_prep


watchers = load_watchers()


def save_watchers():
    jsonified_watchers = {}
    for k, v, in watchers.items():
        jsonified_watchers[k] = v.pack()
    with open("./source/watchers.json", "w") as w:
        json.dump(jsonified_watchers, w)


def get_watchers_and_states():
    watchers_menu = {}
    i = 1
    for k, v in watchers.items():
        watchers_menu[i] = {"Name": k, "Status": v.get_state(), "watcher": v}
        i += 1
    return watchers_menu


def toggle_watcher_state(w):
    if w.get_state() == "Running":
        w.stop()
        print("Stopped")
    else:
        w.start()
        print("Started")


while True:
    # Main Menu
    print("Please choose an option")
    print("C - Create new watcher")
    print("L - List watchers")
    print("S - Start/Stop watcher")
    print("D - Delete watcher")
    print("W - Save watchers")
    print("Q - Save watchers and quit")
    command = input("> ").lower()
    clear()

    if command == "c":
        watcher = create_watcher(create_host())
        watcher_name = check_name("Name: ", watchers)
        input("Created watcher!")
        watchers[watcher_name] = watcher
        clear()
    elif command == "l":
        print(list_watchers())
        input()
    elif command == "s":
        print("Please choose a watcher to start/stop or enter 0 to go back.")
        options = get_watchers_and_states()
        for key, value in options.items():
            print(f"{key}, {value['Name']}, {value['Status']}.")
        print("\n")
        answer = int_input("> ")
        if answer == 0:
            continue
        else:
            try:
                toggle_watcher_state(options[answer]["watcher"])
            except IndexError:
                print("Sorry, that entry is invalid.")

    elif command == "d":
        pass
    elif command == "w":
        save_watchers()
    elif command == "q":
        save_watchers()
        quit(0)
    else:
        print(f"\x1b[0;31;40m Sorry, that wasn't a valid command \x1b[0m")
