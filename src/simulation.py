from src.tasks import TaskSource


def process_taks(task_source: TaskSource) -> None:
    """
        функция, которая принимает на вход обьект, который реализует протокол TaskSource и выводит его задачи

    Args:
        task_source (TaskSource): обьект, который реализует протокол TaskSource

    Raises:
        TypeError: ошибка, если task_source не реализует протокол TaskSource
    """
    if not isinstance(task_source, TaskSource):
        raise TypeError("Задача должна быть экземпляром TaskSource")
    tasks = task_source.get_tasks()
    for task in tasks:
        print(task)
