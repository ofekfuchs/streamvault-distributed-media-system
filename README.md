# StreamVault - Distributed Media Records System

StreamVault is a Django web application developed as a wet assignment in a Distributed Information Systems course.
The system models a media-record workflow: households can order and return programs, submit rankings, and view SQL-based analytical results.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Running the Project](#running-the-project)
- [Privacy and Security Notes](#privacy-and-security-notes)
- [Academic Context](#academic-context)

## Project Overview

This project demonstrates practical backend and database skills:
- relational database modeling
- validation of business rules in server-side logic
- SQL analytics queries integrated into a web application
- Django views/templates connected to real database operations

## Features

- **Records Management:** order and return media records with constraints
- **Program Rankings:** submit household rankings for programs
- **Query Results Screen:** display advanced SQL query outputs
- **Validation Logic:** block invalid operations and show user feedback

## Tech Stack

- Python 3
- Django 4
- SQL
- HTML/CSS (Django templates + static files)

## Project Structure

- `Media_App/` - application logic (`views.py`, `models.py`, `urls.py`)
- `djangoProject/` - Django settings and root URL config
- `templates/` - UI pages
- `static/` - CSS and static assets
- `manage.py` - Django entry point

## Getting Started

### Prerequisites

- Python 3.10+ (recommended)
- `pip` package manager

### Installation

1. Clone the repository:
   - `git clone https://github.com/<your-username>/<your-repo-name>.git`
2. Enter the project directory:
   - `cd <your-repo-name>`
3. Create a virtual environment:
   - `python3 -m venv .venv`
4. Activate it:
   - `source .venv/bin/activate`
5. Install dependencies:
   - `pip install django`

## Running the Project

1. Run database migrations (if needed):
   - `python3 manage.py migrate`
2. Start the development server:
   - `python3 manage.py runserver`
3. Open in browser:
   - `http://127.0.0.1:8000/`

## Privacy and Security Notes

- Local and private IDE files are excluded via `.gitignore` (for example: `.idea/`).
- Do not commit real credentials, API keys, or personal identifiers.
- Keep database configuration values in environment variables for private deployments.

## Academic Context

Built as part of a Distributed Information Systems course assignment focused on hands-on database application development.
