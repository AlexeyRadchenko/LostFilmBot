Telegram bot for tv shows on LostFilm.tv
=========================================
- python - 3.6
- sqlAlchemy - 1.2.7
- requests-html - 0.9.0
- python-telegram-bot - 10.1.0

Telegram: [@LoFi_bot](https://t.me/LoFi_bot)
---------
<img src="https://i.imgur.com/GxitKci.jpg" height="500" align="middle">

Install:
--------
1. Install PostgreSQL

```
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```
2. Create data base
```
CREATE DATABASE <data_base_name>;
```
3. Create user for data base
```
CREATE USER <user_name> WITH PASSWORD 'CREATESTRONGPASSS';
ALTER ROLE crocusdb_user SET client_encoding TO 'utf8';
ALTER ROLE crocusdb_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE crocusdb_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE <data_base_name> TO <user_name>;
```
4. Install python requirements
```
pip install -r requirements.txt
```
5. Create tables in database
```
python create_db_schema.py
```
6. Rename conf_example.py -> conf.py and configure bot.
```
TOKEN=<bot_token>
...and other setting in conf.py
```

7. ***Run Bot***
```
python bot.py
```
