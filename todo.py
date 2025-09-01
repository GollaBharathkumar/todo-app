"""
Todo App — CLI with Unit Tests

Features:
- Add task
- List tasks
- Mark task as done
- Delete task

This single file contains both the app and tests.
Run the CLI:
    python todo_app.py
Run the tests:
    python todo_app.py --test
or
    python -m unittest todo_app.py
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
import argparse
import sys
import unittest


# ---------------------------
# Core domain model & logic
# ---------------------------
@dataclass
class Task:
    id: int
    title: str
    done: bool = field(default=False)

    def __repr__(self) -> str:  # clean, readable debug view
        status = "✓" if self.done else "✗"
        return f"Task(id={self.id}, title={self.title!r}, done={status})"


class TodoList:
    """In-memory Todo list using a Python list as the data structure.

    Demonstrates loops, conditionals, and clean code with type hints.
    """

    def __init__(self) -> None:
        self._tasks: List[Task] = []
        self._next_id: int = 1

    # ------------- CRUD ops -------------
    def add_task(self, title: str) -> Task:
        title = title.strip()
        if not title:
            raise ValueError("Task title cannot be empty.")
        task = Task(id=self._next_id, title=title)
        self._tasks.append(task)
        self._next_id += 1
        return task

    def list_tasks(self) -> List[Task]:
        return list(self._tasks)  # return a copy

    def find_by_id(self, task_id: int) -> Optional[Task]:
        for t in self._tasks:  # loop
            if t.id == task_id:  # conditional
                return t
        return None

    def mark_done(self, task_id: int) -> bool:
        task = self.find_by_id(task_id)
        if task and not task.done:
            task.done = True
            return True
        return False

    def delete_task(self, task_id: int) -> bool:
        for idx, t in enumerate(self._tasks):  # loop with index
            if t.id == task_id:
                del self._tasks[idx]
                return True
        return False


# ---------------------------
# CLI presentation layer
# ---------------------------
MENU = (
    "\nTodo App — Choose an option:\n"
    "1) Add task\n"
    "2) List tasks\n"
    "3) Mark task as done\n"
    "4) Delete task\n"
    "5) Exit\n"
)


def print_tasks(tasks: List[Task]) -> None:
    if not tasks:
        print("No tasks yet. Use option 1 to add your first task.")
        return
    # simple table without external libs
    print("\nID  | Status | Title")
    print("----+--------+--------------------------------")
    for t in tasks:
        status = "DONE" if t.done else "TODO"
        print(f"{t.id:<3} | {status:<6} | {t.title}")


def read_int(prompt: str) -> Optional[int]:
    raw = input(prompt).strip()
    if not raw:
        return None
    if not raw.isdigit():
        print("Please enter a valid number.")
        return None
    return int(raw)


def run_cli() -> None:
    todo = TodoList()
    while True:  # loop
        print(MENU)
        choice = input("Enter 1-5: ").strip()

        if choice == "1":  # Add
            title = input("Task title: ").strip()
            try:
                task = todo.add_task(title)
                print(f"Added: {task}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "2":  # List
            print_tasks(todo.list_tasks())

        elif choice == "3":  # Mark done
            task_id = read_int("Task ID to mark as done: ")
            if task_id is None:
                continue
            if todo.mark_done(task_id):
                print("Marked as done.")
            else:
                print("Task not found or already done.")

        elif choice == "4":  # Delete
            task_id = read_int("Task ID to delete: ")
            if task_id is None:
                continue
            if todo.delete_task(task_id):
                print("Deleted.")
            else:
                print("Task not found.")

        elif choice == "5":  # Exit
            print("Goodbye!")
            break
        else:  # conditional
            print("Invalid option. Please enter a number between 1 and 5.")


# ---------------------------
# Unit tests (unittest)
# ---------------------------
class TestTodoList(unittest.TestCase):
    def setUp(self) -> None:
        self.todo = TodoList()

    def test_add_and_list(self):
        self.assertEqual(self.todo.list_tasks(), [])
        t1 = self.todo.add_task("Read a book")
        t2 = self.todo.add_task("Write code")
        self.assertEqual(len(self.todo.list_tasks()), 2)
        self.assertEqual(t1.id, 1)
        self.assertEqual(t2.id, 2)
        self.assertFalse(t1.done)

    def test_add_empty_title_raises(self):
        with self.assertRaises(ValueError):
            self.todo.add_task("   ")

    def test_mark_done(self):
        t = self.todo.add_task("Test task")
        self.assertTrue(self.todo.mark_done(t.id))
        self.assertTrue(self.todo.find_by_id(t.id).done)
        # marking again should return False
        self.assertFalse(self.todo.mark_done(t.id))

    def test_delete_task(self):
        t1 = self.todo.add_task("A")
        t2 = self.todo.add_task("B")
        self.assertTrue(self.todo.delete_task(t1.id))
        self.assertIsNone(self.todo.find_by_id(t1.id))
        self.assertEqual(len(self.todo.list_tasks()), 1)
        # deleting non-existent returns False
        self.assertFalse(self.todo.delete_task(999))


# ---------------------------
# Entrypoint
# ---------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple CLI Todo App")
    parser.add_argument("--test", action="store_true", help="Run unit tests and exit")
    args = parser.parse_args()

    if args.test:
        # Run the tests
        unittest.main(argv=[sys.argv[0]])
    else:
        # Run the CLI
        try:
            run_cli()
        except KeyboardInterrupt:
            print("\nGoodbye!")
