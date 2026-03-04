from src.tasks import Task, TextTaskSource, ApiTaskSource, GeneratorTaskSource
from src.constants import POSSIBBLE_DATA, POSSIBBLE_EVENTS, POSSIBBLE_NAMES, SEED
import random
import pytest


def test_task_creation_1():
    task = Task(1, 1)
    assert task.id == 1
    assert task.payload == 1


def test_task_creation_2():
    task = Task(0, None)
    assert task.id == 0
    assert task.payload is None


def test_task_not_eq_1():
    task1 = Task(1, 'onew')
    task2 = Task(2, 'two')
    assert task1 != task2


def test_task_not_eq_2():
    task1 = Task(1, 'some')
    task2 = Task(1, 'other')
    assert task1 != task2


def test_task_eq():
    task1 = Task(1, 'some')
    task2 = Task(1, 'some')
    assert task1 == task2


def test_task_eq_erorr():
    with pytest.raises(TypeError) as e:
        task1 = Task(1, 2)
        task2 = 2
        if task1 == task2:
            pass
    assert f"Невозможно сравнить {type(Task)} и {type(task2)}" == e.value.args[0]


def test_task_repr():
    task = Task(1, {'some': 'john'})
    assert repr(task) == "Task(1,{'some': 'john'})"


def test_api_task_source_1():
    obj = ApiTaskSource()
    assert obj.get_tasks(
    ) == [Task(1, 'one'), Task(2, 'two'), Task(3, 'three'), Task(4, 'four'), Task(5, 'five'), Task(6, 'six'), Task(7, 'seven')]


def test_api_task_source_2():
    obj = ApiTaskSource()
    assert obj.get_tasks(
    ) != [Task(1, 'one'), Task(2, 'two'), Task(3, 'three'), Task(4, 'four'), Task(5, 'five'), Task(6, 'six')]


def test_generator_task_source():
    rnd = random.Random(SEED)
    assert GeneratorTaskSource().get_tasks() == [Task(rnd.randint(1, 100), {"action": rnd.choice(
        POSSIBBLE_EVENTS), "name": rnd.choice(POSSIBBLE_NAMES), "info": rnd.choice(POSSIBBLE_DATA)}) for _ in range(10)]


def test_generator_task_source_bad_seed():
    seed: int = 1
    rnd = random.Random(seed)
    assert GeneratorTaskSource().get_tasks() != [Task(rnd.randint(1, 100), {"action": rnd.choice(
        POSSIBBLE_EVENTS), "name": rnd.choice(POSSIBBLE_NAMES), "info": rnd.choice(POSSIBBLE_DATA)}) for _ in range(10)]


def test_text_task_source():
    with open("tasks_examples/task_example.txt", 'r', encoding='utf-8') as file:
        info = file.read().split('\n')
        lst = [Task(int(i.split('.')[0]), i.split('.')[1].strip())
               for i in info if i]
    obj = TextTaskSource("tasks_examples/task_example.txt")
    assert obj.get_tasks() == lst


def test_text_task_source_filenotfound_erorr():
    with pytest.raises(FileNotFoundError) as e:
        obj = TextTaskSource('tasks_examples/task_example_meow.txt')
        obj.get_tasks()
    assert "Файл не найден" == e.value.args[0]


def test_text_task_source_type_erorr():
    with pytest.raises(TypeError) as e:
        TextTaskSource(1)  # type: ignore
    assert "Имя файла должно быть str" == e.value.args[0]


def test_text_task_source_value_erorr_1():
    with pytest.raises(ValueError) as e:
        obj = TextTaskSource('')
        obj.get_tasks()
    assert "Имя файла не должно быть пустым" == e.value.args[0]


def test_text_task_source_value_erorr_2():
    with pytest.raises(ValueError) as e:
        obj = TextTaskSource('tasks_examples/task_example.docx')
        obj.get_tasks()
    assert "Расширение файла должно быть текстовым" == e.value.args[0]
