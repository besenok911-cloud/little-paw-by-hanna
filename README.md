# Little Paw by Hanna — сайт

Грумінг-салон та зооготель. Статичний сайт (HTML/CSS/JS), без збірки — просто відкривається у браузері.

## Структура
- `index.html` — сторінка
- `styles/main.css` — стилі
- `scripts/main.js` — логіка (галерея, прайс, форма запису, анімації)
- `data/prices.js` — **прайс** (редагується вручну, `window.LP_PRICES`)
- `data/gallery.js`, `data/videos.js` — галерея (генеруються скриптами)
- `assets/` — оптимізовані фото/відео/лого
- `tools/` — скрипти збірки медіа (потребують сирий дамп `littlepaw_by_hanna/`)

## Як редагувати
- **Ціни:** відкрити `data/prices.js`, змінити числа у відповідній таблиці, зберегти.
- **Телефон / месенджери:** `scripts/main.js`, об'єкт `CONFIG` угорі.
- **Галерея / відео:** перезапустити `tools/build_media.py` та `tools/build_videos.py` (потрібен Python + Pillow + imageio-ffmpeg і папка з вихідними медіа).

## Публікація
GitHub Pages — сайт оновлюється після `git push`.
