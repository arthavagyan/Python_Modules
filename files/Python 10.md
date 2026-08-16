#status/in-progress
# 🧙 Python 10 — FuncMage: Функциональное программирование

> **Полное название:** FuncMage — Master the Ancient Arts of Functional Programming  
> **Версия:** 3.2  
> **Тема:** Lambda, функции высшего порядка, замыкания, functools, декораторы  
> **Сеттинг:** Год 2142, ты — Маг Функций, восстанавливающий Лямбда-Кодекс

---

## 📚 Общие Правила

- **Python 3.10+**, **flake8**, type hints обязательны
- Разрешённые импорты: `typing`, `collections.abc`, `itertools`, `functools`, `operator` (где указано)
- **Запрещено:** внешние библиотеки, файловый I/O, `eval()`, `exec()`, **глобальные переменные**
- **Запрещено:** сложные алгоритмы — фокус на функциональных паттернах
- Есть helper-файл `data_generator.py` для генерации тестовых данных

---

## 🧠 Чему Учит Этот Модуль

Пять «мистических царств» функционального программирования:
1. **Lambda** — анонимные функции
2. **Higher-order functions** — функции, принимающие/возвращающие функции
3. **Closures** — замыкания и лексические области видимости
4. **functools** — модуль стандартной библиотеки (reduce, partial, lru_cache, singledispatch)
5. **Decorators** — обёртки для функций, `@staticmethod`

> **Ключевая идея:** В Python функции — это **объекты первого класса** (first-class citizens). Их можно передавать как аргументы, возвращать из функций и хранить в переменных.

---

## 📝 Упражнения

---

### Exercise 0: Lambda Sanctum (Лямбда-святилище)

| Параметр | Значение |
|---|---|
| **Директория** | `ex0/` |
| **Файл** | `lambda_spells.py` |
| **Разрешено** | `map`, `filter`, `sorted`, `min`, `max`, `round`, `sum`, `len` |

> ⚠️ **Все трансформации — через lambda!** Запрещено использовать `def` для простых одноразовых операций.

#### Что нужно сделать
Четыре функции, демонстрирующие мастерство лямбд:

**`artifact_sorter(artifacts: list[dict]) -> list[dict]`**
- Сортировка артефактов по `power` (по убыванию) через `sorted()` + lambda
- Артефакт: `{'name': str, 'power': int, 'type': str}`

**`power_filter(mages: list[dict], min_power: int) -> list[dict]`**
- Фильтрация магов по силе через `filter()` + lambda

**`spell_transformer(spells: list[str]) -> list[str]`**
- Преобразование заклинаний через `map()` + lambda (добавить `"* "` и `" *"`)

**`mage_stats(mages: list[dict]) -> dict`**
- Статистика: max/min/avg мощности через lambda с `max()`, `min()`, `sum()`

#### 💡 Подсказки
1. Lambda-синтаксис: `lambda x: x['power']` — анонимная функция
2. Сортировка: `sorted(artifacts, key=lambda a: a['power'], reverse=True)`
3. Фильтрация: `list(filter(lambda m: m['power'] >= min_power, mages))`
4. Маппинг: `list(map(lambda s: f"* {s} *", spells))`
5. Среднее: `round(sum(m['power'] for m in mages) / len(mages), 2)`

> ⚠️ **Нюанс:** `filter()` и `map()` возвращают **итераторы**, не списки. Оберни в `list()` если нужен список.

---

### Exercise 1: Higher Realm (Функции высшего порядка)

| Параметр | Значение |
|---|---|
| **Директория** | `ex1/` |
| **Файл** | `higher_order_spells.py` |
| **Разрешено** | `map`, `filter`, `sorted`, `min`, `max`, `round`, `sum`, `len`, `range` |

#### Что нужно сделать

**`apply_spell(spell: Callable, targets: list) -> list`**
- Принимает **функцию** и список целей, применяет функцию к каждому

**`create_spell_chain(*spells: Callable) -> Callable`**
- Принимает **несколько функций** и возвращает **новую функцию**, которая применяет их **последовательно** (композиция)

