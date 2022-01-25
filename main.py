import ast
import json
import copy
from utils import *


class Project:
    def __init__(self, *args):
        if len(args) == 1:
            self.p_title = args[0].get("p_title")
            self.p_details = args[0].get("p_details")
            self.p_target = args[0].get("p_target")
            self.p_start_date = args[0].get("p_start_date")
            self.p_end_date = args[0].get("p_end_date")
        else:
            self.p_title = args[0]
            self.p_details = args[1]
            self.p_target = args[2]
            self.p_start_date = args[3]
            self.p_end_date = args[4]

    def generate_project_dict(self):
        return {"p_title": self.p_title, "p_details": self.p_details, "p_target": self.p_target,
                "p_start_date": self.p_start_date, "p_end_date": self.p_end_date}

    @staticmethod
    def print_projects(projects_list):
        for i, p_obj in enumerate(projects_list):
            p_num = i + 1
            print("Project {} Title: {}".format(p_num, p_obj.p_title))
            print("Project {} Details: {}".format(p_num, p_obj.p_details))
            print("Project {} Total Target: {}".format(p_num, p_obj.p_target))
            print("Project {} Start Date: {}".format(p_num, p_obj.p_start_date))
            print("Project {} End Date: {}".format(p_num, p_obj.p_end_date))
            print("########################################################")


