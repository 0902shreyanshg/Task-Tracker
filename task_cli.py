"""
task_cli.py - Command-line interface for the Task Tracker application.
Usage: python task_cli.py <command> [arguments]
"""

# To read user input we "import sys", as python revieves user input as a list
import sys
# json - reads and writes json files
import json
# os - checks if the file exists
import os
# for real timestamps
from datetime import datetime


# NOTE: USER INPUT:
#    user input: python FILE_NAME COMMAND ARGUMENT (eg: python task_cli.py add "Buy groceries")
#    python recieves this user input as a list: ['task_cli.py', 'add', 'Buy groceries']
#    this list is accessible via sys.argv :
#    - sys.argv = is the full list
#    - sys.argv[0] = To read the FILE_NAME
#    - sys.argv[1] = To read the COMMAND
#    - sys.argv[2] = To read the ARGUMENT

# * I. FILE_NAME: 
#    We don't need to explicitly read the FILE_NAME as sys.argv[0] is always the FILE_NAME

# * II. COMMANDS
if len(sys.argv) < 2:       #Edge case: where no COMMAND is given (after FILE_NAME), For a COMMAND to exist, you need atleast 2 elements - FILE_NAME + COMMAND
    print("Please provide a command")
else:
    command = sys.argv[1]
    if command == "add":

    # * III.A. ARGUMENT for "add"
    # add here is about adding NEW TASKS
        if len(sys.argv) < 3:       # Same edge case logic here as above in COMMAND
            print("Please provide a task description")
        else:
            argument = sys.argv[2]
            # NOTE: JSON: 
            #    - Universal format for storing and exchanging structured data as text
            #    - Every programming language can read and write it
            #    - Relevance here: PERSISTENCE
            #    PERSISTENCE: 
            #    the ability of data to outlive the specific process or application that created it
            #    options for PERSISTENCE: 
            #    - A database(MySQL, PostgreSQL): Overkill for a local CLI tool
            #    - A plain text file: No structure, hard to read back
            #    - JSON file: structured, simple, no setup required
            # *  i. define file name and load existing types
            filename = "tasks.json"
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    tasks = json.load(f)        # tasks = a Python list in memory containing all tasks. It's loaded from the file (or starts empty). Think of it as the full to-do list.
                                                # json.load(f) = read the contents of the opened file f and convert it from JSON into a Python list.
            else:
                tasks = []
            # *  ii. create a task dicitionary
            task = {        # a single dictionary representing one task you're about to add.
                "id": len(tasks) + 1,
                "description": argument,
                "status": "todo",
                "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),        # for live date and time 
                "updatedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            # *  iii. append and write back
            tasks.append(task)
            with open(filename, "w") as f:
                json.dump(tasks, f)     # json.dump converts the Python list tasks into JSON format and writes it into the file f. It's the reverse of json.load
            # *  iv. print confirmation
            print("Tasks added successfully (ID : " + str(task["id"]) + ")")
    elif command == "delete":
        print("delete command recieved")
    elif command == "update":
        print("update command recieved")
    elif command == "mark-in-progress":
        print("mark-in-progress command recieved")
    elif command == "mark-done":
        print("mark-done command recieved")
    elif command == "list":
    # * III.A. LIST all tasks
        # *  i. define file name and load existing types
        filename = "tasks.json"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                tasks = json.load(f)
        # *  ii. print tasks
            if len(tasks) == 0:
                print("No tasks found")
            else:
                for task in tasks:
                    print(task)
        else:
            print("No file found")
    else:
        print("Unknown command")