**`battle_round(fighters: list[dict], strategy: Callable) -> list[dict]`**
- Принимает список бойцов и **стратегию** (функцию), применяет стратегию к каждому

**`create_power_multiplier(multiplier: int) -> Callable`**
- **Возвращает функцию**, которая умножает силу на `multiplier`

#### 💡 Подсказки
1. **Функция высшего порядка** — функция, которая принимает или возвращает другую функцию
2. Композиция:
   ```python
   def create_spell_chain(*spells):
       def chain(target):
           result = target
           for spell in spells:
               result = spell(result)
           return result
       return chain
   ```
3. Фабрика функций:
   ```python
   def create_power_multiplier(multiplier):
       return lambda power: power * multiplier
   ```

> ⚠️ **Нюанс:** `create_power_multiplier(3)` **не умножает** — она **возвращает функцию**, которая умножает. `triple = create_power_multiplier(3)` → `triple(10)` = `30`.

---

### Exercise 2: Memory Depths (Замыкания — Closures)

| Параметр | Значение |
|---|---|
| **Директория** | `ex2/` |
| **Файл** | `closures_spells.py` |
| **Разрешено** | `print`, `len`, `round`, `sum` |

#### Что нужно сделать

**`create_spell_counter() -> tuple[Callable, Callable, Callable]`**
- Возвращает три функции: `cast` (увеличить счётчик), `get_count` (получить), `reset` (сбросить)
- Все три **разделяют** одну переменную через замыкание

**`create_mage_tracker(mage_name: str) -> Callable`**
- Возвращает функцию, которая **помнит** все заклинания мага (хранит список)
- Каждый вызов добавляет заклинание и возвращает историю

**`create_power_accumulator(initial: int) -> Callable`**
- Возвращает функцию-аккумулятор, которая **накапливает** силу
- `acc = create_power_accumulator(10)` → `acc(5)` = 15 → `acc(3)` = 18

#### 💡 Подсказки
1. **Замыкание** — функция, которая «захватывает» переменные из внешней области видимости:
   ```python
   def create_counter():
       count = 0
       def increment():
           nonlocal count  # ← ключевое слово!
           count += 1
           return count
       return increment
   ```
2. **`nonlocal`** — обязательно при **изменении** захваченной переменной. Без него Python создаст **новую** локальную переменную
3. Для **чтения** захваченной переменной `nonlocal` не нужен
4. Мутабельные типы (list, dict) можно **изменять** без `nonlocal` (потому что сам объект не меняется, меняется его содержимое)

> ⚠️ **Нюанс:** `nonlocal` vs `global`:
> - `nonlocal` — захватывает переменную из **ближайшей** внешней функции
> - `global` — захватывает из **глобальной** области (модуля)
> В функциональном стиле `global` **запрещён** (см. правила).

---

### Exercise 3: Ancient Library (functools)

| Параметр | Значение |
|---|---|
| **Директория** | `ex3/` |
| **Файл** | `functools_artifacts.py` |
| **Разрешено** | `functools` (reduce, partial, lru_cache, singledispatch), `operator` |

#### Что нужно сделать

**`spell_reducer(spells: list[int], operation: str) -> int`**
- Использует `functools.reduce` для свёртки списка сил заклинаний
- Операции: `"add"`, `"multiply"`, `"max"`, `"min"`
- Используй функции из `operator` (add, mul, etc.)
- Пустой список → 0, неизвестная операция → обработка ошибки

**`partial_enchanter(base_enchantment: Callable) -> dict[str, Callable]`**
- Принимает функцию с сигнатурой `(power: int, element: str, target: str) -> str`
- Использует `functools.partial` для создания 3 специализированных версий (power=50 + разные элементы)

**`memoized_fibonacci(n: int) -> int`**
- Фибоначчи с `@functools.lru_cache` для мемоизации
- Проверка кэша: `memoized_fibonacci.cache_info()`

**`spell_dispatcher() -> Callable`**
- Использует `@functools.singledispatch` для обработки разных типов:
  - `int` → урон
  - `str` → зачарование  
  - `list` → мульти-заклинание
  - Остальное → неизвестный тип

