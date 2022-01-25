import re
import datetime

def match_regex(user_input,pattern):
    if re.fullmatch(pattern,user_input):
        return True
    else:
        return False


def create_new_file(file_name):
    with open(file_name, "x") as file:
        pass


def append_to_file(file_name, input_dict):
    with open(file_name, "a") as file:
        file.write(input_dict + "\n")


def validate_date(date_input):
    date_arr = date_input.split("-")
    try:
        start_date = datetime.datetime(int(date_arr[0]), int(date_arr[1]), int(date_arr[2]))
        start_date_formatted = start_date.strftime("%Y-%m-%d")
        if date_input == start_date_formatted:
            return True
        return False
    except ValueError:
        return False
