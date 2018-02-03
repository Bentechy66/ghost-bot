BEGIN TRANSACTION;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS emoji;
DROP TABLE IF EXISTS buy_offers;
DROP TABLE IF EXISTS sell_offers;
DROP TABLE IF EXISTS inventory_items;

CREATE TABLE players (
    user_id char(21) not null unique,
    balance default 0
);

CREATE TABLE emoji (
  name char(30) not null unique,
  last_trade default "-"
);

CREATE TABLE buy_offers (
  name char(30) not null,
  user_id char(21) not null,
  price int(10)
);

CREATE TABLE sell_offers (
  name char(30) not null,
  user_id char(21) not null,
  price int(10)
);

CREATE TABLE inventory_items (
  user_id char(21) not null,
  item char(30) not null,
  quantity int(10) not null
);
COMMIT;
