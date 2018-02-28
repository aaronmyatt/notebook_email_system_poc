# Email System POC

Presented here is a simple Django app that implements a new format for executing and communicating business critical aspects of a system.

**Motivation**: Long have a wanted to integrate [Jupyter Notebooks](https://jupyter-notebook.readthedocs.io/en/stable/), or the recently beta released [Jupyter Lab](https://jupyterlab.readthedocs.io/en/latest/), into my workflow more deeply. It is the best format for code discovery, iteration, experimentation, communication and learning. Therefore, it seems natural to want to leverage this tool more freely throughout my work.


**Purpose**: Rather than experimenting and designing within a notebook and exporting into a system manually, now the notebooks can be executed in the context of the system. This also grants an opportunity to render the notebooks within the application itself further enhancing transparency aand communication of the business logic (see: `localhost:8000/notebooks`).

Example Notebook Logic:
- [Emailer Logic](https://github.com/aaronmyatt/notebook_email_system_poc/blob/master/notebooks/input/email_sender.ipynb)
- [Updater Logic](https://github.com/aaronmyatt/notebook_email_system_poc/blob/master/notebooks/input/user_updater.ipynb)

## App Installation/Setup

> **Global Prerequisites**
>
> `brew`|`apt-get install python3`
>
> `pip3 install pipenv`
>
> Optionally: setup Docker

0. `cd {{ MVETL repo path }}`
1. `pipenv install --dev`
2. `pipenv run ./manage.py migrate`
3. `pipenv run ./manage.py createsuperuser`

## Development

Convenience Commands

0. `create_emailable_users`

    0. Create two emailable mock users who conform will be emailed in the next email cycle
    1. `pipenv run ./manage.py create_emailable_users`

0. `create_updatable_users`

    0. Create three email updatable mock users who will be updated in the next update cycle
    1. `pipenv run ./manage.py create_updatable_users`

Run Server

0. `cd {{ MVETL repo path }`
1. `scripts/runserver`

Testing ([pytest](https://docs.pytest.org/en/latest/))

0. `cd {{ MVETL repo path }`
1. `pipenv run pytest`

Database Changes ([Django Migrations](https://docs.djangoproject.com/en/2.0/topics/migrations/))

0. Update models as desired
1. `pipenv run ./manage.py makemigrations`
2. `pipenv run ./manage.py migrate`
3. Commit to repo as usual
