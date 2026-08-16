#status/in-progress
# 🌌 Python 09 — Cosmic Data: Pydantic модели и валидация

> **Полное название:** Cosmic Data — Discover Pydantic Models & Validation  
> **Версия:** 3.0  
> **Тема:** Pydantic 2.x — валидация данных, кастомные валидаторы, вложенные модели  
> **Сеттинг:** Космическая обсерватория — валидация данных с космических станций

---

## 📚 Общие Правила

- **Python 3.10+**, **flake8**, **mypy**
- Использовать **Pydantic 2.x** (установить через `pip`)
- **Virtual environment** обязателен
- Каждое упражнение в своей директории: `ex0/`, `ex1/`, `ex2/`
- Упражнения строятся друг на друге — выполнять **по порядку**

---

## 🧠 Чему Учит Этот Модуль

**Pydantic** — самая популярная библиотека Python для валидации данных. Используется в FastAPI, LangChain и тысячах других проектов. Ты научишься:
1. Создавать **модели данных** с автоматической валидацией
2. Писать **кастомные валидаторы** для бизнес-логики
3. Работать с **вложенными моделями** и сложными структурами

---

## 📝 Упражнения

---

### Exercise 0: Space Station Data (Данные космической станции)

| Параметр | Значение |
|---|---|
| **Директория** | `ex0/` |
| **Файл** | `space_station.py` |

#### Что нужно сделать
Создать Pydantic-модель **`SpaceStation`** с полями:

| Поле | Тип | Ограничения |
|---|---|---|
| `station_id` | `str` | 3-10 символов |
| `name` | `str` | 1-50 символов |
| `crew_size` | `int` | 1-20 человек |
| `power_level` | `float` | 0.0-100.0% |
| `oxygen_level` | `float` | 0.0-100.0% |
| `last_maintenance` | `datetime` | Дата/время |
| `is_operational` | `bool` | По умолчанию `True` |
| `notes` | `Optional[str]` | Макс. 200 символов |

Создать `main()`:
- Создаёт **валидный** экземпляр станции
- Выводит информацию
- Пытается создать **невалидный** (например, `crew_size > 20`)
- Показывает **сообщение об ошибке валидации**

#### Пример вывода
```
Space Station Data Validation
========================================
Valid station created:
ID: ISS001
Name: International Space Station
Crew: 6 people
Power: 85.5%
Oxygen: 92.3%
Status: Operational

========================================
Expected validation error:
Input should be less than or equal to 20
```

#### 💡 Подсказки
1. Базовая модель Pydantic:
   ```python
   from pydantic import BaseModel, Field
   from datetime import datetime
   from typing import Optional
   
   class SpaceStation(BaseModel):
       station_id: str = Field(min_length=3, max_length=10)
       crew_size: int = Field(ge=1, le=20)
       is_operational: bool = True
       notes: Optional[str] = Field(default=None, max_length=200)
   ```
2. `Field(ge=1, le=20)` — greater or equal, less or equal
3. Pydantic **автоматически** конвертирует типы: строка `"2024-01-15"` → `datetime`
4. При невалидных данных бросается `ValidationError` — лови через `try/except`

> ⚠️ **Нюанс:** Pydantic **автоматически** приводит типы. Если передать `"42"` в поле `int`, оно будет конвертировано в `42`. Это удобно, но нужно понимать, когда это происходит.

---

### Exercise 1: Alien Contact Logs (Логи контактов с инопланетянами)

| Параметр | Значение |
|---|---|
| **Директория** | `ex1/` |
| **Файл** | `alien_contact.py` |

#### Что нужно сделать
Создать модель **`AlienContact`** с **кастомной валидацией** через `@model_validator`.

**Enum:**
```python
class ContactType(str, Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"
```

**Поля модели:**
| Поле | Тип | Ограничения |
|---|---|---|
| `contact_id` | `str` | 5-15 символов |
| `timestamp` | `datetime` | |
| `location` | `str` | 3-100 символов |
| `contact_type` | `ContactType` | Enum |
| `signal_strength` | `float` | 0.0-10.0 |
| `duration_minutes` | `int` | 1-1440 (макс. 24 часа) |
| `witness_count` | `int` | 1-100 |
| `message_received` | `Optional[str]` | Макс. 500 символов |
| `is_verified` | `bool` | По умолчанию `False` |

**Бизнес-правила** (через `@model_validator(mode='after')`):
1. `contact_id` должен начинаться с **"AC"**
2. **Физический** контакт (`physical`) должен быть **верифицирован** (`is_verified=True`)
3. **Телепатический** контакт требует **≥ 3 свидетелей**
4. Сильный сигнал (**> 7.0**) должен содержать **сообщение** (`message_received`)

