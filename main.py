from commands import add_command, check_command, submit_command

file = '.\sheet3.xlsx'
HELP = "help"
QUIT = "quit"
ADD = "add"
CHECK = "check"
SUBMIT = "submit"
YES = "yes"

list_of_commands = """
    Possible commands
    help - print all possible commands
    quit - close program
    add path - is checking all xlsx file/s from path (you can pass directory path) for conflicts
    check - check all newly added files for conflicts
    submit - send data from added xlsx files if conflicts don't occur 

"""


def check_result(result):
    if result:
        return result
    else:
        return []


if __name__ == '__main__':
    excel_list = []
    events_list = []
    text = ""
    print("Input commands")
    while text != QUIT:
        text = input()
        text = text.split(" ")
        command = text[0].lower()
        arg = text[1] if len(text) > 1 else None
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
        elif command == SUBMIT:
            submit_command(events_list)
            print(f"{len(events_list)} events was submitted")
            events_list = []
        elif command == YES:
            text = QUIT
        else:
            print(f"Cannot recognize command {command}. To get all possible commands write help")

    print("Application is closing")
