from commands import add_command, check_command, print_command, submit_command
import colorama
HELP = "help"
QUIT = "quit"
ADD = "add"
CHECK = "check"
PRINT = "print"
SUBMIT = "submit"
CHANGE_MODE = "change_mode"
YES = "yes"

list_of_commands = """
    Possible commands
    help - print all possible commands
    quit - close program
    add <path> - is checking all xlsx file/s from path (you can pass directory path) for conflicts
    check - check all newly added files for conflicts
    print - print all events that were checked for conflicts and are ready to be submitted
    submit - send data from added xlsx files if conflicts don't occur 
    change_mode - change on/off checking with db mode
"""


def check_result(result):
    if result:
        return result
    else:
        return []


is_dbmode_on = False

if __name__ == '__main__':
    colorama.init()
    excel_list = []
    events_list = []
    text = ""
    print("Input commands. Type \"help\" to see a list of possible commands.")

    while text != QUIT:
        print(">", end="")
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
                elif events_list:
                    print(f"Are you sure, that you don't want to submit {len(events_list)} events to system")
                    print("Write yes if you want to exit without submitting files")
                    text = "are you sure"
                else:
                    text = QUIT
            elif command == HELP:
                print(list_of_commands)
            elif command == ADD and arg is not None:
                prev_length = len(excel_list)
                excel_list.extend(check_result(add_command(arg)))
                print(f"Successfully added {len(excel_list) - prev_length} excels")
            elif command == CHECK:
                prev_length = len(events_list)
                events_list.extend(check_result(check_command(excel_list, events_list)))
                print(f"Successfully added {len(events_list) - prev_length} event list(s) without conflicts")
                excel_list = []
            elif command == PRINT:
                print_command(events_list)
            elif command == SUBMIT:
                submit_command(events_list)
                print(f"{len(events_list)} events was submitted")
                events_list = []
            elif command == YES:
                text = QUIT
            elif command == CHANGE_MODE:
                is_dbmode_on = not is_dbmode_on
                print(f"DB mode change to {'on' if is_dbmode_on else 'off'}")
            else:
                print(f"Cannot recognize command {command}. To get all possible commands write help")
        except:
            print(f"Unexpected error occurred. Operation {command} cancelled.")


    print("Application is closing")
