#!/usr/bin/env python
import random

PROJECT_NAME = 'cvdb'


def generate_passwords(password_file_path):
    password_file = open(password_file_path, 'w')
    chars = 'abcdefghijklmnopqrstuvxyz01234567890_-!*'
    secret_key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
    # mysql_password = raw_input('Enter MySQL password for user "tom":')
    password_file.write("SECRET_KEY = '%s'\n" % secret_key)
    # password_file.write("MYSQL_PASSWORD = '%s'\n" % mysql_password)
    password_file.close()


if __name__ == '__main__':
    password_file_path = '%s/passwords.py' % PROJECT_NAME
    generate_passwords(password_file_path)
