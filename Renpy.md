
---

## 📌 Создание персонажа и спрайтов

Для начала определим персонажа и подключим изображения:

```renpy
define e = Character("Чумобой")

image ch happy = "ch_happy.png"
image ch sad = "ch_sad.png"
```

> 📁 Изображения должны находиться в папке `images` проекта.

---

## 🌆 Отображение фона и спрайта

Покажем фон комнаты и персонажа:

```renpy
label start:
    scene bg room with fade
    show ch happy at center
    e "Привет, добро пожаловать!"
    return
```

- `scene` — устанавливает фон  
- `show` — отображает спрайт  
- `with fade` — анимация плавного появления

---

## 📏 Изменение размера спрайта

Уменьшим изображение с помощью `zoom`:

```renpy
show ch happy at center:
    zoom 0.7
```

Создадим трансформацию:

```renpy
transform small:
    zoom 0.5

show ch happy at small
```

---

## 💬 Диалоги

Простой диалог с персонажем:

```renpy
e "Как твои дела?"
"Она смотрит на меня внимательно."
```

---

## ❓ Создание выбора

Игроку можно дать выбор:

```renpy
menu:
    "Что ты ответишь?":
        "Привет!":
            e "Рада тебя видеть!"
        "Уходи.":
            e "Ой..."
```

---

## 🔁 Выбор с переходом на разные сцены

Выбор может не только вызывать реплики, но и переходить на разные `label`:

```renpy
label start:
    e "Куда ты хочешь пойти?"

    menu:
        "Пойти в лес":
            jump forest

        "Остаться дома":
            jump home

label forest:
    scene bg forest with fade
    e "Ты в лесу. Пахнет свежестью и приключениями."
    return

label home:
    scene bg room with fade
    e "Ты решил остаться дома. Иногда покой — лучший выбор."
    return
```

> 🔹 Каждый вариант вызывает `jump` к своей метке (`label`).  
> 🔹 После выполнения сцены используется `return`.

---

## 🚪 Переход между сценами

```renpy
label start:
    e "Начнём!"
    jump forest

label forest:
    scene bg forest
    e "Ты пришёл в лес."
    return
```

Или вызов сцены с возвращением назад:

```renpy
label start:
    call intro
    e "Теперь мы продолжим."

label intro:
    e "Это вводная сцена."
    return
```

---

## 🧪 Полный пример сцены

```renpy
define e = Character("Чумобой")
image ch happy = "ch_happy.png"
image ch sad = "ch_sad.png"

label start:
    scene bg room with fade
    show ch happy at center
    e "Привет!"

    menu:
        "Как ты ответишь?":
            "Привет, Чумобой!":
                e "Я рада!"
            "Ты кто вообще?":
                show ch sad at center
                e "Как грубо..."

    e "Продолжим?"
    jump next_scene

label next_scene:
    scene bg forest with dissolve
    e "Теперь мы в лесу!"
    return
```

---

## 🔧 Дополнительно

- `hide ch` — убрать спрайт с экрана  
- `pause 1.0` — пауза в 1 секунду  
- `with dissolve` — плавная смена фона или спрайта  
- `left`, `right`, `center` — позиционирование персонажей  

---

## 📚 Ресурсы

- 🌐 [Официальный сайт Ren'Py](https://www.renpy.org/)
- 📖 [Документация](https://www.renpy.org/doc/html/)
- 🎨 [Бесплатные ресурсы на itch.io](https://itch.io/)

---

