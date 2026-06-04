"""
task_cli.py - Command-line interface for the Task Tracker application.
Usage: python task_cli.py <command> [description]
"""
#-------------------------------------------------------------------------------------------------------------------------------------
# NOTE: CLI
#
#       USER INPUT: 
#       python3 FILE_NAME COMMAND DESCRIPTION (eg: python3 task_cli.py add "Buy groceries")
#       python receives this user input as a LIST: ['task_cli.py', 'add', 'Buy groceries']
#       this LIST is accessible via sys.argv :
#       - sys.argv = is the full list
#       - sys.argv[0] = To read the FILE_NAME
#       - sys.argv[1] = To read the COMMAND
#       - sys.argv[2] = To read the DESCRIPTION/ TASK_ID
#       - sys.argv[3] = To read the DESCRIPTION


# NOTE: FILE-SYSTEM 
#
#       JSON:
#       Universal format for storing and exchanging structured data as text
#       Every programming language can read and write it
#       Relevance here: PERSISTENCE
#
#       PERSISTENCE: 
#       the ability of data to outlive the specific process or application that created it
#       options for PERSISTENCE: 
#       - A database(MySQL, PostgreSQL): Overkill for a local CLI tool
#       - A plain text file: No structure, hard to read back
#       - JSON file: structured, simple, no setup required
#-------------------------------------------------------------------------------------------------------------------------------------


# * IMPORT MODULES
#
# CLI 
#   import sys : To read user input
#
# FILE-SYSTEM
#   import os : checks if the file exists
#   import json : reads and writes json files
#
#   from datetime import datetime : for real timestamps 

import sys
import json
import os
from datetime import datetime


# * I. FILE_NAME: 
#       Already in USER INPUT in CLI. eg: python3 "task_cli.py" ....
#       Hence sys.argv[0] as input not required


# * II. COMMANDS: 
#       i. EDGE CASE: For a COMMAND to exist, you need atleast 2 elements
#       ii. add
#       iii. delete
#       iv. update
#       v. mark-in-progress
#       vi. mark-done
#       vii. list
#       viii. unknown command

if len(sys.argv) < 2:       
    print("Please provide a command")
else:
    command = sys.argv[1]

    if command == "add":
    # * III. DESCRIPTION:
    #       i. EDGE CASE: For a DESCRIPTION to exist, you need atleast 3 elements
    #       ii. define file name and load EXISTING tasks
    #           - filename = "tasks.json" :                                     stores the filename in a variable for reuse
    #           - if os.path.exists(filename) :                                 checks file's existence
    #           - with open(filename, "r") as f :                               "r" here is for reading the file
    #           - tasks = json.load(f) :                                        converts from JSON to python list & stores in tasks
    #           - else: tasks = [] :                                            if file doesnot exist, empty list (tasks) is created
    #       iii. create a task dicitionary (for tasks you're about to add)
    #           - task = {...} :                                                argument = sys.argv[2] gets used here to make new task
    #           - max(task["id"] for task in tasks) + 1 if tasks else 1 :       take the max id in the list and add 1 BUT if list is empty, use 1 
    #           - datetime.now().strftime("%Y-%m-%d %H:%M:%S") :                for live date and time
    #       iv. append NEW tasks & write back in file
    #           - json.dump(tasks, f) :                                         converts tasks (python list) to JSON format & writes it into the file f
    #       v. print confirmation
    #           - str(task["id"]) :                                             task["id"] is an int & we can't concatenate str & int in python directly

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
    #           - int(sys.argv[2]) :                                            sys.argv[2] is a str, but TASK_ID is an int
    #       ii. define file name & load EXISTING tasks
    #           - else: print("File doesnot exist") :                           file doesnot exist/ no tasks exist
    #       iii. delete task
    #           - tasks = [task for task in tasks if task["id"] != task_id] :   (LIST COMPREHENSION) Rebuilds the list keeping only tasks whose id does not match
    #       iv. write back in file
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
    #       i. EDGE CASE
    # NOTE : loading the file before checking description doesn't break anything, but validating inputs before doing file I/O is better.
    # * IV. DESCRIPTION
    #       i. EDGE CASE: For a DESCRIPTION to exist, you need atleast 4 elements
    #       ii. define file name & load EXISTING tasks
    #       iii. update description and time
    #           - for task in tasks :                                           task is like i iterator in for loop
    #       iv. write back in file
    #       v. print confirmation

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
    #       ii. define file name & load EXISTING tasks
    #       iii. update status and time
    #           - task["status"] = "in-progress" :                              The command is mark-in-progress but the stored status value is just "in-progress"
    #       iv. write back in file
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
    #       ii. define file name & load EXISTING tasks
    #       iii. update status and time
    #           - task["status"] = "done" :                                     The command is mark-done but the stored status value is just "done"
    #       iv. write back in file
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
    #       i. define file name & load EXISTING tasks
    #       ii. Check loaded tasks
    #       iii. filter tasks
    #       iv. print confirmation

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
