CREATE TABLE IF NOT EXISTS bookings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TEXT NOT NULL,
  pet       TEXT,
  breed     TEXT,
  service   TEXT,
  name      TEXT,
  phone     TEXT,
  date      TEXT,
  time      TEXT,
  duration  INTEGER,
  price_min INTEGER,
  price_max INTEGER,
  is_request INTEGER DEFAULT 0,
  status    TEXT DEFAULT 'new',
  note      TEXT
);
CREATE INDEX IF NOT EXISTS idx_bookings_phone ON bookings(phone);
CREATE INDEX IF NOT EXISTS idx_bookings_date  ON bookings(date);
