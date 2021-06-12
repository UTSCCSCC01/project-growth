#!/bin/bash
for f in 'virtualenv -p python3 .' 'source bin/activate' 'pip install django' 'pip install django-crispy-forms' 'pip install pillow' 'pip install django-channels' 'cd Growth' 'python3 manage.py runserver'
do
  $f
  rc=$?
  if [[ 0 != $rc ]]; then echo Failed command: ${f}; break; fi
done