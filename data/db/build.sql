CREATE TABLE IF NOT EXISTS prefixes (
  id integer PRIMARY KEY,
  prefix text
);

CREATE TABLE IF NOT EXISTS afk (
  id integer PRIMARY KEY,
  mentions integer DEFAULT 0,
  reason text DEFAULT "No Reason"
);