class User:
    def __init__(self, *args):
        if len(args) == 1:
            self.f_name = args[0].get("f_name")
            self.l_name = args[0].get("l_name")
            self.email = args[0].get("email")
            self.password = args[0].get("password")
            self.mobile_num = args[0].get("mobile_num")
            self.projects = args[0].get("projects") if args[0].get("projects") is not None else []
        else:
            self.f_name = args[0]
            self.l_name = args[1]
            self.email = args[2]
            self.password = args[3]
            self.mobile_num = args[4]
            self.projects = []

    def generate_user_dict(self):
        return {"f_name": self.f_name, "l_name": self.l_name, "email": self.email,
                "password": self.password, "mobile_num": self.mobile_num, "projects": self.projects}

    def delete_project(self, p_title):
        if p_title in self.projects:
            self.projects.remove(p_title)
            with open("reg_users", "r") as file:
                users = file.readlines()
            with open("reg_users", "w") as file:
                for user in users:
                    if p_title in ast.literal_eval(user.strip()).get("projects"):
                        continue
                    else:
                        file.write(user)
                file.write(json.dumps(self.generate_user_dict()))
            with open("projects", "r") as file:
                projects = file.readlines()
            with open("projects", "w") as file:
                for project in projects:
                    if Project(ast.literal_eval(project.strip())).p_title != p_title:
                        file.write(project)
            print("Project '{}' deleted successfully".format(p_title))
        else:
            print("You can't delete a project that you didn't create")

    def create_project(self):
        p_title = input("Enter project title:\n")
        p_details = input("Enter project details:\n")
        p_target = int(input("Enter project total target:\n"))
        while 1:
            p_start_date = input("Enter project start date (yyyy-mm-dd):\n")
            if validate_date(p_start_date):
                break
            else:
                print("Please enter a valid project start date\n")
        while 1:
            p_end_date = input("Enter project end date (yyyy-mm-dd):\n")
            if validate_date(p_end_date):
                break
            else:
                print("Please enter a valid project end date\n")
        p_data = Project(p_title, p_details, p_target, p_start_date, p_end_date)
        append_to_file("projects", json.dumps(p_data.generate_project_dict()))
        print("Project Created Successfully\n")
        old_user_data = copy.deepcopy(self)
        self.projects.append(p_title)
        with open("reg_users", "r") as file:
            users = file.readlines()
        with open("reg_users", "w") as file:
            for user in users:
                if ast.literal_eval(user.strip()) == old_user_data.generate_user_dict():
                    continue
                else:
                    file.write(user)
            file.write(json.dumps(self.generate_user_dict()))

    @staticmethod
    def search_projects():
        search_method = int(input("Enter 1 to search by project title,\n2 to search by project start date\n"))
        if search_method == 1:
            search_title = input("Enter project title to search with: ")
            search_result = []
            with open("projects", "r") as f:
                projects = f.readlines()
                for project in projects:
                    current_project_obj = Project(ast.literal_eval(project.strip()))
                    if current_project_obj.p_title == search_title:
                        search_result.append(current_project_obj)
            return search_result
        elif search_method == 2:
            search_start_date = input("Enter project start date to search with (yyyy-mm-dd): ")
            if validate_date(search_start_date):
                search_result = []
                with open("projects", "r") as f:
                    projects = f.readlines()
                    for project in projects:
                        current_project_obj = Project(ast.literal_eval(project.strip()))
                        if current_project_obj.p_start_date == search_start_date:
                            search_result.append(current_project_obj)
                return search_result
            else:
                return "Please enter a valid date"
        else:
            return "Invalid input. Please enter 1 or 2 to make an action."

    @staticmethod
    def view_projects():
        with open("projects", "r") as file:
            projects = file.readlines()
            for i, project in enumerate(projects):
                p_obj = Project(ast.literal_eval(project.strip()))
                p_num = i + 1
                print("Project {} Title: {}".format(p_num, p_obj.p_title))
                print("Project {} Details: {}".format(p_num, p_obj.p_details))
                print("Project {} Total Target: {}".format(p_num, p_obj.p_target))
                print("Project {} Start Date: {}".format(p_num, p_obj.p_start_date))
                print("Project {} End Date: {}".format(p_num, p_obj.p_end_date))
                print("########################################################")

    @staticmethod
    def register():
        f_name = input("Enter your first name:\n")
        l_name = input("Enter your last name:\n")
        while 1:
            email = input("Enter your email:\n")
            if match_regex(email, r".*@[a-zA-Z]+\.[a-zA-Z]+"):
                break
            else:
                print("Please enter a valid email\n")
        password = input("Enter your password:\n")
        while 1:
            conf_password = input("Confirm your password:\n")
            if conf_password == password:
                break
            else:
                print("Your password doesn't match, please re-enter\n")
        while 1:
            mobile_num = input("Enter your mobile number preceded by '+20' :\n")
            if match_regex(mobile_num, r"\+20[0-9]{10}"):
                break
            else:
                print("Please enter a valid mobile number\n")
        while 1:
            try:
                with open("reg_users", "r") as file:
                    users = file.read()
                if email not in users:
                    user_data = {"f_name": f_name, "l_name": l_name, "email": email,
                                 "password": password, "mobile_num": mobile_num, "projects": []}
                    append_to_file("reg_users", json.dumps(user_data))
                    return User(user_data)
                else:
                    return "This email is already Registered\n"
            except FileNotFoundError:
                create_new_file("reg_users")
                continue

    @staticmethod
    def login():
        email = input("Email: ")
        password = input("Password: ")
        with open("reg_users", "r") as file:
            users = file.readlines()
            for line_num, user in enumerate(users):
                if email in user:
                    user_obj = User(ast.literal_eval(user.strip()))
                    if password == user_obj.password:
                        print("Logged in successfully\nWelcome {} !".format(user_obj.f_name))
                        return user_obj
                    else:
                        return "Wrong password!, try again\n"
                if line_num == len(users) - 1:
                    return "There is no registered account with this email\n"
# Main run


user_first_input = int(input("Enter 0 to register, 1 to login, or 2 to exit!\n"))

if user_first_input == 0:
    logged_user = User.register()
    if type(logged_user) is str:
        print(logged_user)
elif user_first_input == 1:
    logged_user = User.login()
    if type(logged_user) is str:
        print(logged_user)
    else:
        while True:
            project_input = int(input("Enter 1 to create new project, 2 to list all projects,"
                                      "\n3 to search for a project, 4 to delete a project\nor 5 to exit\n"))
            if project_input == 1:
                logged_user.create_project()
            elif project_input == 2:
                logged_user.view_projects()
            elif project_input == 3:
                search_output = logged_user.search_projects()
                if type(search_output) == list:
                    if len(search_output) == 0:
                        print("No matches found")
                    else:
                        Project.print_projects(search_output)
                else:
                    print(search_output)
            elif project_input == 4:
                p_title_del = input("Enter the title of the project you want to delete: ")
                logged_user.delete_project(p_title_del)
            elif project_input == 5:
                break
            else:
                print("Invalid input. Please enter 1 or 2 or 3 or 4 or 5 to make an action.")
elif user_first_input == 2:
    exit()
else:
    print("Invalid input. Please enter 0 or 1 or 2 to make an action.")
