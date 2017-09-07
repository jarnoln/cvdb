# CVDB

[![CircleCI](https://circleci.com/gh/jarnoln/cvdb.svg?style=shield)](https://circleci.com/gh/jarnoln/cvdb)
[![Travis CI](https://travis-ci.org/jarnoln/cvdb.png)](https://travis-ci.org/jarnoln/cvdb)
[![codecov](https://codecov.io/gh/jarnoln/cvdb/branch/master/graph/badge.svg)](https://codecov.io/gh/jarnoln/cvdb)

CV database for storing and displaying CVs and resumes. There are many like it, but this one is mine.

 - CVs and resumes can be uploaded in [JSON resume format](https://github.com/jsonresume)
 - They can be exported as HTML and PDF
 - Can choose CSS file to be used for styling the CV or write your own CSS
 - [Open source](https://github.com/jarnoln/cvdb/)
   ([MIT licence](https://github.com/jarnoln/cvdb/blob/master/LICENSE))

Running instance at [cvdb.fi](https://cvdb.fi).

Using
-----
 - [Python](https://www.python.org/)(3.5) and [Django](https://www.djangoproject.com/)(1.11)
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

Installation
------------
[Install Ansible](http://docs.ansible.com/ansible/latest/intro_installation.html)

Get sources:

    git clone https://github.com/jarnoln/cvdb.git

Add your host to ansible/inventory. Then:

    ansible-playbook -i ansible/inventory ansible/provision-deb.yaml
    fab -f fabfile.py deploy:host=user@host
