CREATE TABLE "followers" (
  "id" integer PRIMARY KEY,
  "name" varchar,
  "url" varchar
);

CREATE TABLE "subscribers" (
  "id" integer PRIMARY KEY,
  "name" varchar,
  "url" varchar
);

CREATE TABLE "users" (
  "id" integer PRIMARY KEY,
  "name" varchar,
  "url" varchar
);

CREATE TABLE "users_subscribers" (
  "id_users" integer,
  "id_subscribers" integer
);

CREATE TABLE "users_followers" (
  "id_users" integer,
  "id_followers" integer
);

ALTER TABLE "users_subscribers" ADD FOREIGN KEY ("id_users") REFERENCES "users" ("id");

ALTER TABLE "users_subscribers" ADD FOREIGN KEY ("id_subscribers") REFERENCES "subscribers" ("id");

ALTER TABLE "users_followers" ADD FOREIGN KEY ("id_users") REFERENCES "users" ("id");

ALTER TABLE "users_followers" ADD FOREIGN KEY ("id_followers") REFERENCES "followers" ("id");
