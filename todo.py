import click  # Import the `click` library to create a CLI
import json  # Import `json` to save and load tasks from a file
import os  # Import `os` to check if the file exists

TODO_FILE = "todo.json"  # Define the filename where tasks are stored


# Function to load tasks from the JSON file
def load_tasks():
    if not os.path.exists(TODO_FILE):  # Check if file exists
        return []  # If not, return an empty list
    with open(TODO_FILE, "r") as file:  # Open the file in read mode
        return json.load(file)  # Load and return the JSON data as a Python list

# Function to save tasks to the JSON file
def save_tasks(tasks):
    with open(TODO_FILE, "w") as file:  # Open the file in write mode
        json.dump(tasks, file, indent=4)  # Save tasks as formatted JSON


@click.group()  # Define a Click command group (main CLI)
def cli():
    """Simple To-Do List Manager"""  # Docstring for the CLI
    pass  # No action, acts as a container for commands


@click.command()  # Define a command called 'add'
@click.argument("task")  # Accepts a required argument (task name)
def add(task):
    """Add a new task to the list"""
    tasks = load_tasks()  # Load existing tasks
    tasks.append({"task": task, "done": False})  # Append a new task (default: not done)
    save_tasks(tasks)  # Save the updated tasks
    click.echo(f"Task added: {task}")  # Print a success message


@click.command()  # Define a command called 'list'
def list():
    """List all tasks"""
    tasks = load_tasks()  # Load existing tasks
    if not tasks:  # If there are no tasks
        click.echo("No tasks found!")  # Print message
        return  # Stop execution
    for index, task in enumerate(tasks, 1):  # Loop through tasks with numbering
        status = "✓" if task["done"] else "✗"  # Show '✓' for completed, '✗' for not
        click.echo(f"{index}. {task['task']} [{status}]")  # Print task with status


@click.command()  # Define a command called 'complete'
@click.argument("task_number", type=int)  # Accepts a task number as an integer
def complete(task_number):
    """Mark a task as completed"""
    tasks = load_tasks()  # Load existing tasks
    if 0 < task_number <= len(tasks):  # Ensure task number is valid
        tasks[task_number - 1]["done"] = True  # Mark as done
        save_tasks(tasks)  # Save updated tasks
        click.echo(f"Task {task_number} marked as completed!")  # Print success message
    else:
        click.echo("Invalid task number.")  # Handle invalid numbers


@click.command()  # Define a command called 'remove'
@click.argument("task_number", type=int)  # Accepts a task number as an integer
def remove(task_number):
    """Remove a task from the list"""
    tasks = load_tasks()  # Load existing tasks
    if 0 < task_number <= len(tasks):  # Ensure task number is valid
        removed_task = tasks.pop(task_number - 1)  # Remove the task
        save_tasks(tasks)  # Save updated tasks
        click.echo(f"Removed task: {removed_task['task']}")  # Print removed task
    else:
        click.echo("Invalid task number.")  # Handle invalid numbers

@click.command()
def clear():
    """Clear All Tasks From The List"""
    if click.confirm("Are you sure you want to clear all tasks?"):
        save_tasks([])
        click.echo("All Tasks have been cleared.")
    else:
        click.echo("Operation cancelled.")

# -------------------------------
@click.command()
@click.argument("task_number",type=int)
def reset(task_number):
    """Mark Tasks as not completed""" 
    tasks= load_tasks()
    if 0<task_number<=len(tasks):
        if not tasks[task_number-1]["done"]:
            click.echo("This task is already pending")
        else:
            tasks[task_number-1]["done"] =False
            save_tasks(tasks)
            click.echo(f"Task {task_number} has been reset to pending.")
    else:
        click.echo("Invalid task number.")

@click.command()
@click.argument("task_number", type=int)
@click.argument("new_position", type=int)
def move(task_number, new_position):
    """Move a task to a new position in the list"""
    tasks = load_tasks()
    if 0 < task_number <= len(tasks) and 0 < new_position <= len(tasks):
        task_to_move = tasks.pop(task_number - 1)
        tasks.insert(new_position - 1, task_to_move)
        save_tasks(tasks)
        click.echo(f"Moved task {task_number} to position {new_position}.")
    else:
        click.echo("Invalid task number or new position.")
# Add commands to the main CLI group
cli.add_command(add)
cli.add_command(list)
cli.add_command(complete)
cli.add_command(remove)
cli.add_command(clear)
cli.add_command(reset)
cli.add_command(move)


# If the script is run directly, start the CLI
if __name__ == "__main__":
    cli()