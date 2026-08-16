# 🌱 Python 00 — Growing Code: Основы Python через данные о саде

## Общее описание проекта

Этот проект называется **"Growing Code"** — ты будешь изучать базовый синтаксис Python, работая с данными о коммунальном саде (community garden). Звучит мило, но по сути это набор из **8 упражнений (ex0–ex7)**, которые идут от простого к сложному и покрывают:

- Функции
- Ввод/вывод (`print`, `input`)
- Переменные и типы данных
- Условные операторы (`if/else`)
- Циклы (`for`) и рекурсия
- Аннотации типов (type hints)

---

## 🔑 Ключевые правила (General Instructions)

Прежде чем кодить, запомни эти правила — нарушишь, не пройдёшь проверку:

| Правило | Что это значит |
|---------|---------------|
| **Python 3.10+** | Используй современный Python (скорее всего уже установлен) |
| **flake8** | Линтер — проверяет стиль кода (отступы, длина строк и т.д.) |
| **Каждое упражнение в своём файле** | `ex0/ft_hello_garden.py`, `ex1/ft_garden_name.py` и т.д. |
| **Только функция, никакого `main`** | НЕ пиши `if __name__ == "__main__":`, НЕ вызывай функцию в файле |
| **Имена функций — точно как в задании** | `ft_hello_garden`, не `helloGarden`, не `hello_garden` |
| **Обработка ошибок не нужна** | Если не сказано иначе — не надо обрабатывать невалидный ввод |
| **Type hints** | Необязательны для ex0–ex6, **обязательны для ex7** |

### ⚠️ Самое важное правило

> **В файле должна быть ТОЛЬКО функция.** Никакого кода вне функции. Никаких вызовов. Никакого `main`.

Для тестирования используй предоставленный `main.py` — положи его рядом с файлами упражнений и запускай `python3 main.py`.

---

## 🐍 Python vs C: Быстрый ликбез для сишника

Ты знаешь C? Отлично. Вот главные отличия, которые тебе нужны для этого проекта:

### 1. Нет точек с запятой, нет фигурных скобок

```c
// C
int main() {
    printf("Hello\n");
    return 0;
}
```

```python
# Python
def main():
    print("Hello")
```

**Отступы (indentation) — это и есть "фигурные скобки".** В Python блок кода определяется отступом (4 пробела — стандарт). Если отступ неправильный — код не работает. Это не стиль, это **синтаксис**.

### 2. Нет объявления типов переменных

```c
// C
int x = 5;
char *name = "Garden";
```

```python
# Python
x = 5
name = "Garden"
```

Python — **динамически типизированный**. Тип переменной определяется автоматически по значению. Не надо писать `int`, `char*` и т.д.

### 3. Функции — ключевое слово `def`

```c
// C
void say_hello() {
    printf("Hello\n");
}
```

```python
# Python
def say_hello():
    print("Hello")
```

- Нет `void`, `int` и т.д. перед именем функции
- Двоеточие `:` после сигнатуры
- Тело функции — с отступом

### 4. `print()` вместо `printf()`

```c
// C
printf("Area: %d\n", area);
```

```python
# Python
print("Area:", area)          # автоматический пробел между аргументами
print(f"Area: {area}")        # f-string — аналог printf с форматированием
```

`print()` автоматически добавляет `\n` в конце. Не нужно писать `\n` явно.

### 5. `input()` вместо `scanf()`

```c
// C
char name[100];
printf("Enter name: ");
scanf("%s", name);
```

```python
# Python
name = input("Enter name: ")
```

`input()` всегда возвращает **строку** (`str`). Если нужно число:

```python
x = int(input("Enter number: "))  # преобразуем строку в int
```

### 6. Нет `{` `}` для if/else

```c
// C
if (x > 60) {
    printf("Ready\n");
} else {
    printf("Not ready\n");
}
```

```python
# Python
if x > 60:
    print("Ready")
else:
    print("Not ready")
```

Обрати внимание: **нет скобок вокруг условия**, двоеточие после условия, тело — с отступом.

### 7. Цикл `for` — это `for ... in range()`

```c
// C
for (int i = 1; i <= 5; i++) {
    printf("Day %d\n", i);
}
```

```python
# Python
for i in range(1, 6):       # range(1, 6) = [1, 2, 3, 4, 5]
    print("Day", i)
```

`range(start, stop)` — stop **не включается**! Это как `[start, stop)` в математике.

