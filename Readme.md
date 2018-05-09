Telegram bo for LostFilm.tv updates
----------------
- for use socks5 proxy install urllib3 from repo
```
pip install git+https://github.com/urllib3/urllib3
```
-TOKEN, SOCKS_USER, SOCKS_PASS in conf.py

PostgreSQL install
```
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```
Создание базы в PostgreSQL
```
CREATE DATABASE scrm_crocusdb;
CREATE USER crocusdb_user WITH PASSWORD 'CREATESTRONGPASSS';
ALTER ROLE crocusdb_user SET client_encoding TO 'utf8';
ALTER ROLE crocusdb_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE crocusdb_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE scrm_crocusdb TO crocusdb_user;

```
