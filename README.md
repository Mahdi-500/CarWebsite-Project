# CarWebsite-Project

## How to run
    1 - install python version 3.12.8 from python.org
        * if you have more than 1 version installed check which version is active by typing "python --version" in your terminal

    2 - create a virtual environment by following the steps blow:
        2.1 - go to your terminal
        2.2 - change the directory to your desired destination
        2.3 - run this command "python -m venv <name of you virtual environment>
    
    3 - clone the repository

    4 - open the folder in your code editor or IDE

    5 - activate the venv by simply changing the directory to a foldaer named "Scripts" and after than type in "activate"

    6 - go back to your main folder (the one that "CarWebiste" is in it) and install the requirements by running this command: "pip install -r requirements.txt"

    7 - change the directory to "CarWebsite"

    8 - run these commands below **in order**:
        8.1 - python manage.py makemigrations
        8.2 - python manage.py migrate
        8.3 - python manage.py runserver