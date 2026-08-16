#status/in-progress
# 🃏 Python 07 — DataDeck: Абстрактные паттерны проектирования

> **Полное название:** DataDeck — Abstract Card Architecture  
> **Версия:** 3.0  
> **Тема:** Паттерны: Abstract Factory, Capabilities (множественное наследование), Strategy  
> **Сеттинг:** Карточная игра с существами (à la Pokémon)

---

## 📚 Общие Правила

- **Python 3.10+**, **flake8**, **mypy**
- Разрешено: `abc`, `typing`, все стандартные типы и встроенные функции
- **Запрещено:** `eval()`, `exec()`, внешние библиотеки
- Обработка исключений обязательна

> ⚠️ **PREREQUISITE:** Нужно владеть наследованием, абстрактными классами, полиморфизмом и импортами. Рекомендуется завершить предыдущие модули.

> ⚠️ **`__init__.py` обязателен** для каждой папки-упражнения. Весь тестовый код — в корне Git-репозитория.

---

## 📝 Упражнения

---

### Exercise 0: Creature Factory (Фабрика существ)

| Параметр | Значение |
|---|---|
| **Директория** | `ex0/` (как пакет) |
| **Файлы** | `battle.py` (в корне), `ex0/` — пакет со всеми нужными файлами |
| **Разрешено** | builtins, `import typing`, `import abc` |

#### Что нужно сделать

1. **Абстрактный класс `Creature`** (ABC):
   - Атрибуты: `name`, `creature_type` (строки)
   - Абстрактный метод `attack()` → возвращает строку описания атаки
   - Метод `describe()` → `"Name is a Type type Creature"`

2. **Два семейства существ** (конкретные классы):
   - Семейство Огня: `Flameling` (base), `Infernox` (evolved) — тип "Fire"
   - Семейство Воды: `Aquabub` (base), `Tidalon` (evolved) — тип "Water"

3. **Абстрактная фабрика `CreatureFactory`** (ABC):
   - `create_base()` → базовое существо
   - `create_evolved()` → эволюционированное существо

4. **Конкретные фабрики:**
   - `FireCreatureFactory` → создаёт `Flameling` / `Infernox`
   - `WaterCreatureFactory` → создаёт `Aquabub` / `Tidalon`

5. Пакет `ex0` **не должен** экспортировать конкретные Creature напрямую — **только фабрики**

6. Скрипт `battle.py` — создаёт существ через фабрики и демонстрирует бой

#### Пример
```
Flameling is a Fire type Creature
Flameling uses Ember!
Infernox is a Fire type Creature
Infernox uses Inferno Blast!
...
```

#### 💡 Подсказки
1. **Abstract Factory** — паттерн, который создаёт **семейства** связанных объектов без указания конкретных классов
2. В `__init__.py` пакета `ex0` экспортируй **только фабрики**:
   ```python
   from .factories import FireCreatureFactory, WaterCreatureFactory
   ```
3. Клиентский код (battle.py) **не знает** о конкретных существах — работает только через фабрики
4. Это обеспечивает **слабую связанность** (loose coupling)

> ⚠️ **Нюанс:** Почему фабрики? Потому что клиенту не нужно знать имена конкретных классов. Если завтра `Flameling` переименуют в `FireStarter` — клиентский код **не сломается**, потому что он вызывает `factory.create_base()`.

---

### Exercise 1: Capabilities (Способности — множественное наследование)

| Параметр | Значение |
|---|---|
| **Директория** | `ex1/` (как пакет) |
| **Файлы** | `capacitor.py` (в корне), `ex1/` — пакет |
| **Разрешено** | builtins, `import typing`, `import abc` |

#### Что нужно сделать

1. **Абстрактные классы способностей** (НЕ наследуются от Creature!):
   - `HealCapability` — абстрактный метод `heal()`
   - `TransformCapability` — абстрактные методы `transform()` и `revert()`. Состояние трансформации **персистентно** и влияет на `attack()`

2. **Конкретные классы** (множественное наследование от Creature + Capability):
   - Лечебное семейство: `Sproutling` и `Bloomelle` (Creature + HealCapability)
     → `HealingCreatureFactory`
   - Трансформирующее семейство: `Shiftling` и `Morphagon` (Creature + TransformCapability)
     → `TransformCreatureFactory`