#### 💡 Подсказки
1. **reduce:** `functools.reduce(operator.add, [10, 20, 30])` = 60
2. **partial:** `fire_enchant = functools.partial(enchant, power=50, element="fire")`
3. **lru_cache:**
   ```python
   @functools.lru_cache(maxsize=None)
   def fib(n):
       if n <= 1: return n
       return fib(n-1) + fib(n-2)
   ```
4. **singledispatch:**
   ```python
   @functools.singledispatch
   def cast(spell):
       return "Unknown spell type"
   
   @cast.register(int)
   def _(spell):
       return f"{spell} damage"
   ```

> ⚠️ **Нюанс:** `lru_cache` **драматически** ускоряет рекурсивный Фибоначчи: без кэша O(2^n), с кэшем O(n). Разница: `fib(35)` без кэша ~15 сек, с кэшем ~0.001 сек.

---

### Exercise 4: Master's Tower (Декораторы и @staticmethod)

| Параметр | Значение |
|---|---|
| **Директория** | `ex4/` |
| **Файл** | `decorator_mastery.py` |
| **Разрешено** | `functools.wraps`, `staticmethod` |

#### Что нужно сделать

**`spell_timer(func: Callable) -> Callable`** — декоратор-таймер:
- Печатает `"Casting {name}..."` перед вызовом
- Печатает `"Spell completed in X.XXX seconds"` после
- Использует `functools.wraps` для сохранения метаданных
- Возвращает результат оригинальной функции

**`power_validator(min_power: int) -> Callable`** — **параметризованный** декоратор:
- Декоратор-фабрика: `@power_validator(10)` проверяет что power ≥ 10
- Если валидно — выполняет функцию нормально
- Если нет — возвращает `"Insufficient power for this spell"`

**`retry_spell(max_attempts: int) -> Callable`** — декоратор повтора:
- Если функция бросает исключение — повторяет до `max_attempts` раз
- Печатает `"Spell failed, retrying... (attempt n/max)"`
- Если все попытки неудачны: `"Spell casting failed after N attempts"`

**`MageGuild` класс:**
- `@staticmethod validate_mage_name(name: str) -> bool` — имя ≥ 3 символов, только буквы/пробелы
- `cast_spell(self, spell_name, power)` — с `@power_validator(10)`

#### 💡 Подсказки
1. Базовый декоратор:
   ```python
   def spell_timer(func):
       @functools.wraps(func)
       def wrapper(*args, **kwargs):
           start = time.time()
           result = func(*args, **kwargs)
           print(f"Completed in {time.time() - start:.3f}s")
           return result
       return wrapper
   ```
2. **Параметризованный** декоратор — это **три** уровня вложенности:
   ```python
   def power_validator(min_power):        # фабрика
       def decorator(func):                # декоратор
           @functools.wraps(func)
           def wrapper(*args, **kwargs):    # обёртка
               # логика валидации
               return func(*args, **kwargs)
           return wrapper
       return decorator
   ```
3. `functools.wraps` — сохраняет `__name__`, `__doc__` оригинальной функции
4. `@staticmethod` — метод класса, который **не получает** `self` и не привязан к экземпляру

> ⚠️ **Нюанс:** `@power_validator(10)` vs `@power_validator` — скобки **критичны**! Первое — параметризованный декоратор (фабрика), второе — обычный. Путаница — частый баг.

> ⚠️ **Нюанс:** `functools.wraps` — **всегда** используй его в декораторах. Без него `func.__name__` будет `"wrapper"` вместо оригинального имени, что ломает отладку и документацию.

---

## 🗺️ Общая Картина Модуля

```
ex0: Lambda — анонимные функции (map, filter, sorted)
 │
 ▼
ex1: Higher-order functions — функции как аргументы/результаты
 │
 ▼
ex2: Closures — замыкания и nonlocal
 │
 ▼
ex3: functools — reduce, partial, lru_cache, singledispatch
 │
 ▼
ex4: Decorators — обёртки функций, @staticmethod
```

От простого к сложному: lambda → функции высшего порядка → замыкания → стандартная библиотека → декораторы.