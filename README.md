

## LOCAL DEVELOPMENT
### Set Up Project

#### Install postgres and create database
- Install postgres using ubuntu:
    ```
    sudo sh -c 'echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
    sudo apt-get update
    sudo apt-get -y install postgresql
    ```
- Install PostgreSQL development libraries:
`sudo apt-get install libpq-dev`
- Install PostgreSQL adapter for Python
`pip install psycopg2`
- Run postgresql service
`sudo service postgresql start`
- Create db
`sudo -u postgres psql`
- Create USER
    ```
    CREATE USER yourusername WITH PASSWORD 'yourpassword';
    GRANT ALL PRIVILEGES ON DATABASE yourdbname TO yourusername;
    ```

- Create DB
`createdb surface-interval-db`

#### Run migrations
`python manage.py migrate`


## USING THE API
Endpoints require an API token. The token is tied to a user and is provided by registering. Access the /register endpoint and provide the following:
```
username
email
password
first_name
last_name
units (provide 'metric' or 'imperial')
```

Use the returned token after registering and provide it in the header as `Authorization: TOKEN "your_token"`
