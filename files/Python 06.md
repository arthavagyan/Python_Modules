#status/in-progress
# 📦 Python 06 — The Codex: Импорты и модули Python

> **Полное название:** The Codex — Mastering Python's Import Mysteries  
> **Версия:** 2.0  
> **Тема:** Пакеты Python, `__init__.py`, абсолютные/относительные импорты, циклические зависимости  
> **Сеттинг:** Алхимическая лаборатория — модули = зелья, пакеты = гримуары

---

## 📚 Общие Правила

- **Python 3.10+**, **flake8**, **mypy**
- Только импорты файлов/модулей, которые ты **сам создаёшь**
- **Запрещено:** `eval()`, `exec()`, модификация `sys.path`
- Все стандартные типы и встроенные функции разрешены

---

## 🧠 Чему Учит Этот Модуль

Четыре «священные тайны» системы импортов Python:
1. **`__init__.py`** — как папка становится пакетом
2. **Импорт между модулями** — вызов кода из одного модуля в другом
3. **Абсолютные vs относительные импорты**
4. **Циклические зависимости** — как их распознать и сломать

---

## 📁 Финальная Структура Проекта

```
.
├── alchemy/
│   ├── __init__.py
│   ├── elements.py
│   ├── potions.py
│   ├── grimoire/
│   │   ├── __init__.py
│   │   ├── light_spellbook.py
│   │   ├── light_validator.py
│   │   ├── dark_spellbook.py
│   │   └── dark_validator.py
│   └── transmutation/
│       ├── __init__.py
│       └── recipes.py
├── elements.py              ← в корне (не путать с alchemy/elements.py!)
├── ft_distillation_0.py
├── ft_distillation_1.py
├── ft_transmutation_0.py
├── ft_transmutation_1.py
├── ft_transmutation_2.py
├── ft_kaboom_0.py
└── ft_kaboom_1.py
```

---

## 📝 Упражнения (4 части одного задания)

---

### Part I: The Alembic (Алембик — основы пакетов)

#### Что нужно сделать

1. Создать **корневой файл** `elements.py` с четырьмя функциями-«элементами»:
   - `fire()` → `"Fire element created"`
   - `water()` → `"Water element created"`
   - `earth()` → `"Earth element created"`
   - `air()` → `"Air element created"`

2. Создать **пакет** `alchemy/`:
   - `alchemy/__init__.py` — делает папку пакетом
   - `alchemy/elements.py` — **импортирует** функции из корневого `elements.py`
   - `alchemy/potions.py` — содержит функции зелий:
     - `strength_potion()` — использует `fire()` и `water()` → возвращает строку
     - `healing_potion()` — использует `earth()` и `air()` → возвращает строку

3. `alchemy/__init__.py` должен предоставлять доступ к четырём элементам

#### 💡 Подсказки
1. `__init__.py` — это «точка входа» пакета. Когда пишешь `import alchemy`, Python выполняет `alchemy/__init__.py`
2. В `__init__.py` можно реэкспортировать:
   ```python
   from .elements import fire, water, earth, air
   ```
3. В `alchemy/elements.py` нужно импортировать из **корневого** `elements.py` (абсолютный импорт)
4. В `alchemy/potions.py` можно использовать **относительный** импорт: `from .elements import fire, water`

> ⚠️ **Нюанс:** `alchemy/elements.py` и `elements.py` (в корне) — это **разные файлы**! `alchemy/elements.py` служит «прослойкой», которая импортирует из корневого.

> ⚠️ **Нюанс:** Нельзя модифицировать `sys.path`! Нужно использовать правильную структуру импортов.

---

### Part II: Distillation (Дистилляция — разные стили импорта)

#### Что нужно сделать

Создать два тестовых скрипта:

1. **`ft_distillation_0.py`** — использует `from ... import ...`:
   ```python
   from alchemy.potions import strength_potion, healing_potion
   ```

2. **`ft_distillation_1.py`** — использует `import alchemy`:
   ```python
   import alchemy
   alchemy.potions.strength_potion()
   ```
   Также тестирует **алиас** `heal()` — это алиас для `healing_potion()`, который нужно настроить в `__init__.py`

#### Пример вывода
```bash
$ python3 ft_distillation_0.py
=== Distillation 0 ===
Direct access to alchemy/potions.py
Testing strength_potion: Strength potion brewed with 'Fire element created' and 'Water element created'
Testing healing_potion: Healing potion brewed with 'Earth element created' and 'Air element created'

$ python3 ft_distillation_1.py
=== Distillation 1 ===
Using: 'import alchemy' structure to access potions
Testing strength_potion: Strength potion brewed with 'Fire element created' and 'Water element created'
Testing heal alias: Healing potion brewed with 'Earth element created' and 'Air element created'
```

