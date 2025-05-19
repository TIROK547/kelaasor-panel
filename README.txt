# Kelaasor Panel

## Overview

This project is a Django-based backend system for managing users, tickets, and bootcamps with support for technical and financial admins. It supports ticket creation, messaging, user verification via SMS, and role management with groups for admin types.

## Features

- User registration with phone number verification via SMS.
- Ticketing system with statuses like pending, answered, closed.
- Message creation within tickets.
- Role-based access control with user groups:
  - `tech_support` group for technical admins.
  - `fin_support` group for financial admins.
  - `default user` group for normal users.
- Admin management to assign/revoke roles.
- Bootcamp management with join requests and state decisions.
- Async tasks with Celery for sending SMS and alerts.

## Installation

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd kelaasorPanel

    Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

Install dependencies:

pip install -r requirements.txt

Configure your settings (settings.py or .env):

    Set up database.

    Add your Kavenegar API key.

    Configure email backend for sending ticket alerts.

Run migrations:

python manage.py migrate

Create necessary user groups (run in Django shell):

python manage.py shell

Then:

from django.contrib.auth.models import Group

Group.objects.get_or_create(name='tech_support')
Group.objects.get_or_create(name='fin_support')
Group.objects.get_or_create(name='default user')

Run the development server:

    python manage.py runserver

Usage

    Register users: /user/create/

    Request verification code: /user/verification-code/

    Verify code: /user/verify-code/

    Create tickets and messages: /ticket/ endpoints

    Admin role management: /admin-status/change-staff/<user_id>/

    Bootcamp management: /admin-status/ endpoints

Notes

    Celery must be configured and running to handle async tasks like SMS sending.

    Make sure email backend is properly configured for alerts.

    Phone number validation supports Iranian numbers only.