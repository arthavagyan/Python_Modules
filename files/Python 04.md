#status/in-progress
# 📁 Python 04 — Data Archivist: Файловые операции

> **Полное название:** Data Archivist — Digital Preservation in the Cyber Archives  
> **Версия:** 3.0  
> **Тема:** Работа с файлами (File I/O), потоки ввода-вывода, контекстные менеджеры  
> **Сеттинг:** Год 2087, ты — Архивариус данных в Кибер-Архивах

---

## 📚 Общие Правила

- **Python 3.10+**, **flake8**, **mypy** (type hints обязательны)
- Обработка исключений — программа не должна крашиться
- Разрешённые типы: `str`, `int`, `float`, `list`, `dict`, `set`, `tuple` и их методы

> ⚠️ **ВАЖНО:** Оператор `with` (контекстный менеджер) будет введён **только в ex3**. До этого его использовать **нельзя!**

---

## 📝 Упражнения

---

### Exercise 0: Ancient Text Recovery (Восстановление древнего текста)

| Параметр | Значение |
|---|---|
| **Директория** | `ex0/` |
| **Файл** | `ft_ancient_text.py` |
| **Разрешено** | `import sys`, `sys.argv`, `len()`, `open()`, `import typing`, `typing.IO`, `io.read()`, `io.close()`, `print()` |

#### Что нужно сделать
Скрипт, который:
- Получает **имя файла** через `sys.argv` (аргументы командной строки)
- Открывает файл для **чтения**
- Выводит содержимое
- **Закрывает** файл
- Обрабатывает ошибки (файл не найден, нет аргументов и т.д.)

#### Пример
```bash
$ python3 ft_ancient_text.py ancient_fragment.txt
=== Cyber Archives Recovery & Preservation ===
Accessing file 'ancient_fragment.txt'
---

[FRAGMENT 001] Digital preservation protocols established 2087
[FRAGMENT 002] Knowledge must survive the entropy wars
[FRAGMENT 003] Every byte saved is a victory against oblivion

---
File 'ancient_fragment.txt' closed.
```

#### 💡 Подсказки
1. `sys.argv` — список аргументов. `sys.argv[0]` — имя скрипта, `sys.argv[1]` — первый аргумент
2. Проверь `len(sys.argv)` перед доступом к `sys.argv[1]`
3. `f = open(filename, 'r')` → `content = f.read()` → `f.close()` — **не забудь закрыть!**
4. Оберни `open()` в `try/except` для перехвата `FileNotFoundError`

> ⚠️ **Нюанс:** `f.close()` нужно вызывать **всегда**, даже при ошибке. Пока нет `with`, используй `try/finally`:
> ```python
> f = open(filename)
> try:
>     content = f.read()
> finally:
>     f.close()
> ```

---

### Exercise 1: Archive Creation (Создание архива)

| Параметр | Значение |
|---|---|
| **Директория** | `ex1/` |
| **Файл** | `ft_archive_creation.py` |
| **Разрешено** | `import sys`, `sys.argv`, `len()`, `open()`, `import typing`, `typing.IO`, `io.read()`, `io.write()`, `io.close()`, `print()`, `input()` |

#### Что нужно сделать
Расширить код из ex0:
1. Прочитать файл (как в ex0)
2. **Трансформировать данные:** добавить символ `#` в конец каждой строки (для «совместимости с 2087»)
3. Вывести трансформированные данные
4. **Спросить** у пользователя имя нового файла через `input()`
5. Если имя пустое — не сохранять. Если введено — **записать** данные в новый файл

#### Пример
```bash
$ python3 ft_archive_creation.py ancient_fragment.txt
=== Cyber Archives Recovery & Preservation ===
Accessing file 'ancient_fragment.txt'
---
[FRAGMENT 001] Digital preservation protocols established 2087
---
File 'ancient_fragment.txt' closed.

Transform data:
---
[FRAGMENT 001] Digital preservation protocols established 2087#
[FRAGMENT 002] Knowledge must survive the entropy wars#
---
Enter new file name (or empty): new_fragment.txt
Saving data to 'new_fragment.txt'
Data saved in file 'new_fragment.txt'.
```

#### 💡 Подсказки
1. Разбей содержимое на строки: `lines = content.split('\n')`
2. Добавь `#` к каждой строке: `new_lines = [line + '#' for line in lines]`
3. Для записи: `open(filename, 'w')` — режим записи (создаёт или **перезаписывает** файл)
4. `f.write(content)` — записать строку в файл

> ⚠️ **Нюанс:** Режим `'w'` **полностью перезаписывает** файл. Если хочешь **дописать** — используй `'a'` (append).

---

