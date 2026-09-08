# Онлайн-запис — налаштування (Google Calendar + Cloudflare Worker)

Разова настройка. Далі сайт сам показує вільні слоти й створює події в календарі Ганни.

## 1. Google Cloud — service account
1. Відкрити https://console.cloud.google.com → створити проєкт (напр. `little-paw`).
2. **APIs & Services → Library** → знайти **Google Calendar API** → **Enable**.
3. **APIs & Services → Credentials → Create credentials → Service account**.
   - Ім'я будь-яке (напр. `booking`). Роль не обов'язкова. Create.
4. Відкрити створений service account → вкладка **Keys → Add key → Create new key → JSON**.
   - Завантажиться `.json` файл. У ньому знадобляться `client_email` і `private_key`.

## 2. Поділитися календарем із service account
1. Google Calendar (https://calendar.google.com) → створити окремий календар (напр. «Little Paw записи») або взяти робочий.
2. **Settings → «Share with specific people» → Add people** → вставити `client_email` із JSON.
   - Права: **«Make changes to events»**. Save.
3. Там же **Integrate calendar → Calendar ID** — скопіювати (виглядає як `...@group.calendar.google.com`; для основного — це ваш email).

## 3. Telegram-бот (сповіщення про записи)
1. У Telegram написати **@BotFather** → `/newbot` → отримати **token**.
2. Написати щось своєму боту, потім відкрити
   `https://api.telegram.org/bot<TOKEN>/getUpdates` → знайти `chat.id` — це **TELEGRAM_CHAT_ID**.

## 4. Деплой Worker (Cloudflare)
> Потрібен встановлений Node.js. У папці `worker/`:
```bash
npm i -g wrangler
wrangler login
wrangler secret put SA_EMAIL          # client_email з JSON
wrangler secret put SA_PRIVATE_KEY    # private_key з JSON (весь блок BEGIN...END)
wrangler secret put CALENDAR_ID       # Calendar ID з кроку 2
wrangler secret put TELEGRAM_BOT_TOKEN
wrangler secret put TELEGRAM_CHAT_ID
wrangler deploy
```
Після `deploy` буде URL воркера, напр. `https://littlepaw-booking.<акаунт>.workers.dev`.

## 5. Підключити сайт
У `scripts/main.js`, в об'єкті `CONFIG`, вписати цей URL у поле `bookingEndpoint`. Закомітити й запушити.

Готово: сайт показує вільний час, створює події в календарі, шле сповіщення в Telegram.
Ручні блокування часу в Google Calendar автоматично прибирають слоти на сайті.