### 8. Рекурсия — почти как в C

```c
// C
void count(int current, int max) {
    if (current > max) return;
    printf("Day %d\n", current);
    count(current + 1, max);
}
```

```python
# Python
def count(current, max_val):
    if current > max_val:
        return
    print("Day", current)
    count(current + 1, max_val)
```

Почти один в один. Только синтаксис отличается.

---

## 📋 Разбор каждого упражнения

---

### Exercise 0: Hello Garden 🌻

**Файл:** `ex0/ft_hello_garden.py`
**Разрешено:** `print()`
**Цель:** Написать функцию, которая печатает приветствие.

#### Что нужно сделать:

```python
def ft_hello_garden():
    print("Hello, Garden Community!")
```

Вот и всё. Серьёзно. Это **весь файл**. Никакого другого кода.

#### Что тут учим (для сишника):
- `def` — объявление функции (вместо `void func_name()`)
- Нет `return` — если функция ничего не возвращает, `return` можно опустить (в C аналогично для `void`)
- `print()` — вывод на экран с автоматическим `\n`

#### Аналог на C:
```c
void ft_hello_garden(void) {
    printf("Hello, Garden Community!\n");
}
```

---

### Exercise 1: Garden Name 🏷️

**Файл:** `ex1/ft_garden_name.py`
**Разрешено:** `input()`, `print()`
**Цель:** Спросить имя сада и вывести его + фиксированное сообщение.

#### Ожидаемое поведение:
```
Enter garden name: Community Garden
Garden: Community Garden
Status: Growing well!
```

#### Что нужно знать:
- `input("prompt")` — выводит prompt и ждёт ввод пользователя, возвращает строку
- Вторая строка (`Status: Growing well!`) — **фиксированная**, всегда одинаковая

#### Аналог на C:
```c
void ft_garden_name(void) {
    char name[256];
    printf("Enter garden name: ");
    fgets(name, 256, stdin);
    // удалить \n из fgets...
    printf("Garden: %s\n", name);
    printf("Status: Growing well!\n");
}
```

В Python это намного проще — `input()` уже убирает `\n` за тебя.

---

### Exercise 2: Garden Plot Area 📐

**Файл:** `ex2/ft_plot_area.py`
**Разрешено:** `input()`, `int()`, `print()`
**Цель:** Спросить длину и ширину, посчитать площадь.

#### Ожидаемое поведение:
```
Enter length: 5
Enter width: 3
Plot area: 15
```

#### Что нужно знать:
- `input()` возвращает **строку**, даже если пользователь ввёл число
- `int()` — преобразует строку в целое число
- Комбинация: `int(input("Enter length: "))` — читает ввод и сразу конвертирует в `int`

#### Ключевой момент для сишника:

В C ты пишешь `scanf("%d", &x)` и получаешь сразу `int`. В Python нужно **явно преобразовать**:

```python
length = int(input("Enter length: "))   # "5" → 5
width = int(input("Enter width: "))     # "3" → 3
area = length * width                    # 5 * 3 = 15
print("Plot area:", area)
```

---

### Exercise 3: Harvest Total 🥕

**Файл:** `ex3/ft_harvest_total.py`
**Разрешено:** `input()`, `int()`, `print()`
**Цель:** Спросить урожай за 3 дня, посчитать сумму.

#### Ожидаемое поведение:
```
Day 1 harvest: 5
Day 2 harvest: 8
Day 3 harvest: 3
Total harvest: 16
```

#### Что нужно знать:
Это то же самое, что и ex2, но с тремя числами. Три вызова `int(input(...))`, потом сложение.

---

### Exercise 4: Plant Age Check 🌿

**Файл:** `ex4/ft_plant_age.py`
**Разрешено:** `input()`, `int()`, `print()`
**Цель:** Спросить возраст растения в днях. Если **строго больше 60** — "готово к сбору", иначе — "нужно ещё расти".

#### Ожидаемое поведение:
```
Enter plant age in days: 75
Plant is ready to harvest!

Enter plant age in days: 45
Plant needs more time to grow.
```

#### Что нужно знать:
- `if/else` — условный оператор
- **Строго больше 60** — значит `age > 60`, НЕ `age >= 60`. 60 дней = ещё не готово.

#### Ключевой момент:

```python
if age > 60:
    print("Plant is ready to harvest!")
else:
    print("Plant needs more time to grow.")
```