3. Пакет `ex1` экспортирует **только фабрики**

4. Скрипт `capacitor.py` — демонстрирует:
   - Лечебные: describe → attack → heal
   - Трансформирующие: describe → attack → transform → attack (усиленная!) → revert

#### Пример
```
Sproutling is a Grass type Creature
Sproutling uses Vine Whip!
Sproutling heals itself for a small amount

Shiftling is a Normal type Creature
Shiftling attacks normally.
Shiftling shifts into a sharper form!
Shiftling performs a boosted strike!
Shiftling returns to normal.
```

#### 💡 Подсказки
1. **Множественное наследование:** `class Sproutling(Creature, HealCapability):`
2. Способности **отделены** от Creature — это паттерн **Mixin** / **Capability**
3. Для `TransformCapability` — используй атрибут `_is_transformed` (булевый), который меняет поведение `attack()`
4. `super().__init__()` — для вызова `__init__` родительского класса (Creature)

> ⚠️ **Нюанс:** Способности НЕ наследуются от Creature! Это **отдельная иерархия**. Потом они **комбинируются** через множественное наследование. Это позволяет добавлять способности к **любому** типу существ.

---

### Exercise 2: Abstract Strategy (Стратегия боя — паттерн Strategy)

| Параметр | Значение |
|---|---|
| **Директория** | `ex2/` (как пакет) |
| **Файлы** | `tournament.py` (в корне), `ex2/` — пакет |
| **Разрешено** | builtins, `import typing`, `import abc` |

#### Что нужно сделать

1. **Абстрактный класс `BattleStrategy`**:
   - `is_valid(creature)` → `bool` — подходит ли существо для стратегии
   - `act(creature)` — выполнить боевое действие

2. **Три стратегии:**
   - `NormalStrategy` — подходит **любому** Creature, просто `attack()`
   - `AggressiveStrategy` — только для Creature с TransformCapability: `transform() → attack() → revert()`
   - `DefensiveStrategy` — только для Creature с HealCapability: `attack() → heal()`

3. Если стратегия **не подходит** — `is_valid()` → `False`. Если вызвать `act()` с неподходящим — **исключение**

4. **Турнир** (`tournament.py`):
   - Принимает список оппонентов: `list[tuple[CreatureFactory, BattleStrategy]]`
   - Каждый оппонент сражается с **каждым** другим
   - Бой: каждый боец использует свою стратегию
   - Некорректные комбинации обрабатываются (прерывают турнир)

#### Пример
```
Tournament 0 (basic)
*** Tournament ***
2 opponents involved
* Battle *
Flameling is a Fire type Creature
  vs.
Sproutling is a Grass type Creature
  now fight!
Flameling uses Ember!
Sproutling uses Vine Whip!
Sproutling heals itself for a small amount

Tournament 1 (error)
Battle error, aborting tournament: Invalid Creature 'Flameling' for this aggressive strategy
```

#### 💡 Подсказки
1. **Strategy Pattern** — паттерн, где алгоритм (поведение) **вынесен** в отдельный объект и может **меняться** на лету
2. `is_valid()` проверяет `isinstance(creature, TransformCapability)` или `isinstance(creature, HealCapability)`
3. Для турнира — двойной цикл:
   ```python
   for i in range(len(opponents)):
       for j in range(i+1, len(opponents)):
           # бой opponents[i] vs opponents[j]
   ```
4. При невалидной комбинации — бросай исключение и **прерывай** турнир

> ⚠️ **Нюанс из PDF:** Зачем Strategy? Без него пришлось бы в турнире проверять тип каждого существа и вызывать разные методы. С Strategy — один вызов `strategy.act(creature)`, и стратегия сама знает, что делать. Код турнира **не зависит** от конкретных способностей.

---

## 🗺️ Общая Картина Модуля

```
ex0: Abstract Factory — создание семейств объектов
 │
 ▼
ex1: Capabilities (Mixins) — множественное наследование
 │
 ▼
ex2: Strategy Pattern — взаимозаменяемые алгоритмы
```

Три **паттерна GoF** (Gang of Four) — фундамент архитектуры ПО.