"""
task_cli.py - Command-line interface for the Task Tracker application.
Usage: python task_cli.py <command> [description]
"""

# *
# sys - To read user input as python receives user input as a list
# json - reads and writes json files
# os - checks if the file exists
# datetime - for real timestamps 

import sys
import json
import os
from datetime import datetime


# NOTE: USER INPUT:
#       user input: python FILE_NAME COMMAND DESCRIPTION (eg: python3 task_cli.py add "Buy groceries")
#       python recieves this user input as a list: ['task_cli.py', 'add', 'Buy groceries']
#       this list is accessible via sys.argv :
#       - sys.argv = is the full list
#       - sys.argv[0] = To read the FILE_NAME
#       - sys.argv[1] = To read the COMMAND
#       - sys.argv[2] = To read the DESCRIPTION/ TASK_ID (in update)
#       - sys.argv[3] = To read the DESCRIPTION (in update)

# NOTE: JSON: 
#       - Universal format for storing and exchanging structured data as text
#       - Every programming language can read and write it
#       - Relevance here: PERSISTENCE
#   PERSISTENCE: 
#       the ability of data to outlive the specific process or application that created it
#       options for PERSISTENCE: 
#       - A database(MySQL, PostgreSQL): Overkill for a local CLI tool
#       - A plain text file: No structure, hard to read back
#       - JSON file: structured, simple, no setup required


# * I. FILE_NAME: 
#       Already typed in the USER INPUT in CLI. eg: python3 "task_cli.py" ....
#       Hence sys.argv[0] as input is not required


# * II. COMMANDS: 
#       - EDGE CASE: For a COMMAND to exist, you need atleast 2 elements
#       - add
#       - delete
#       - update
#       - mark-in-progress
#       - mark-done
#       - list
#       - unknown command

if len(sys.argv) < 2:       
    print("Please provide a command")