#### 💡 Подсказки
1. Чтобы `import alchemy` давал доступ к `alchemy.potions`, нужно в `__init__.py`:
   ```python
   from . import potions
   ```
2. Для алиаса `heal` в `__init__.py`:
   ```python
   from .potions import healing_potion as heal
   ```
3. `from X import Y` — прямой доступ к `Y`. `import X` — доступ через `X.Y`

---

### Part III: The Great Transmutation (Абсолютные vs относительные импорты)

#### Что нужно сделать

Добавить подпакет `alchemy/transmutation/`:
- `alchemy/transmutation/__init__.py`
- `alchemy/transmutation/recipes.py` содержит:
  - `lead_to_gold()` — использует **минимум один абсолютный** и **один относительный** импорт
  - Возвращает строку, описывающую рецепт

Создать три скрипта:
1. `ft_transmutation_0.py` — импортирует `alchemy.transmutation.recipes` напрямую
2. `ft_transmutation_1.py` — импортирует модуль `transmutation` (через `alchemy`)
3. `ft_transmutation_2.py` — импортирует только `alchemy`

#### 💡 Подсказки
1. **Абсолютный** импорт: `from alchemy.elements import fire` — полный путь от корня
2. **Относительный** импорт: `from ..elements import air` — относительно текущего файла (`..` = на уровень вверх)
3. В `recipes.py` нужно оба стиля:
   ```python
   from alchemy.potions import strength_potion  # абсолютный
   from ..elements import air                    # относительный
   ```
4. Нужно обновить `__init__.py` файлы, чтобы обеспечить доступ через разные стили

> ⚠️ **Нюанс:** Относительные импорты работают **только внутри пакетов** (не в скриптах верхнего уровня). `.` = текущий пакет, `..` = родительский пакет, `...` = два уровня вверх.

---

### Part IV: Avoid the Explosion (Циклические зависимости)

#### Что нужно сделать

Добавить подпакет `alchemy/grimoire/`:

**Световая магия (работает):**
- `light_spellbook.py`:
  - `light_spell_allowed_ingredients()` → `["earth", "air", "fire", "water"]`
  - `light_spell_record(spell_name, ingredients)` — использует `validate_ingredients` из `light_validator.py`
- `light_validator.py`:
  - `validate_ingredients(ingredients)` — проверяет, есть ли хотя бы один допустимый ингредиент

**Тёмная магия (ломается!):**
- `dark_spellbook.py` и `dark_validator.py` — **копии** светлых, но с **циклическим импортом**:
  - `dark_spellbook` импортирует из `dark_validator`
  - `dark_validator` импортирует из `dark_spellbook`
  - → **ImportError!**

Два скрипта:
1. `ft_kaboom_0.py` — использует **светлую** магию (работает, без циклических зависимостей)
2. `ft_kaboom_1.py` — использует **тёмную** магию (падает с `ImportError`)

#### Пример
```bash
$ python3 ft_kaboom_0.py
=== Kaboom 0 ===
Testing record light spell: Spell recorded: Fantasy (Earth, wind and fire - VALID)

$ python3 ft_kaboom_1.py
=== Kaboom 1 ===
Test import now - THIS WILL RAISE AN UNCAUGHT EXCEPTION
ImportError: cannot import name 'dark_spell_allowed_ingredients' from partially initialized module...
```

#### 💡 Подсказки
1. **Циклический импорт** = модуль A импортирует B, модуль B импортирует A → Python не может инициализировать ни один
2. Для **светлой магии** — избежать цикла можно несколькими способами:
   - **Импорт внутри функции** (lazy import): `def f(): from .validator import validate_ingredients`
   - **Объединение** в один модуль
   - **Передача зависимости через параметр** (dependency injection)
   - **Реструктуризация** — вынести общий код в третий модуль
3. Для **тёмной магии** — специально создать цикл (оба файла импортируют друг друга на верхнем уровне)
4. На защите нужно уметь **объяснить разные подходы** к решению циклических зависимостей!

> ⚠️ **Нюанс:** Циклические зависимости — одна из самых частых проблем в больших проектах. В реальности используют: lazy imports, dependency injection, или restructuring. Знание этих паттернов — признак опытного разработчика.

---

## 🗺️ Общая Картина Модуля

```
Part I:  __init__.py → папка становится пакетом
Part II: from/import → разные стили импорта
Part III: absolute vs relative → навигация внутри пакета
Part IV: circular imports → распознавание и решение
```