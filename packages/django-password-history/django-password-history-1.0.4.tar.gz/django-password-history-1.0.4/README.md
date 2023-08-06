<h1 align="center">Django Password History</h1>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/Lenders-Cooperative/django-password-history)](https://github.com/Lenders-Cooperative/django-password-history/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/kylelobo/The-Documentation-Compendium.svg)](https://github.com/Lenders-Cooperative/django-password-history/pulls)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

</div>

---

<p align="center"> Django module meant to allow django users to keep a history of their previously used passwords.
    <br> 
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting-started)
- [Running Tests](#running-tests)
- [Usage](#usage)
- [Built Using](#built-using)
- [Authors](#authors)
- [Acknowledgments](#acknowledgements)

## About

Django module meant to allow django users to keep a history of their previously used passwords.

## Getting Started

Follow these instructions to install and setup django-password-history in your django project.

### Prerequisites

The only prerequisites to installing django-password-history is having django 2 installed in a Python 3 environment.

### Installing

The installation process for django password history is very simple. Start by running the following command to install the package.

```
pip install django-password-history
```


End with an example of getting some data out of the system or using it for a little demo.

## Running Tests

The test suite for this package is a work in progress. The initial sample test can be run by using the following command.

```
coverage run --source django_password_history runtests.py
```


## Usage

In order to use the system you must add django_password_history to your installed apps in your settings.py file.

```
INSTALLED_APPS = [
    'django_password_history'
]
```

Next you need to define how many historical passwords you want to compare on to the new password when a password is chanced. The default and max is 5 previous passwords.

```
PREVIOUS_PASSWORD_COUNT = 3
```

THe UserPasswordHistory has a one to one relationship with your user model as defined in your settings.py file.

```
AUTH_USER_MODEL = "users.User"
```

To import the UserPasswordHistory model add the following to the top of the desired python file.

```
from django_password_history.models import UserPasswordHistory
```



## Built Using

- [Django](https://www.djangoproject.com/) - Web Framework
- [Cookiecutter Django Package](https://github.com/pydanny/cookiecutter-djangopackage) - Cookie Cutter Django Package

## Authors
- David Graves - Working on behalf of Lender's Cooperative
- [Roderick Smith](https://github.com/rsmith0717) - Working on behalf of Lender's Cooperative


## Acknowledgements

- Inspiration
- References
