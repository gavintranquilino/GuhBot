CREATE TABLE IF NOT EXISTS prefixes (
  id integer PRIMARY KEY,
  prefix text
);

CREATE TABLE IF NOT EXISTS afk (
  id integer PRIMARY KEY,
  mentions integer DEFAULT 0,
  reason text DEFAULT "No Reason"
);

CREATE TABLE IF NOT EXISTS snipe (
  channel_id integer PRIMARY KEY,
  user_id integer,
  time integer,
  message text
);