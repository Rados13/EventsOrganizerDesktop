import os
from typing import List
from commands import add_command, check_command, print_events_command, print_files_command, submit_command, \
    remove_command
import colorama

HELP = "help"
QUIT = "quit"
ADD = "add"
REMOVE = "remove"
CHECK = "check"
PRINT = "print"
SUBMIT = "submit"
CHANGE = "change"
YES = "yes"

list_of_commands = """
    Possible commands
    help - print all possible commands
    quit - close program
    add <path> - is checking all xlsx file/s from path (you can pass directory path) for conflicts
    check - check all newly added files for conflicts
    print <events/files> - print all events that were checked for conflicts and are ready to be submitted or all added files
    submit - send data from added xlsx files if conflicts don't occur 
    change <mode/suggest> - change on/off checking with database mode <mode> or finding suggestions <suggest>
"""


def check_result(result):
    if result:
        return result
    else:
        return []


is_dbmode_on = False
is_suggest_on = False
is_yes_awaiting = False


def dbmode_str():
    return 'on' if is_dbmode_on else 'off'


def suggest_str():
    return 'on' if is_suggest_on else 'off'


def span(predicate, list: List[str]) -> (List[str], List[str]):
    repeated = []
    new_values = []
    for elem in list:
        if predicate(elem):
            repeated.append(elem)
        else:
            new_values.append(elem)
    return repeated, new_values


if __name__ == '__main__':
    colorama.init()
    excel_list = []
    events_list = []
    text = ""
    print("Input commands. Type \"help\" to see a list of possible commands.")

    while text != QUIT:
        print(f"db_mode={dbmode_str()}|suggest={suggest_str()}>", end="")
        text = input()
        text = text.split(" ")
        command = text[0].lower()
        arg = text[1] if len(text) > 1 else None
        try:
            if command == QUIT:
                if excel_list:
                    print("Are you sure, that you don't want to check these files", " ".join(excel_list))
                    print("Write yes if you want to exit without checking files")
                    text = "are you sure"
                    is_yes_awaiting = True
                elif events_list:
                    print(f"Are you sure, that you don't want to submit {len(events_list)} events to system")
                    print("Write yes if you want to exit without submitting files")
                    text = "are you sure"
                    is_yes_awaiting = True
                else:
                    text = QUIT
            elif command == HELP:
                print(list_of_commands)
            elif command == ADD and arg is not None:
                prev_length = len(excel_list)
                path = os.path.realpath(arg)
                add_command_result = check_result(add_command(path))
                repeated, new_values = span(lambda elem: elem in excel_list, add_command_result)
                excel_list.extend(new_values)
                [print(f"File {elem} added again") for elem in repeated]
                print(f"Successfully added {len(new_values)} excel files")
            elif command == REMOVE and arg is not None:
                path = os.path.realpath(arg)
                to_remove = remove_command(excel_list, path)
                for i in to_remove:
                    excel_list.remove(i)
                print(f"Successfully removed {to_remove}.")
            elif command == CHECK:
                to_remove = [excel for excel in excel_list if not os.path.isfile(excel)]
                if len(to_remove) > 0:
                    for i in to_remove:
                        excel_list.remove(i)
                    print(f"Files {to_remove} no longer exist. Removing from an internal list.")
                events_list = check_result(check_command(excel_list, is_dbmode_on, is_suggest_on))
                print(f"Successfully added {len(events_list)} events without conflicts")
            elif command == PRINT and arg == "events":
                print_events_command(events_list)
            elif command == PRINT and arg == "files":
                print_files_command(excel_list)
            elif command == SUBMIT:
                submit_command(events_list)
                print(f"{len(events_list)} events were submitted")
                events_list = []
                excel_list = []
            elif command == YES and is_yes_awaiting:
                text = QUIT
            elif command == CHANGE:
                if arg == 'mode':
                    is_dbmode_on = not is_dbmode_on
                    print(f"DB mode change to {dbmode_str()}")
                elif arg == 'suggest':
                    is_suggest_on = not is_suggest_on
                    print(f"Suggestions changed to {suggest_str()}")
            else:
                print(f"Cannot recognize command {command}. To get all possible commands write help")

            if command != QUIT:
                is_yes_awaiting = False
        except:
            print(f"Unexpected error occurred. Operation {command} cancelled.")

    print("Application is closing")
