# LITReview (OC_P9)

LITReview is a **training project** part of "Python application developer" training of OpenClassrooms. 
It's a web app made with Django's framework.

Make sure to install all packages in 'requirements.txt'.

## Download & Create a virtual env

For this software you will need Python 3 (made on Python 3.9.6)

Open a terminal and navigate into the folder you want LITReview to be downloaded. 
Then run the following commands: 

* From repository download files and clone the folder.
    ```
    $ git clone https://github.com/AatroXissTV/litreview_django.git LITReview
    $ cd LITReview
    ```
* Create a Python environment named "env".
    ```
    $ python -m venv env
    ```
* Activate the environment.
    ```
    $ source/env/bin/activate #MacOS & linux
    $ source/env/Scripts/activate # Windows
    ```
* Install packages from **requirements.txt**.
    ```
    $ pip install -r requirements.txt
    ```
* Once you have created the environment and the requirements.txt you can launch the server that way :
    ```
    $ python manage.py runserver
    ```

In your web browser you can use the following URL to connect to the website: http://127.0.0.1:8000/

## Generate Flake8 Report

You can generate a flake8 report. It's located inside the 'flake-report' folder. 
flake8 has an option for max-line set to 79.

* Generate Flake8 report:
    ```
    $ flake8 --format=html --htmldir=flake-report
    ```

## Updates

This project is finished and all features are working.

## Author

This software was made by Antoine "AatroXiss" Beaudesson with :heart: and :coffee:

## Support

Contributions, issues and features requests are welcome ! 
Feel free to give a ⭐️ if you liked this project. 