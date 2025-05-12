
# LOCAL DEVELOPMENT

## 🛠️ Set Up Project

#### Containerized (recommended) 📦
1. Ensure docker is installed: https://docs.docker.com/engine/install/
2. Run `bin/build` which will run the docker build command. This will also run django migrations and run django server.
3. Run `bin/dbseed` which will install fixtures and seed the database.

That's it! 

#### Non-containerized ⌨️
1. #### Install postgres
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

2. #### Run postgresql service
- `sudo service postgresql start`

3. #### Create db
- `sudo -u postgres psql`

4. #### Create USER
    ```
    CREATE USER surfaceinterval WITH PASSWORD 'yourpassword';
    GRANT ALL PRIVILEGES ON DATABASE surface-interval-db TO surfaceinterval;
    ```

5. #### Create DB
- `createdb surface-interval-db`

6. #### Run migrations
- `python manage.py migrate`


## ▶️ USING THE API

#### Connect to local db

<b>Docker:</b> As long as container is running, you are good to go!

<b>Non-Docker:</b> Run `bin/pgconnect` -- This automatically enters your user password as stored in the .env file to connect.

⚠️ Endpoints require a token. The token is tied to a user and is provided by logging in, registering or running the `drf_create_token` command.

#### Register New User 🪪
As long as you ran the `bin/dbseed` command, you should not have to do this but for registering a new user and testing the `/register` endpoint, provide the following:
```
username
email
password
first_name
last_name
units (provide 'metric' or 'imperial')
```

#### Login and Tokens
Access the /login endpoint and provide the following:
```
username
password
```

#### Generate Token 🪙
Alternatively, run `python manage.py drf_create_token <username>` from the CLI which will show:
```
Generated token <TOKEN> for user TestUser
```

### API Authorization Header 🔒
Provide the token in the header as `Authorization: TOKEN "your_token"`
