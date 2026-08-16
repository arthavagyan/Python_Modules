#status/in-progress
# 🧪 Python 08 — The Matrix: Виртуальные среды и управление пакетами

> **Полное название:** The Matrix — Welcome to the Real World of Data Engineering  
> **Версия:** 3.0  
> **Тема:** Виртуальные среды (venv), pip, Poetry, переменные окружения (.env)  
> **Сеттинг:** Матрица — ты выбрал красную таблетку и познаёшь реальный мир

---

## 📚 Общие Правила

- **Python 3.10+**, **flake8**, **mypy**
- Все стандартные типы и встроенные функции разрешены
- Тестировать в **разных окружениях** (с/без venv, с/без зависимостей)

---

## 🧠 Чему Учит Этот Модуль

Три фундаментальных навыка для любого Python-разработчика:
1. **Виртуальные среды** — изолированные окружения для проектов
2. **Управление пакетами** — pip vs Poetry
3. **Конфигурация через переменные окружения** — `.env` файлы, безопасность

---

## 📝 Упражнения

---

### Exercise 0: Entering the Matrix (Виртуальные среды)

| Параметр | Значение |
|---|---|
| **Директория** | `ex0/` |
| **Файл** | `construct.py` |
| **Разрешено** | `sys`, `os`, `site` модули, `print()` |

#### Что нужно сделать
Создать скрипт `construct.py`, который:
- Определяет, **запущен ли** он в виртуальной среде
- Выводит информацию о текущем окружении Python:
  - Версия Python
  - Путь к исполняемому файлу
  - Пути поиска модулей (`sys.path`)
  - Пакеты `site-packages`
- Показывает **разницу** между работой внутри и вне venv
- Создаёт виртуальную среду, если она ещё не существует

#### 💡 Подсказки
1. Проверка venv: `sys.prefix != sys.base_prefix` — если True, ты в виртуальной среде
2. `sys.executable` — путь к Python
3. `sys.path` — список путей, где Python ищет модули
4. `site.getsitepackages()` — пути к установленным пакетам
5. Создание venv: `python3 -m venv .venv`
6. Активация: `source .venv/bin/activate` (Linux/Mac) или `.venv\Scripts\activate` (Windows)

> ⚠️ **Нюанс:** venv решает «проблему зависимостей»: проект A требует библиотеку v1.0, проект B — v2.0. Без venv они конфликтуют. С venv у каждого проекта **свои** зависимости.

> ⚠️ **Нюанс:** Внутри venv `pip install` ставит пакеты **только** в эту среду, не загрязняя системный Python.

---

### Exercise 1: Loading Programs (pip vs Poetry)

| Параметр | Значение |
|---|---|
| **Директория** | `ex1/` |
| **Файлы** | `loading.py`, `requirements.txt`, `pyproject.toml` |
| **Разрешено** | `pandas`, `requests`, `matplotlib`, `numpy`, `sys`, `importlib` |

#### Что нужно сделать
Создать программу `loading.py`, которая:
- Использует **pandas** для работы с данными
- Использует **numpy** для генерации «данных Матрицы» (numpy **обязателен** как источник данных — не захардкоженные списки!)
- Использует **matplotlib** для визуализации
- **Корректно обрабатывает** отсутствие зависимостей (показывает инструкции по установке)
- Включает функцию **сравнения версий** установленных пакетов

Создать файлы зависимостей для **обоих** менеджеров:
- `requirements.txt` — для pip
- `pyproject.toml` — для Poetry

#### Пример
```bash
# Без зависимостей:
$ python3 loading.py
# Покажет: какие пакеты отсутствуют + инструкции для pip и Poetry

# После установки:
$ pip install -r requirements.txt
$ python3 loading.py
LOADING STATUS: Loading programs...
Checking dependencies:
[OK] pandas (2.1.0) - Data manipulation ready
[OK] numpy (1.25.0) - Numerical computation ready
[OK] matplotlib (3.7.2) - Visualization ready

Analyzing Matrix data...
Processing 1000 data points...
Analysis complete!
Results saved to: matrix_analysis.png
```

