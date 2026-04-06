# Лабораторная работа 3 - пользовательская коллекция задач для ленивой обработки задач

Цель - реализовать пользовательскую очередь TaskQueue для ленивой обработки задач посредством использования генераторов и итераторов.
## Структура проекта

```
README.md
requirements.txt
src/
    __init__.py
    contracts/        # контракты
        task.py        # контракт задачи
        task_source.py # контракт источника задач
    descriptors/      # дескрипторы
        numeric_descriptors.py
        string_descriptors.py
    custom_exceptions/ # пользовательские исключения
        queue_exceptions.py
        string_exceptions.py
        numeric_exceptions.py
        string_error.py
        numeric_error.py
    iterators/         # итераторы
        task_queue.py
    constants.py       # константы для генератора
    main.py            # точка входа для интерактивной оболочки
    simulation.py      # функция обработки задач
    tasks.py           # определение источников задач

tasks_examples/
    task_example.txt   # пример текстового файла с задачами

tests/
    __init__.py
    test_simulation.py # модуль с unit-тестами
    test_tasks.py      # модуль с unit-тестами
    test_task_queue.py # модуль с unit-тестами
```

## Установка и запуск

1. **Установка зависимости**
   ```bash
   pip install -r requirements.txt
   ```

2. **Запустить интерактивную оболочку**
   ```bash
   python -m src.main
   ```

## Функциональность

- **Класс `Task`** — минимальная структура для хранения идентификатора и данных задачи.
- **Источники задач** реализуют протокол `TaskSource`:
  - `TextTaskSource` - чтение из `.txt`
  - `GeneratorTaskSource` - случайная генерация с фиксированным seed
  - `ApiTaskSource` - эмуляция внешнего API
- **`simulation.process_taks`** - демонстрация обработки задач из любого источника
- **Класс `TaskQueue`** — очередь задач с поддержкой фильтрации по приоритету и статусу, итерации и управления задачами.
- **Логирование** сохраняет сообщения в `shell.log`

## Тестирование

Проект покрыт набором тестов в `tests/`
Запуск:
```bash
pytest tests
```
или
```bash
pytest -v
```
или
```bash
pytest -v --cov=src
```
Тесты проверяют создание задач, сравнения, работу всех источников, валидацию имени файла, обработку ошибок и работу очереди задач

Выполнил: **Малинин Ярослав М8О-102БВ-25**

Лабораторная работа 3 по программированию на Python