Для сишника: то же самое, только без `()` вокруг условия и без `{}`. Двоеточие + отступ = блок.

---

### Exercise 5: Water Reminder 💧

**Файл:** `ex5/ft_water_reminder.py`
**Разрешено:** `input()`, `int()`, `print()`
**Цель:** Спросить, сколько дней прошло с последнего полива. Если **больше 2** — "полей!", иначе — "всё ок".

#### Ожидаемое поведение:
```
Days since last watering: 4
Water the plants!

Days since last watering: 1
Plants are fine
```

#### Что нужно знать:
Аналогично ex4, только другое условие (`days > 2`) и другие сообщения.

#### ⚠️ Внимание на текст!
- `"Water the plants!"` — с восклицательным знаком
- `"Plants are fine"` — **без** восклицательного знака

Текст должен совпадать **посимвольно**. Один лишний пробел или точка = fail на проверке.

---

### Exercise 6: Count to Harvest 🔢

**Файл:** `ex6/ft_count_harvest_iterative.py` и `ex6/ft_count_harvest_recursive.py`
**Разрешено:** `input()`, `int()`, `print()`, `range()`, вспомогательные функции для рекурсии
**Цель:** Два файла! Считать от 1 до N, потом "Harvest time!". Один файл — цикл, другой — рекурсия.

#### Ожидаемое поведение (одинаковое для обоих):
```
Days until harvest: 5
Day 1
Day 2
Day 3
Day 4
Day 5
Harvest time!
```

#### Итеративная версия (цикл):

```python
def ft_count_harvest_iterative():
    days = int(input("Days until harvest: "))
    for i in range(1, days + 1):    # range(1, 6) = 1,2,3,4,5
        print("Day", i)
    print("Harvest time!")
```

**Для сишника:** `range(1, days + 1)` — это аналог `for (int i = 1; i <= days; i++)`. Помни: верхняя граница `range()` **не включается**.

#### Рекурсивная версия:

Есть несколько вариантов. Вот один с вложенной функцией:

```python
def ft_count_harvest_recursive():
    days = int(input("Days until harvest: "))

    def helper(current):
        if current > days:
            return
        print("Day", current)
        helper(current + 1)

    helper(1)
    print("Harvest time!")
```

**Для сишника:** В Python можно определять функцию **внутри** функции. Это называется замыкание (closure). Внутренняя функция видит переменные внешней (`days`). В C такого нет — пришлось бы передавать `days` как параметр.

Другие допустимые подходы:
- Параметр по умолчанию: `def helper(current=1)`
- Отдельная функция-помощник вне `ft_count_harvest_recursive`

---

### Exercise 7: Seed Inventory with Type Annotations 🏷️📦

**Файл:** `ex7/ft_seed_inventory.py`
**Разрешено:** `print()`, строковые методы
**Цель:** Функция принимает аргументы (не `input()`!) и выводит информацию в зависимости от типа единицы измерения.

#### ⚠️ Здесь Type Hints ОБЯЗАТЕЛЬНЫ!

#### Сигнатура функции (должна быть именно такой):

```python
def ft_seed_inventory(seed_type: str, quantity: int, unit: str) -> None:
```

**Для сишника:** Это как прототип функции в C:
```c
void ft_seed_inventory(char *seed_type, int quantity, char *unit);
```

Только в Python эти аннотации (`str`, `int`, `-> None`) — это **подсказки** для людей и инструментов, Python их **не проверяет** при запуске. Но инструмент **mypy** проверяет — и это требование задания.

#### Ожидаемое поведение:

```
>>> ft_seed_inventory("tomato", 15, "packets")
Tomato seeds: 15 packets available

>>> ft_seed_inventory("carrot", 8, "grams")
Carrot seeds: 8 grams total

>>> ft_seed_inventory("lettuce", 12, "area")
Lettuce seeds: covers 12 square meters
```

#### Что нужно знать:

1. **Заглавная первая буква:** `"tomato"` → `"Tomato"`. Метод `.capitalize()`:
   ```python
   "tomato".capitalize()  # → "Tomato"
   ```

2. **Разные форматы для разных unit:**
   - `"packets"` → `"{Name} seeds: {qty} packets available"`
   - `"grams"` → `"{Name} seeds: {qty} grams total"`
   - `"area"` → `"{Name} seeds: covers {qty} square meters"`
   - Любой другой unit → `"Unknown unit type"`

