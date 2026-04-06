from logging import getLogger, basicConfig, DEBUG
from src.tasks import ApiTaskSource, TextTaskSource, GeneratorTaskSource
from src.contracts.task import Task
logger = getLogger()
format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
basicConfig(filename='shell.log', encoding='utf-8',
            level=DEBUG, format=format, filemode='w')


def display_menu() -> None:
    """Выводит главное меню"""
    print("\n" + "=" * 40)
    print("       TASK SYSTEM INTERACTIVE DEMO")
    print("=" * 40)
    print("1. Generate tasks from API source")
    print("2. Generate tasks from random generator")
    print("3. Generate tasks from text file")
    print("4. View all collected tasks")
    print("5. Exit")
    print("=" * 40)


def display_tasks(tasks: list[Task]) -> None:
    """Выводит список задач"""
    if not tasks:
        print("\nNo tasks collected yet.")
        return
    print(f"\n{'ID':<20} {'Payload':<40} {'Priority':<10} {'Status':<10}")
    print("-" * 80)
    for task in tasks:
        print(f"{task.id:<20} {task.payload:<40} {task.priority:<10} {task.status:<10}")


def main() -> None:
    """Главная функция с интерактивным меню"""
    collected_tasks: list[Task] = []
    sources = {
        'api': ApiTaskSource,
        'generator': GeneratorTaskSource,
        'text': None
    }

    print("Welcome to the Task System Interactive Demo!")
    print("This demo allows you to explore how tasks are created and managed.")

    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            print("\nGenerating tasks from API source...")
            tasks = sources['api']().get_tasks()
            collected_tasks.extend(tasks)
            print(f"Successfully added {len(tasks)} tasks from API source.")
            display_tasks(tasks)

        elif choice == '2':
            print("\nGenerating tasks from random generator...")
            gen = sources['generator']().get_tasks()
            for i, task in enumerate(gen):
                collected_tasks.append(task)
                if i >= 4:
                    break
            print(
                f"Successfully generated {min(5, len(collected_tasks))} random tasks.")
            display_tasks(
                collected_tasks[-5:] if len(collected_tasks) >= 5 else collected_tasks)

        elif choice == '3':
            filename = "tasks_examples/task_example.txt"
            print(f"\nLoading tasks from text file: {filename}")
            try:
                if sources['text'] is None:
                    sources['text'] = TextTaskSource(filename)
                tasks = sources['text'].get_tasks()
                collected_tasks.extend(tasks)
                print(f"Successfully loaded {len(tasks)} tasks from file.")
                display_tasks(tasks)
            except FileNotFoundError:
                print(f"Error: File '{filename}' not found.")
            except Exception as e:
                print(f"Error loading tasks: {e}")

        elif choice == '4':
            display_tasks(collected_tasks)

        elif choice == '5':
            print("\nGoodbye")
            break

        else:
            print("\nInvalid choice. Please enter a number between 1 and 5.")


if __name__ == '__main__':
    main()
