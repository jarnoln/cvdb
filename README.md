# CVDB

[![CircleCI](https://circleci.com/gh/jarnoln/cvdb.svg?style=shield)](https://circleci.com/gh/jarnoln/cvdb)
[![Travis CI](https://travis-ci.org/jarnoln/cvdb.svg)](https://travis-ci.org/jarnoln/cvdb)
[![codecov](https://codecov.io/gh/jarnoln/cvdb/branch/master/graph/badge.svg)](https://codecov.io/gh/jarnoln/cvdb)

CV database for storing and displaying CVs and resumes. There are many like it, but this one is mine.

 - CVs and resumes can be uploaded in [JSON resume format](https://github.com/jsonresume)
   ([examples](https://github.com/jarnoln/cvdb/tree/master/examples))
 - They can be exported as HTML and PDF
 - Can choose CSS file to be used for styling the CV or write your own CSS
 - [Open source](https://github.com/jarnoln/cvdb/)
   ([MIT licence](https://github.com/jarnoln/cvdb/blob/master/LICENSE))

Sources at [GitHub](https://github.com/jarnoln/cvdb).
Running instance at [cvdb.fi](https://cvdb.fi).

Using
-----
 - [Python](https://www.python.org/)(3.9) and [Django](https://www.djangoproject.com/)(4.1)
 - [Behave](http://pythonhosted.org/behave/),
   [behave-django](https://behave-django.readthedocs.io/) and
   [Selenium](http://www.seleniumhq.org/) for functional testing
 - [GitHub](https://github.com/jarnoln/cvdb/) for version control
 - [Ansible](https://www.ansible.com/) for provisioning servers
 - [Fabric](http://www.fabfile.org/) for automated deployments
 - [Travis](https://travis-ci.org/jarnoln/cvdb) and
   [CircleCI](https://circleci.com/gh/jarnoln/cvdb) for test automation
 - [codecov.io](https://codecov.io/gh/jarnoln/cvdb) for test coverage tracking
 - [django-allauth](http://django-allauth.readthedocs.io/en/latest/) for 3rd party authentication
 - [JSON resume](https://github.com/jsonresume) as reference resume format 
 - [AWS](https://aws.amazon.com/) and/or
   [DigitalOcean](https://www.digitalocean.com/) for servers
 - [PyCharm](https://www.jetbrains.com/pycharm/) as IDE
 - [Obey the testing goat](https://www.obeythetestinggoat.com/) for guidance and inspiration

Deploy
------------
[Install Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)

Install fabric 1.x:

    pip install 'fabric<2.0' 

Get sources:

    git clone https://github.com/jarnoln/cvdb.git

Add your host to ansible/inventory. Then:

    ansible-playbook -i ansible/inventory ansible/provision-deb.yaml

    fab -f fabfile.py deploy:host=user@host


Set up development environment
------------------------------

Get sources:

    git clone https://github.com/jarnoln/cvdb.git

Create virtual environment and install Python packages:

    mkvirtualenv -p /usr/bin/python3 cvdb
    pip install -r requirements.txt

Generate password:

    python cvdb/generate_passwords.py cvdb/passwords.py

Initialize DB:

    ./manage.py migrate
    ./manage.py makemigrations viewcv
    ./manage.py migrate viewcv

Run tests:

    ./manage.py test

If tests pass, you should be good to go.

Run development server:

    ./manage.py runserver

Now should be able to see CVDB in your browser at http://127.0.0.1:8000/

Note: When trying to sign up on local server, sending confirmation email fails
unless a mail server is installed. Installing for example Postfix should fix
this:

    sudo apt install postfix
