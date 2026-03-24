# Лабораторная работа 2 - дескрипторы данных и не данных

Цель - применить дескрипторы данных и не данных для оптимизации кода - класса задачи Task
## Структура проекта

```
README.md
requirements.txt
паф.md
src/
    __init__.py
    contracts/        # контракты
        task.py        # контракт задачи
        task_source.py # контракт источника задач
    descriptors/      # дескрипторы
        numeric_descriptors.py
        string_descriptors.py
    errors/            # ошибки
        numeric_error.py
        string_error.py
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
- **Логирование** сохраняет сообщения в `shell.log`

## Тестирование

Проект покрыт набором тестов в `tests/test_tasks.py`
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
Тесты проверяют создание задач, сравнения, работу всех источников, валидацию имени файла и обработку ошибок

Выполнил: **Малинин Ярослав М8О-102БВ-25**

Лабораторная работа 2 по программированию на Python
