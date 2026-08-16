#status/in-progress
# 🌿 Python 02 — Garden Guardian: Обработка Ошибок

> **Полное название:** Garden Guardian — Data Engineering for Smart Agriculture  
> **Версия:** 3.0  
> **Тема:** Обработка исключений (Exception Handling) в Python  
> **Предыдущие модули:** Python 00 (основы), Python 01 (ООП)

---

## 📚 Общие Правила

- **Python 3.10+**
- Код должен соответствовать стандартам **flake8**
- Все функции и методы должны иметь **type hints** (проверка через `mypy`)
- Программы **не должны крашиться** — исключения обрабатываются корректно

---

## 🧠 Чему Учит Этот Модуль

Этот модуль учит тебя делать **устойчивый код**, который не падает при ошибках. Основная идея — ты строишь «защитника сада» (Garden Guardian), систему мониторинга сельского хозяйства, которая обрабатывает данные с датчиков. А датчики — они ломаются, отправляют мусор, связь пропадает. Твоя программа должна всё это переживать.

---

## 📝 Упражнения

---

### Exercise 0: Agricultural Data Validation (Валидация данных сельского хозяйства)

| Параметр | Значение |
|---|---|
| **Директория** | `ex0/` |
| **Файл** | `ft_data_validation.py` |
| **Разрешено** | `print()`, `int()`, `float()` |

#### Что нужно сделать
Написать функцию `input_temperature(data)`, которая:
- Принимает **строку** (данные с датчика)
- Конвертирует в число с плавающей запятой
- Проверяет, что температура в диапазоне **0°C — 40°C**
- Если данные невалидны или вне диапазона — **поднимает исключение** (`ValueError`)

Написать функцию `test_sensor()`, которая:
- Тестирует `input_temperature()` с различными данными
- **Ловит исключения** с помощью `try/except`
- Показывает, что программа продолжает работать после ошибки

#### Пример вывода
```
=== Garden Sensor Validation ===

Input data is '25.5'
Valid temperature: 25.5°C

Input data is 'abc'
Caught input_temperature error: invalid literal for int() ...

Input data is '100'
Caught input_temperature error: 100°C is too hot for plants (max 40°C)

All tests completed - program didn't crash!
```

#### 💡 Подсказки
1. Используй `float()` для конвертации строки → число. Если строка не число, `float()` **автоматически** выбросит `ValueError`
2. Для проверки диапазона: `if temp < 0 or temp > 40: raise ValueError(f"...")`
3. В `test_sensor()` оберни каждый вызов в `try/except ValueError as e`
4. Ключевое слово `raise` — это то, как ты **сам бросаешь** исключение

> ⚠️ **Нюанс:** Обрати внимание на разницу: `float()` сам бросает `ValueError` при невалидной строке, а ты **дополнительно** бросаешь `ValueError` при выходе за диапазон. Ловятся они одинаково — через `except ValueError`.

---

### Exercise 1: Agricultural Data Validation Pipeline (Пайплайн валидации)

| Параметр | Значение |
|---|---|
| **Директория** | `ex1/` |
| **Файл** | `ft_data_pipeline.py` |
| **Разрешено** | `print()`, `int()`, `float()`, `range()`, `len()` |

#### Что нужно сделать
Расширить код из ex0 — создать **полный пайплайн валидации** данных с датчиков. Нужно обрабатывать данные от нескольких датчиков (температура, влажность, pH почвы) и собирать результаты.

#### 💡 Подсказки
1. Создай отдельные функции валидации для каждого типа данных
2. Используй **список** для хранения результатов валидации
3. Каждая функция валидации может бросать своё исключение
4. Основная функция пайплайна обрабатывает всё через `try/except`

---

### Exercise 2: Different Types of Problems (Разные типы ошибок)

| Параметр | Значение |
|---|---|
| **Директория** | `ex2/` |
| **Файл** | `ft_different_errors.py` |
| **Разрешено** | `print()`, `open()`, `int()` |

#### Что нужно сделать
Написать функцию `garden_operations(operation_number)`, которая содержит **сломанный код** специально. Для каждого значения `operation_number` (0-3) должна возникать **конкретная** ошибка:

| operation_number | Тип ошибки | Как вызвать |
|---|---|---|
| 0 | `ValueError` | `int("abc")` — плохие данные |
| 1 | `ZeroDivisionError` | Деление на ноль |
| 2 | `FileNotFoundError` | `open('/non/existent/file')` |
| 3 | `TypeError` | Сложение строки и числа (`"abc" + 5`) |
| другие | Нет ошибки | Просто `return` |

Написать `test_error_types()`, которая:
- Вызывает `garden_operations()` для каждого значения 0-4
- Ловит каждую ошибку и объясняет, что произошло
- Показывает, что можно ловить **несколько типов** ошибок одним `try`

#### Пример вывода
```
=== Garden Error Types Demo ===
Testing operation 0...
Caught ValueError: invalid literal for int() with base 10: 'abc'
Testing operation 1...
Caught ZeroDivisionError: division by zero
Testing operation 2...
Caught FileNotFoundError: [Errno 2] No such file or directory: '/non/existent/file'
Testing operation 3...
Caught TypeError: can only concatenate str (not "int") to str
Testing operation 4...
Operation completed successfully

All error types tested successfully!
```

#### 💡 Подсказки
1. Используй `if/elif` внутри `garden_operations()` для разных операций
2. Для ловли нескольких типов в одном `except`: `except (ValueError, TypeError) as e:`
3. Для ловли **конкретного** типа: отдельные блоки `except ValueError`, `except ZeroDivisionError` и т.д.
4. Файл, который не нашли — закрывать **не нужно** (он же не открылся)