#### 💡 Подсказки
1. Проверка наличия пакета:
   ```python
   try:
       import pandas
       print(f"[OK] pandas ({pandas.__version__})")
   except ImportError:
       print("[MISSING] pandas - pip install pandas")
   ```
2. `requirements.txt` формат: `pandas>=2.0.0`, `numpy>=1.24.0`
3. `pyproject.toml` — для Poetry, содержит `[tool.poetry.dependencies]`
4. Используй `numpy` для генерации данных: `np.random.normal(0, 1, 1000)`

> ⚠️ **Нюанс из PDF:** `requests` появляется в выводе **только если** ты используешь API для получения данных. Это опционально.

> ⚠️ **Нюанс:** flake8 и mypy могут ругаться на импорт-ошибки. Для этого упражнения это **допускается** (PDF это явно говорит).

---

### Exercise 2: Accessing the Mainframe (Переменные окружения)

| Параметр | Значение |
|---|---|
| **Директория** | `ex2/` |
| **Файлы** | `oracle.py`, `.env.example`, `.gitignore` |
| **Разрешено** | `os`, `sys`, `python-dotenv` модули, файловые операции |

#### Что нужно сделать
Создать `oracle.py` — систему конфигурации через переменные окружения:
- Загружает конфигурацию из **переменных окружения**
- Использует **`.env` файл** для девелопмент-настроек (через `python-dotenv`)
- Показывает **разницу** между development и production режимами
- Обрабатывает отсутствие конфигурации

Переменные окружения:
| Переменная | Описание |
|---|---|
| `MATRIX_MODE` | `"development"` или `"production"` |
| `DATABASE_URL` | Строка подключения к БД |
| `API_KEY` | Секретный ключ для API |
| `LOG_LEVEL` | Уровень логирования (DEBUG, INFO, etc.) |
| `ZION_ENDPOINT` | URL для «сети сопротивления» |

Файлы:
- `.env.example` — пример конфигурации (без реальных секретов!)
- `.gitignore` — **обязательно** содержит `.env`

#### Пример
```bash
# С .env файлом:
$ python oracle.py
ORACLE STATUS: Reading the Matrix...
Configuration loaded:
Mode: development
Database: Connected to local instance
API Access: Authenticated
Log Level: DEBUG
Zion Network: Online

# С переменными окружения (перезаписывают .env):
$ MATRIX_MODE=production API_KEY=secret123 python3 oracle.py
Mode: production
...
```

#### 💡 Подсказки
1. Установка: `pip install python-dotenv`
2. Загрузка `.env`:
   ```python
   from dotenv import load_dotenv
   load_dotenv()  # загружает .env в os.environ
   ```
3. Чтение: `os.getenv("MATRIX_MODE", "development")` — второй аргумент = значение по умолчанию
4. **Приоритет:** переменные окружения ОС **перезаписывают** значения из `.env`
5. `.gitignore` должен содержать `.env` — **НИКОГДА не коммить секреты!**
6. `.env.example` — шаблон без реальных значений, который **можно** коммитить

> ⚠️ **КРИТИЧНО:** `.env` файл **никогда** не должен попадать в Git! Там лежат пароли, ключи API, строки подключения к БД. Утечка = серьёзная проблема безопасности.

> ⚠️ **Нюанс:** На защите нужно уметь **объяснить, почему** переменные окружения — это правильный способ хранения конфигурации (12-Factor App методология).

---

## 🗺️ Общая Картина Модуля

```
ex0: Виртуальные среды (изоляция проектов)
 │
 ▼
ex1: pip vs Poetry (управление зависимостями)
 │
 ▼
ex2: .env + переменные окружения (конфигурация и безопасность)
```

Эти три навыка — обязательный минимум для любого Python-проекта в продакшене.