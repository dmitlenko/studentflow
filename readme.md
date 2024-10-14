#StudentFlow
StudentFlow is a cross-platform online whiteboard specifically designed for students to find and post announcements and communicate with each other.

## System requirements
Server requirements:
- Operating system: Linux, Windows or macOS.
- Programming language: Python (version 3.10+).
- Database: PostgreSQL.
- Cache system: Redis (version 3.0+)

Client requirements:
- Web browser: A modern web browser such as Google Chrome, Mozilla Firefox, Safari or Microsoft Edge.
- JavaScript support: The browser must support JavaScript execution.

Mobile requirements:
- Operating system: Android or iOS.
- OS version: Minimum Android 6.0 or iOS 12.

Other requirements:
- Internet connection: An active Internet connection is required to use the StudentFlow online whiteboard.

## Configuration.
To configure the parameters of the StudentFlow project, you can use the `.env' file. This file is a text file that stores the configuration variables of the environment.

To configure the project, create a file named `.env' in the root directory of the project and add lines of the following format:
```
# Configure the Django framework
DJANGO_SECRET_KEY='<Django secret key>'
DJANGO_ALLOWED_HOSTS=<site domain> # for example 'example.com'
DJANGO_CSRF_TRUSTED_ORIGINS=<site domain with protocol> # for example 'https://example.com'

# Setting up the Redis cache system
REDIS_HOST=<cache system host> # 127.0.0.1 by default
REDIS_PORT=<cache port> # 6379 by default

# Setting up the PostgreSQL database
POSTGRES_DB=<database name>
POSTGRES_USER=<database user>
POSTGRES_PASSWORD=<database user password>
POSTGRES_HOST=<database host> # 127.0.0.1 by default
POSTGRES_PORT=<database port> # 5432 by default
```

Translated with DeepL.com (free version)

To get the Django secret key, run the following command:
```
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
This will print the secret key, which can then be inserted into the `.env` file.

## First run instructions

### Step 0: Setting up the virtual environment

1. Make sure you have Python version 3.10+ installed. If not, download and install Python from the [official website] (https://www.python.org/).
2. Open a command prompt (terminal) on your computer.
3. Change to the project folder using the command `cd /path/to/project/folder`.
4. Create a new virtual environment using the command:

    ```
    python3 -m venv venv
    ```

5. Activate the virtual environment:

    - for Windows:

        ```
        /venv/Scripts/activate
        ```
    
    - for Linux:

        ```
        source /venv/bin/activate
        ```

### Step 1: Install the necessary dependencies

1. Make sure that you have activated the virtual environment
2. Navigate to the project folder using the command `cd /path/to/project/folder`.
3. Install the necessary packages from the `requirements.txt` file using the command:

    ```
    pip install -r requirements.txt
    ```

    This command will install all the dependencies required for the project specified in the requirements.txt file.

### Step 2: Deploy the PostgreSQL database

1. Make sure that the PostgreSQL server is installed on your computer. If not, download and install PostgreSQL from the [official website](https://www.postgresql.org/).
2. Open a command prompt (terminal) on your computer.
3. Change to the project folder using the command `cd /path/to/project/folder`.
4. Start the PostgreSQL server if it is not already running.
5. Perform the database migration using the command:

    ```
    python3 manage.py migrate
    ```

    This command will create the necessary tables and database structure based on the defined project models.

### Step 3: Start the Redis server
1. Make sure that the Redis server is installed on your computer. If not, download and install Redis from the [official website] (https://redis.io/).
2. Open a command prompt (terminal) on your computer.
3. Change to the project folder using the command `cd /path/to/project/folder`.
4. Start the Redis server using the command:

    ```
    sh run_redis.sh
    ```

    This command will execute the script run_redis.sh, which must be located in the root directory of the project. The script will start the Redis server with the settings defined in the file.

### Step 4: Create a new administrator
1. In the command prompt, change to the folder where the manage.py file is located.
2. Run the following command:
   
    ```
    python3 manage.py createsuperuser
    ```

3. Follow the instructions on the screen.

### Step 5: Run the Django project

1. At the command prompt, change to the folder where the manage.py file is located.
2. Start the local project server using the command:

    ```
    python3 manage.py runserver
    ```

    This command will start the server on the local computer at http://127.0.0.1:8000/. You can also run the command to start the project globally:

    ```
    python3 manage.py runserver 0.0.0.0:80
    ```

    After that, you will be able to navigate to the site domain, which is specified in the file `.env`.

Translated with DeepL.com (free version)