> ⚠️ **Нюанс про mypy:** `mypy` будет ругаться на строку, вызывающую `TypeError` (`"abc" + 5`). Это нормально — ты намеренно создаёшь ошибку. Mypy делает свою работу! Нельзя использовать `type()`.

> ⚠️ **Нюанс:** Порядок `except` блоков имеет значение! Более **специфичные** исключения ставь **выше**, а более общие — ниже. Иначе общий `except Exception` перехватит всё.

---

### Exercise 3: Making Your Own Error Types (Свои типы ошибок)

| Параметр | Значение |
|---|---|
| **Директория** | `ex3/` |
| **Файл** | `ft_custom_errors.py` |
| **Разрешено** | `print()` |

#### Что нужно сделать
Создать **собственные классы исключений**:

```
Exception
  └── GardenError          ← базовая ошибка сада
        ├── PlantError     ← проблемы с растениями
        └── WaterError     ← проблемы с поливом
```

Каждый класс:
- Наследуется от `Exception` (или от `GardenError`)
- Имеет **дефолтное сообщение** (например, `"Unknown plant error"`), если не передано другое

Создать функции, которые:
- **Поднимают** кастомные ошибки: `raise PlantError("Помидоры вянут!")`
- **Ловят** конкретные типы ошибок
- Демонстрируют, что ловля `GardenError` перехватывает **все** дочерние ошибки

#### Пример вывода
```
=== Custom Garden Errors Demo ===

Testing PlantError...
Caught PlantError: The tomato plant is wilting!

Testing WaterError...
Caught WaterError: Not enough water in the tank!

Testing catching all garden errors...
Caught GardenError: The tomato plant is wilting!
Caught GardenError: Not enough water in the tank!

All custom error types work correctly!
```

#### 💡 Подсказки
1. Кастомный класс ошибки — это просто класс, наследующийся от `Exception`:
   ```python
   class GardenError(Exception):
       def __init__(self, message="Unknown garden error"):
           super().__init__(message)
   ```
2. `PlantError(GardenError)` и `WaterError(GardenError)` — наследуются от `GardenError`
3. Если ловишь `except GardenError` — он **поймает** и `PlantError`, и `WaterError` (полиморфизм!)
4. Это ключевой принцип: **иерархия исключений** позволяет ловить ошибки на нужном уровне абстракции

> ⚠️ **Нюанс:** Дефолтное сообщение задаётся в `__init__`. Не забудь вызвать `super().__init__(message)` — иначе механизм исключений не получит текст ошибки.

---

### Exercise 4: Finally Block - Always Clean Up (Блок Finally — Всегда Убирай)

| Параметр | Значение |
|---|---|
| **Директория** | `ex4/` |
| **Файл** | `ft_finally_block.py` |
| **Разрешено** | `print()`, `str.capitalize()` |

#### Что нужно сделать
Написать `water_plant(plant_name)`:
- Если имя растения **заглавное** (начинается с большой буквы) — полив успешен
- Если **нет** — бросить `PlantError` (из предыдущего упражнения)

Написать `test_watering_system()`:
- Открывает систему полива (просто print)
- Поливает несколько растений через `water_plant()`
- Использует `try/except/finally`
- При ошибке — **останавливает** тесты и возвращается в main
- В блоке `finally` — **всегда** закрывает систему полива
- Демонстрирует, что `finally` выполняется **ВСЕГДА** (и при ошибке, и без)

#### Пример вывода
```
=== Garden Watering System ===

Testing valid plants...
Opening watering system
Watering Tomato: [OK]
Watering Lettuce: [OK]
Watering Carrots: [OK]
Closing watering system

Testing invalid plants...
Opening watering system
Watering Tomato: [OK]
Caught PlantError: Invalid plant name to water: 'lettuce'
.. ending tests and returning to main
Closing watering system

Cleanup always happens, even with errors!
```

#### 💡 Подсказки
1. Проверка заглавной буквы: `plant_name[0].isupper()` или `plant_name == plant_name.capitalize()`
2. Структура `try/except/finally`:
   ```python
   try:
       # рискованный код
   except PlantError as e:
       print(f"Caught: {e}")
       return  # ← выходим из функции
   finally:
       print("Closing watering system")  # ← ВЫПОЛНИТСЯ ВСЕГДА
   ```
3. **`finally` выполняется даже при `return`!** Это ключевой момент упражнения
4. Это важно для реальных систем: файлы нужно закрывать, соединения с БД разрывать, ресурсы освобождать — **независимо от ошибок**

> ⚠️ **Нюанс:** В реальном коде `finally` используется для закрытия файлов, сетевых соединений, освобождения блокировок. Позже ты узнаешь про `with` (контекстный менеджер), который делает это элегантнее. Но сначала нужно понять `finally` — это фундамент.

> ⚠️ **Нюанс:** Используй `PlantError` из ex3. Импортируй его или скопируй класс.

---

## 🗺️ Общая Картина Модуля

```
ex0: Базовая обработка ошибок (try/except, raise)
 │
 ▼
ex1: Пайплайн валидации данных (несколько датчиков)
 │
 ▼
ex2: Разные типы встроенных исключений Python
 │
 ▼
ex3: Создание своей иерархии исключений (наследование)
 │
 ▼
ex4: finally — гарантированная очистка ресурсов
```

Каждое упражнение строится на предыдущем. В конце ты понимаешь полный цикл обработки ошибок в Python.