CREATE TABLE bets (
    id integer PRIMARY KEY,
    player integer,
    wager integer,
    account integer,
    "char" integer,
    illuminati boolean,
    all_in boolean,
    match integer
);

CREATE TABLE chars (
    id integer PRIMARY KEY NOT NULL,
    name text,
    tier char(3),
    streak integer,
    wins integer,
    losses integer,
    matches_at_tier integer,
    last_match_id integer,
    elo integer DEFAULT 1000,
    tourny_wins integer DEFAULT 0 NOT NULL
);

CREATE TABLE matches (
    id integer PRIMARY KEY NOT NULL,
    "timestamp" datetime,
    red_char integer,
    blue_char integer,
    winner integer,
    red_money integer,
    blue_money integer,
    mode char(1),
    notes text,
    tier char(3),
    tourny_final boolean DEFAULT false NOT NULL
);

CREATE TABLE players (
    id integer PRIMARY KEY NOT NULL,
    name text,
    last_seen datetime,
    last_match_id integer
);

CREATE TABLE tier_moves (
    id integer PRIMARY KEY NOT NULL,
    "char" integer,
    match integer,
    old_tier char(3),
    new_tier char(3),
    type text,
    missed boolean DEFAULT false NOT NULL,
    elo integer DEFAULT 0 NOT NULL
);