else:
    command = sys.argv[1]

    if command == "add":
    # * III. DESCRIPTION:
    #       i. EDGE CASE: For a DESCRIPTION to exist, you need atleast 3 elements
    #       ii. define file name and load existing tasks
    #           - filename = "tasks.json" : give a name to the file
    #           - os.path.exists(filename) : check file's existence
    #           - with open(filename, "r") as f : "r" here is for reading the file
    #           - json.load(f) : converts from JSON to python list
    #       iii. create a task dicitionary (for tasks you're about to add)
    #           - max(task["id"] for task in tasks) + 1 if tasks else 1 : 
    #           - datetime.now().strftime("%Y-%m-%d %H:%M:%S") : for live date and time
    #       iv. append & write back
    #           - json.dump(tasks, f) : converts python list tasks to JSON format & writes it into the file f
    #       v. print confirmation

        if len(sys.argv) < 3:
            print("Please provide a task description")
        else:
            argument = sys.argv[2]
            
            filename = "tasks.json"
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    tasks = json.load(f)
            else:
                tasks = []

            task = {
                "id": max(task["id"] for task in tasks) + 1 if tasks else 1,
                "description": argument,
                "status": "todo",
                "createdAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                "updatedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            tasks.append(task)
            with open(filename, "w") as f:
                json.dump(tasks, f)

            print("Tasks added successfully (ID : " + str(task["id"]) + ")")
    
    elif command == "delete":
    # * III. TASK_ID
    #       i. EDGE CASE: For a TASK_ID to exist, you need atleast 3 elements
    #           - int(sys.argv[2]) : sys.argv[2] is a string, but TASK_ID is integer
    # * IV. DESCRIPTION
    #       i. EDGE CASE: For a DESCRIPTION to exist, you need atleast 4 elements
    #       ii. define file name & load existing tasks
    #           - filename = "tasks.json" : give a name to the file
    #           - os.path.exists(filename) : check file's existence
    #           - with open(filename, "r") as f : "r" here is for reading the file
    #           - json.load(f) : converts from JSON to python list  
    #       iii. delete task
    #           - tasks = [task for task in tasks if task["id"] != task_id] : also known as LIST COMPREHENSION
    #                       (it rebuilds the list keeping only tasks whose id does not match)
    #       iv. write back
    #       v. print confirmation

        if len(sys.argv) < 3:
            print("Please enter the TASK_ID")
        else:
            task_id = int(sys.argv[2])

            filename = "tasks.json"
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    tasks = json.load(f)

                tasks = [task for task in tasks if task["id"] != task_id]

                with open(filename, "w") as f:
                    json.dump(tasks, f)
                    
                print("Task(s) deleted successfully (ID : " + str(task_id) + ")")

            else:
                print("File doesnot exist")
    
    elif command == "update":
    # * III. TASK_ID
    #       i. EDGE CASE: For a TASK_ID to exist, you need atleast 3 elements
    #           - int(sys.argv[2]) : sys.argv[2] is a string, but TASK_ID is integer
    # NOTE : loading the file before checking description doesn't break anything. But validating inputs before doing file I/O is better.
    # * IV. DESCRIPTION
    #       i. EDGE CASE: For a DESCRIPTION to exist, you need atleast 4 elements
    #       ii. define file name & load exisiting tasks
    #           - filename = "tasks.json" : give a name to the file
    #           - os.path.exists(filename) : check file's existence
    #           - with open(filename, "r") as f : "r" here is for reading the file
    #           - json.load(f) : converts from JSON to python list    
    #       iii. update description and time
    #       iv. write back
    #       v. print confirmation
    #           - task is like i iterator 

        if len(sys.argv) < 3:
            print("Please provide an ID")
        else:
            task_id = int(sys.argv[2])

            if len(sys.argv) < 4:
                print("Please provide a description")
            else:
                new_description = sys.argv[3]

                filename = "tasks.json"
                if os.path.exists(filename):
                    with open(filename, "r") as f:
                        tasks = json.load(f)
                    
                    for task in tasks:
                        if task["id"] == task_id:
                            task["description"] = new_description
                            task["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                    with open(filename, "w") as f:
                        json.dump(tasks, f)
                
                    print("Tasks updated successfully (ID : " + str(task_id) + ")")
                
                else:
                    print("No tasks found")

    elif command == "mark-in-progress":
    # * III. TASK_ID
    #       i. EDGE CASE
    #       ii. define file name & load existing tasks
    #       iii. update status and time
    #           - status : in-progress
    #       iv. write back
    #       v. print confirmation

        if len(sys.argv) < 3:
            print("Please provide TASK_ID")
        else:
            task_id = int(sys.argv[2])

            filename = "tasks.json"
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    tasks = json.load(f)

                for task in tasks:
                    if task["id"] == task_id:
                        task["status"] = "in-progress"
                        task["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                with open(filename, "w") as f:
                    json.dump(tasks, f)

                print("Tasks status changed to mark-in-progress successfully (ID : " + str(task_id) + ")")

            else:
                print("No tasks found")
    
    elif command == "mark-done":
    # * III. TASK_ID
    #       i. EDGE CASE
    #       ii. define file name & load existing tasks
    #       iii. update status and time
    #           - status : done
    #       iv. write back
    #       v. print confirmation

        if len(sys.argv) < 3:
            print("Please provide a TASK_ID")
        else:
            task_id = int(sys.argv[2])

            filename = "tasks.json"
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    tasks = json.load(f)
                
                for task in tasks:
                    if task["id"] == task_id:
                        task["status"] = "done"
                        task["updatedAt"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                with open(filename, "w") as f:
                    json.dump(tasks, f)

                print("Tasks status changed to done successfully (ID : " + str(task_id) + ")")

            else:
                print("No tasks found")
    
    elif command == "list":
    # * III. FILTER ARGUMENT
    #       i. define file name & load existing tasks
    #       ii. Check loaded tasks
    #       iii. filter tasks
    #       iv. print

        filename = "tasks.json"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                tasks = json.load(f)

                if len(tasks) == 0:
                    print("No tasks found")
                else:
                    
                    if len(sys.argv) < 3:
                        tasks_to_print = tasks
                    else:
                        filter_status = sys.argv[2]
                        tasks_to_print = [task for task in tasks if task["status"] == filter_status]
                    
                    for task in tasks_to_print:
                        print(task)

        else:
            print("No file found")
    
    else:
        print("Unknown command")
