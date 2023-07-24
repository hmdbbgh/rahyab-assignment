=================
Rahyab Assignment
=================

**Contents:**

.. contents:: :local:

Instruction
-----------

Step 1.
~~~~~~~
**Install Virtual Environment (venv):**
    For Linux:
        
        .. code-block:: bash

            sudo apt install python3.10-venv

    For Windows:
    
        .. code-block:: bash

            pip install virtualenv

Step 2.
~~~~~~~
**Create a Virtual Environment:**

    For Linux:
        
        .. code-block:: bash

            python3.10 -m venv venv

    For Windows:
    
        .. code-block:: bash

            virtualenv venv

Step 3.
~~~~~~~
**Activate your Virtual Environment:**

    For Linux:
        
        .. code-block:: bash

            source venv/bin/activate

    For Windows:
    
        .. code-block:: bash

            venv\Scripts\activate.bat

Step 4.
~~~~~~~
**Install required packages from requirements.txt:**

.. code-block:: bash

    pip install -r requirements.txt

Step 5.
~~~~~~~
**Create required directories:**

.. code-block:: bash

    mkdir media media/static media/upload media/upload/tmp

Step 6.
~~~~~~~
**Create settings.ini:**

    For Linux:
        
        .. code-block:: bash

            cp settings-template.ini settings.ini 

    For Windows:
    
        .. code-block:: bash

            copy settings-template.ini settings.ini

Step 7.
~~~~~~~
**Docker compose up**
.. code-block:: bash
    docker-compose -f docker-compose.yml up -d

Step 8.
~~~~~~~
**Migrate the basic migrations:**

.. code-block:: bash

    python manage.py migrate

Step 9.
~~~~~~~
**Create superuser:**

.. code-block:: bash

    python manage.py createsuperuser

Step 10.
~~~~~~~
**Run the server:**

.. code-block:: bash

    python manage.py runserver

Step 11.
~~~~~~~
**Celery and celery beat:**

.. code-block:: bash

    celery -A apps.tasks worker -l info --without-gossip --without-mingle --without-heartbeat
    celery -A apps.tasks beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler


Tips
----
We used Redis and Celery and RabbitMQ to reduce the number of read and write requests to the database for obtaining the view count of an announcement."