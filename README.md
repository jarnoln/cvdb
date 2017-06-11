# CVDB

[![Travis CI](https://travis-ci.org/jarnoln/cvdb.png)](https://travis-ci.org/jarnoln/cvdb)
[![codecov](https://codecov.io/gh/jarnoln/cvdb/branch/master/graph/badge.svg)](https://codecov.io/gh/jarnoln/cvdb)

CV database

## Installation

Add your host to ansible/inventory. Then:

    ansible-playbook -i ansible/inventory ansible/provision.yaml
    fab -f fabfile.py deploy:host=user@host