### Exercise 2: Stream Management (Управление потоками)

| Параметр | Значение |
|---|---|
| **Директория** | `ex2/` |
| **Файл** | `ft_stream_management.py` |
| **Разрешено** | `import sys`, `sys.argv`, `sys.stdin`, `sys.stdout`, `sys.stderr`, `len()`, `open()`, `import typing`, `typing.IO`, `io.read()`, `io.readline()`, `io.write()`, `io.flush()`, `io.close()`, `print()` |

#### Что нужно сделать
Расширить код из ex1:
1. **Ошибки** выводить в `stderr` (стандартный поток ошибок), а не в `stdout`
2. Получать **ввод от пользователя** **без** использования `input()` — через `sys.stdin`

#### Пример
```bash
$ python3 ft_stream_management.py foo
=== Cyber Archives Recovery & Preservation ===
Accessing file 'foo'
[STDERR] Error opening file 'foo': [Errno 2] No such file or directory: 'foo'

$ python3 ft_stream_management.py ancient_fragment.txt
...
Enter new file name (or empty): /etc/passwd
Saving data to '/etc/passwd'
[STDERR] Error opening file '/etc/passwd': [Errno 13] Permission denied: '/etc/passwd'
Data not saved.
```

#### 💡 Подсказки
1. Вывод в stderr: `print("Error", file=sys.stderr)` или `sys.stderr.write("Error\n")`
2. Чтение из stdin без `input()`:
   ```python
   sys.stdout.write("Enter name: ")
   sys.stdout.flush()  # обязательно! иначе текст может не появиться
   user_input = sys.stdin.readline().strip()
   ```
3. `flush()` — принудительно «выталкивает» буфер. Без него текст может задержаться

> ⚠️ **Нюанс:** Три потока Unix — это фундамент:
> - `stdin` (0) — ввод
> - `stdout` (1) — нормальный вывод
> - `stderr` (2) — вывод ошибок
> 
> В Unix можно **перенаправлять** их: `python3 script.py 2>/dev/null` — скроет ошибки, но покажет нормальный вывод. Поэтому ошибки **должны** идти в stderr!

---

### Exercise 3: Vault Security (Безопасность хранилища — `with`)

| Параметр | Значение |
|---|---|
| **Директория** | `ex3/` |
| **Файл** | `ft_vault_security.py` |
| **Разрешено** | `open()`, `read()`, `write()`, `print()` |

#### Что нужно сделать
Использовать оператор **`with`** (контекстный менеджер) для безопасной работы с файлами.

Создать функцию `secure_archive()`:
- Принимает: **имя файла** (обязательно), **действие** (чтение/запись, опционально), **контент** для записи (опционально)
- Возвращает **кортеж** `(bool, str)` — успех/неудача и содержимое/сообщение об ошибке
- Использует `with open(...)` для автоматического закрытия файлов

#### Пример
```python
$ python3 ft_vault_security.py
=== Cyber Archives Security ===

Using 'secure_archive' to read from a nonexistent file:
(False, "[Errno 2] No such file or directory: '/not/existing/file'")

Using 'secure_archive' to read from a regular file:
(True, '[FRAGMENT 001] Digital preservation...\n...')

Using 'secure_archive' to write previous content to a new file:
(True, 'Content successfully written to file')
```

#### 💡 Подсказки
1. **`with`** автоматически закрывает файл, даже при ошибке:
   ```python
   with open(filename, 'r') as f:
       content = f.read()
   # f уже закрыт здесь!
   ```
2. Оберни `with open(...)` в `try/except` для перехвата ошибок:
   ```python
   try:
       with open(filename, 'r') as f:
           content = f.read()
       return (True, content)
   except OSError as e:
       return (False, str(e))
   ```
3. Используй `int` или `str` для параметра действия (чтение/запись) — **на твой выбор**

> ⚠️ **Нюанс:** `with` — это **контекстный менеджер**. Он вызывает `__enter__()` при входе и `__exit__()` при выходе. Для файлов `__exit__()` вызывает `close()`. Это делает `try/finally` ненужным для файлов.

> ⚠️ **Нюанс:** На защите будут **проверять структуру** кода — что ты действительно используешь `with`, а не `try/finally` + `close()`.

---

## 🗺️ Общая Картина Модуля

```
ex0: open() / read() / close() — ручное управление файлами
 │
 ▼
ex1: write() — создание и запись файлов
 │
 ▼
ex2: stdin/stdout/stderr — три потока Unix
 │
 ▼
ex3: with — контекстный менеджер (автоматическое закрытие)
```

Прогрессия: от ручного управления → к автоматическому. Каждое упражнение строится на предыдущем коде.