#### Пример вывода
```
Alien Contact Log Validation
======================================
Valid contact report:
ID: AC_2024_001
Type: radio
Location: Area 51, Nevada
Signal: 8.5/10

======================================
Expected validation error:
Telepathic contact requires at least 3 witnesses
```

#### 💡 Подсказки
1. Кастомный валидатор:
   ```python
   from pydantic import model_validator
   
   class AlienContact(BaseModel):
       # поля...
       
       @model_validator(mode='after')
       def validate_contact(self) -> 'AlienContact':
           if self.contact_type == ContactType.telepathic and self.witness_count < 3:
               raise ValueError("Telepathic contact requires at least 3 witnesses")
           return self  # ← ОБЯЗАТЕЛЬНО вернуть self!
   ```
2. `mode='after'` — валидатор запускается **после** валидации всех полей
3. **Обязательно** возвращай `self` из валидатора!
4. `Enum` из стандартной библиотеки: `from enum import Enum`

> ⚠️ **Нюанс:** `@model_validator(mode='after')` vs `@field_validator` — `model_validator` видит **все** поля модели, поэтому может проверять **связи** между ними. `field_validator` видит только одно поле.

---

### Exercise 2: Space Crew Management (Управление экипажем — вложенные модели)

| Параметр | Значение |
|---|---|
| **Директория** | `ex2/` |
| **Файл** | `space_crew.py` |

#### Что нужно сделать
Создать **вложенные** Pydantic-модели:

**Enum рангов:**
```python
class Rank(str, Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"
```

**Модель `CrewMember`:**
| Поле | Тип | Ограничения |
|---|---|---|
| `member_id` | `str` | 3-10 символов |
| `name` | `str` | 2-50 символов |
| `rank` | `Rank` | Enum |
| `age` | `int` | 18-80 |
| `specialization` | `str` | 3-30 символов |
| `years_experience` | `int` | 0-50 |
| `is_active` | `bool` | По умолчанию `True` |

**Модель `SpaceMission`:**
| Поле | Тип | Ограничения |
|---|---|---|
| `mission_id` | `str` | 5-15 символов |
| `mission_name` | `str` | 3-100 символов |
| `destination` | `str` | 3-50 символов |
| `launch_date` | `datetime` | |
| `duration_days` | `int` | 1-3650 (макс. 10 лет) |
| `crew` | `list[CrewMember]` | 1-12 человек |
| `mission_status` | `str` | По умолчанию `"planned"` |
| `budget_millions` | `float` | 1.0-10000.0 |

**Правила валидации миссии:**
1. `mission_id` должен начинаться с **"M"**
2. Должен быть **хотя бы один** Commander или Captain в экипаже
3. Длинные миссии (**> 365 дней**) требуют **50%** опытного экипажа (5+ лет опыта)
4. Все члены экипажа должны быть **активными** (`is_active=True`)

#### Пример вывода
```
Space Mission Crew Validation
=========================================
Valid mission created:
Mission: Mars Colony Establishment
ID: M2024_MARS
Destination: Mars
Duration: 900 days
Budget: $2500.0M
Crew size: 3
Crew members:
- Sarah Connor (commander) - Mission Command
- John Smith (lieutenant) - Navigation
- Alice Johnson (officer) - Engineering

=========================================
Expected validation error:
Mission must have at least one Commander or Captain
```

#### 💡 Подсказки
1. **Вложенные модели** — просто используй одну модель как тип поля другой:
   ```python
   class SpaceMission(BaseModel):
       crew: list[CrewMember] = Field(min_length=1, max_length=12)
   ```
2. Pydantic **автоматически** валидирует вложенные модели
3. Проверка наличия командира:
   ```python
   has_leader = any(
       m.rank in (Rank.commander, Rank.captain) 
       for m in self.crew
   )
   ```
4. Проверка опытности: `len([m for m in self.crew if m.years_experience >= 5]) / len(self.crew) >= 0.5`

> ⚠️ **Нюанс:** Что происходит, если `CrewMember` невалиден внутри `SpaceMission`? Pydantic покажет **вложенную** ошибку с точным указанием, какой член экипажа и какое поле невалидно. Это очень удобно для отладки.

---

## 🗺️ Общая Картина Модуля

```
ex0: Базовые модели Pydantic (Field, типы, ограничения)
 │
 ▼
ex1: @model_validator — кастомная бизнес-логика валидации
 │
 ▼
ex2: Вложенные модели — сложные структуры данных
```