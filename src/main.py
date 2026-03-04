from logging import getLogger, basicConfig, DEBUG
from src.tasks import Task, ApiTaskSource, TextTaskSource, GeneratorTaskSource
logger = getLogger()
format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
basicConfig(filename='shell.log', encoding='utf-8',
            level=DEBUG, format=format, filemode='w')


def main() -> None:
    current_task: Task | None = None
    tasks_list: list[Task] = []
    command: int = 0

    while command != 7:
        print("\nВыберите действие:\n1 Создать задачу\n2 Добавить только что созданную задачу в список задачу")
        print("3 Вывести список задач")
        print("4 Получить задачи через API")
        print("5 Получить задачи из файла (tasks_examples/task_example.txt)")
        print("6 Сгенерировать случайные задачи")
        print("7 Выйти")
        try:
            command = int(input("Введите номер действия: "))

            if command == 1:
                task_id = int(input("Введите ID задачи: "))
                payload = input("Введите содержание задачи: ")
                current_task = Task(task_id, payload)
                print(f"Создана задача: {current_task}")

            elif command == 2:
                if current_task is None:
                    print("Ошибка: сначала создайте задачу (опция 1)")
                else:
                    tasks_list.append(current_task)
                    print("Задача добавлена в список")

            elif command == 3:
                if not tasks_list:
                    print("Список задач пуст")
                else:
                    print(f"\nВсего задач: {len(tasks_list)}")
                    for i, task in enumerate(tasks_list, 1):
                        print(f"  {i}. {task}")

            elif command == 4:
                api_source = ApiTaskSource()
                new_tasks = api_source.get_tasks()
                tasks_list.extend(new_tasks)
                print(f"Получено {len(new_tasks)} задач с API")

            elif command == 5:
                try:
                    text_source = TextTaskSource(
                        "tasks_examples/task_example.txt")
                    new_tasks = text_source.get_tasks()
                    tasks_list.extend(new_tasks)
                    print(f"Получено {len(new_tasks)} задач из файла")
                except FileNotFoundError as e:
                    print(f"Ошибка: {e}")

            elif command == 6:
                gen_source = GeneratorTaskSource()
                new_tasks = gen_source.get_tasks()
                tasks_list.extend(new_tasks)
                print(f"Сгенерировано {len(new_tasks)} случайных задач")

            elif command == 7:
                print("Выход...")
                break

            else:
                print("Ошибка, выберите число от 1 до 7")

        except ValueError:
            logger.error("Введено некорректное значение")
            print("Ошибка: введите корректное число")
        except Exception as e:
            logger.error(f"Ошибка при выполнении команды: {e}")
            print(f"Ошибка: {e}")


if __name__ == '__main__':
    main()
