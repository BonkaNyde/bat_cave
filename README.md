# School Portal #
This is a PWA that manages CBC operations.

## Dependencies ##
To run this project, you need the following installed:
- python3 
```
$ sudo add-apt-repository ppa:jonathonf/python-3.6
$ sudo apt-get update
$ sudo apt-get install python3.6
```
- postgres
```
$ sudo apt-get update
$ sudo apt-get install postgresql postgresql-contrib libpq-dev
$ sudo service postgresql start
$ sudo -u postgres createuser --superuser $USER
$ sudo -u postgres createdb $USER
```
After this, type `$ psql` and in the prompt, type `ALTER ROLE <username> WITH PASSWORD '<password>';`, replacing \<username\> with your postgres database username and \<password\> with the password you wish to set, to set a password.
To identify your username, type `$USER' and press enter, and your username will be displayed.


- pip3
```
$ sudo apt-get update
$ sudo apt-get install python3-pip
```
- redis
#### Consider the resource : *`https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-18-04`*. ####
```
$ sudo apt-get update
$ sudo apt-get install redis-server
```
- gunicorn
```
$ sudo apt-get update
$ sudo apt-get install gunicorn
```
- celery
```
$ sudo apt-get update
$ sudo apt-get install python-celery-common
```

## *Setup* ##
To setup this project,
1) Clone this repo.
2) Copy the bash code below to create a virtual environment and install all the necessary dependencies.
```
$ python3 -m venv --without-pip .virtual && source .virtual/bin/activate && curl https://bootstrap.pypa.io/get-pip.py | python && pip install -r requirements.txt
```
3) Create a file named `.env` in the root folder, and copy the following environment variables.

```
# caching configuration
# read more https://flask-caching.readthedocs.io/en/latest/
CACHE_TYPE='redis'
CACHE_DEFAULT_TIMEOUT=300

# security configuration
# read more: https://flask-bcrypt.readthedocs.io/en/1.0.1/
#            https://flask-praetorian.readthedocs.io/en/latest/quickstart.html
#            https://pythonhosted.org/Flask-Security/
#            https://flask-wtf.readthedocs.io/en/1.0.x/csrf/
SECRET_KEY='kingkaka'
SESSION_PROTECTION='strong'
BCRYPT_LOG_ROUNDS=13

# mail configurations
# read more: https://pythonhosted.org/Flask-Mail/
MAIL_SERVER='smtp.googlemail.com'
MAIL_PORT=587
MAIL_USE_TLS=1
MAIL_USE_SSL=1
MAIL_USERNAME=`<your_email>`
MAIL_PASSWORD=`<your_mail_password>`
MAIL_SUPPRESS_SEND=0
ADMIN_MAIL_USERNAME=`<a_name_that_identifies_with_your_email>` example `[Gareth Bale]`

# babel configuration
# read more: https://flask-babel.tkte.ch/
BABEL_DEFAULT_LOCALE='en-us'
BABEL_DEFAULT_TIMEZONE='UTC'
BABEL_DOMAIN='messages'
BABEL_TRANSLATION_DIRECTORIES='translations'

# uploads configuration
# read more: https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask
SEND_FILE_MAX_AGE_DEFAULT=3600
MAX_CONTENT_LENGTH=1048576
UPLOADED_PHOTOS_DEST='app/static/photos'

# redis configuration
REDIS_WITH_PASSWORD=1
REDIS_PASSWORD='bigboy999'
REDIS_HOST='localhost' # or '127.0.0.1'
REDIS_PORT=6379

# database configuration
# format: 'postgresql+psycopg2://username:password@localhost/watchlist'
#         '<DB>+<DB_DRIVER>://<DB_USERNAME>:<DB_PASSWORD>@localhost/<DB_NAME>'
DB='postgresql'
DB_DRIVER='psycopg2'
DB_USERNAME='<your_psql_username>'
DB_PASSWORD='<your_psql_password>'
DB_NAME='<your_database_name>'

# for production
DATABASE_URI=''
```
4) Replace the variables in the mail and db configurations with information that match your respective setup.
=======
# bat_cave
