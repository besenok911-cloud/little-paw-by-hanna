# Оплата (Monobank Acquiring) — активація

Інфраструктура готова, але **вимкнена**. Щоб увімкнути онлайн-оплату, потрібні два рішення бізнесу + ключ.

## Що потрібно від салону
1. **Еквайринг** — підключений Monobank Acquiring (ФОП + мерчант у Monobank).
2. **Модель оплати** — що саме беремо: депозит (частина) / повна сума / лише готель·pawplay.
3. **Токен мерчанта** (X-Token) з кабінету Monobank.

## Кроки активації
1. Задати токен:
   ```bash
   cd worker
   npx wrangler secret put MONO_TOKEN
   npx wrangler deploy
   ```
2. У `scripts/main.js` → `CONFIG.payment`:
   ```js
   payment: { enabled: true, mode: "deposit", depositAmount: 200 }
   ```
   (`mode`: `deposit` — депозит; `full` — повна сума. `depositAmount` — сума депозиту, грн.)
3. Закомітити й запушити сайт.

## Як це працює
- Клієнт бронює → сайт створює запис (`/book` повертає `bookingId`).
- Для оплати сайт викликає `/pay/create` (сума, `bookingId`) → Worker створює рахунок у Monobank і повертає `pageUrl`.
- Клієнта перекидає на **захищену сторінку оплати Monobank** (картка, Apple Pay, Google Pay — автоматично).
- Monobank шле `/pay/webhook` → Worker перевіряє статус і ставить `paid = 1` у базі CRM.

## Ендпоінти (у `worker/src/index.js`)
- `POST /pay/create` — `{ bookingId, amount, description }` → `{ pageUrl }` (або `{ disabled:true }`, якщо токена нема).
- `POST /pay/webhook` — Monobank повідомляє про оплату; статус перевіряється сервером повторно.

## База
Колонки `paid` та `invoice_id` у таблиці `bookings` (див. `schema.sql`).