3. **`if/elif/else`** — аналог `switch/case` или цепочки `if/else if/else` в C:

```python
if unit == "packets":
    print(f"{name} seeds: {quantity} packets available")
elif unit == "grams":
    print(f"{name} seeds: {quantity} grams total")
elif unit == "area":
    print(f"{name} seeds: covers {quantity} square meters")
else:
    print("Unknown unit type")
```

#### Новое для сишника:
- **f-strings:** `f"Hello {name}"` — строка с подстановкой переменных. Буква `f` перед кавычками. Переменные в `{}`. Это удобнее, чем `printf("Hello %s", name)`.
- **Строковые методы:** Строки в Python — это объекты с методами. `"hello".capitalize()` → `"Hello"`. В C ты бы писал свою функцию для этого.
- **`elif`** — это `else if` из C, просто короче записывается.

#### Про mypy:

Mypy — это инструмент статической проверки типов. Запускаешь так:
```bash
mypy ft_seed_inventory.py
```
Если всё ок — ошибок не будет. Если забыл аннотации или типы не совпадают — покажет ошибки.

Установка (если не установлен):
```bash
pip install mypy
```

---

## 🛠️ Инструменты и рабочий процесс

### Как тестировать

1. Положи `main.py` (предоставленный в проекте) в рабочую директорию
2. Запусти:
   ```bash
   python3 main.py
   ```
3. Выбери номер упражнения для тестирования

### flake8 — линтер

flake8 проверяет стиль кода. Основные правила:
- Отступы — 4 пробела (не табы!)
- Строки не длиннее 79 символов
- Пустая строка в конце файла
- Пробелы вокруг операторов (`x = 5`, не `x=5`)

Запуск:
```bash
flake8 ft_hello_garden.py
```

Установка (если не установлен):
```bash
pip install flake8
```

### Структура сдачи

```
Python00/
├── ex0/
│   └── ft_hello_garden.py
├── ex1/
│   └── ft_garden_name.py
├── ex2/
│   └── ft_plot_area.py
├── ex3/
│   └── ft_harvest_total.py
├── ex4/
│   └── ft_plant_age.py
├── ex5/
│   └── ft_water_reminder.py
├── ex6/
│   ├── ft_count_harvest_iterative.py
│   └── ft_count_harvest_recursive.py
└── ex7/
    └── ft_seed_inventory.py
```

---

## 📝 Шпаргалка: Python для сишника

| Концепция | C | Python |
|-----------|---|--------|
| Вывод | `printf("Hi %s\n", name);` | `print(f"Hi {name}")` |
| Ввод | `scanf("%d", &x);` | `x = int(input("prompt"))` |
| Объявление функции | `void foo() { ... }` | `def foo(): ...` |
| Условие | `if (x > 5) { ... }` | `if x > 5: ...` |
| Иначе если | `else if` | `elif` |
| Цикл for | `for(int i=0;i<n;i++)` | `for i in range(n):` |
| Строка | `char str[]` | `str` (неизменяемый объект) |
| Нет типов | `int x = 5;` | `x = 5` |
| Аннотации типов | прототип `int foo(int x);` | `def foo(x: int) -> int:` |
| Сравнение строк | `strcmp(a, b) == 0` | `a == b` |
| Конкатенация | `strcat()` / сложная логика | `"hello" + " world"` |
| Длина строки | `strlen(s)` | `len(s)` |
| Нет return для void | `return;` или ничего | просто не пишешь `return` |

---

## 🎯 Итого: что проект тестирует

| Упражнение | Концепция | Сложность |
|------------|-----------|-----------|
| ex0 | Определение функции, `print()` | ⭐ |
| ex1 | `input()`, переменные | ⭐ |
| ex2 | `int()` преобразование, арифметика | ⭐ |
| ex3 | Несколько переменных, сложение | ⭐ |
| ex4 | `if/else`, сравнение | ⭐⭐ |
| ex5 | `if/else` (закрепление) | ⭐⭐ |
| ex6 | `for` цикл + рекурсия, `range()` | ⭐⭐⭐ |
| ex7 | Аргументы функции, type hints, `elif`, строковые методы, mypy | ⭐⭐⭐⭐ |

---

> **Совет:** На защите (defense) тебя могут попросить объяснить каждую строку кода, пройтись по execution flow или изменить решение на месте. Убедись, что понимаешь каждую строку, которую написал. Не копируй — разбирайся!
