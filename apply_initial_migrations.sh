#!/bin/bash
python manage.py migrate auth &&
python manage.py migrate ledger_api_client &&

# patch admin 0001_initial migration file
if [ $VIRTUAL_ENV ]; then
    echo $VIRTUAL_ENV
    patch venv/lib/python3.8/site-packages/django/contrib/admin/migrations/0001_initial.py < 0001_initial.py.patch1 &&
    status=$?
    if [ $status -ne 0  ]; then
          echo "Migration patch filed: $status"
            exit $status
        fi
else
    echo "no venv"
    patch /usr/local/lib/python3.8/dist-packages/django/contrib/admin/migrations/0001_initial.py < 0001_initial.py.patch1 &&
    status=$?
    if [ $status -ne 0  ]; then
          echo "Migration patch filed: $status"
            exit $status
        fi
fi

python manage.py migrate admin &&

# repatch admin 0001_initial migration file
if [ $VIRTUAL_ENV ]; then
    echo $VIRTUAL_ENV
    patch venv/lib/python3.8/site-packages/django/contrib/admin/migrations/0001_initial.py < 0001_initial.py.patch2 &&
    status=$?
    if [ $status -ne 0  ]; then
          echo "Migration patch filed: $status"
            exit $status
        fi
else
    echo "no venv"
    patch /usr/local/lib/python3.8/dist-packages/django/contrib/admin/migrations/0001_initial.py < 0001_initial.py.patch2 &&
    status=$?
    if [ $status -ne 0  ]; then
          echo "Migration patch filed: $status"
            exit $status
        fi
fi

python manage.py migrate django_cron &&
python manage.py migrate sites 0001_initial &&
python manage.py migrate flatpages 0001_initial &&
python manage.py migrate sites 0002_alter_domain_unique &&
python manage.py migrate taggit &&
python manage.py migrate sessions &&
python manage.py migrate
