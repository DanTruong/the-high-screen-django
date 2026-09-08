# The High Screen — Django

A full-stack Django implementation of **The High Screen**, a former sports and entertainment blog rebuilt as a portfolio project for experimenting with modern web development, content management, and deployment practices.

This version uses **Python and Django** to manage the site's content and application logic, with the historical article archive imported into a relational database and managed through Django's built-in administration interface.

## About The High Screen

**The High Screen** was originally developed as a sports and entertainment blog inspired by sites such as Grantland. The original website used WordPress as its content management system and contained articles written by multiple contributors across several categories.

The project has since been revisited as a way to preserve the original content while exploring different approaches to building and managing the same website.

Several implementations of The High Screen are being maintained, including:

- **Jekyll** — a static implementation of the archived site using Markdown, generated JSON feeds, and GitHub Pages.
- **WordPress** — a rebuilt version using WordPress and PHP.
- **Django** — this repository, which rebuilds the site as a Python/Django web application backed by a relational database.

Rather than simply restoring the original site, each implementation provides an opportunity to explore a different web development stack while working from the same historical content.

## Django Implementation

This version of The High Screen uses Django to provide both the application backend and content-management functionality.

The historical articles were exported into JSON and imported into Django using a custom management command. Posts are stored in the database and associated with their original authors and categories.

Django's built-in authentication system is used to represent the site's authors, while the Django Admin interface provides a backend for managing the site's content.

The application currently includes:

- Django models for posts and categories
- Django users representing the original article authors
- Many-to-many relationships between posts and categories
- Original publication dates preserved from the historical site
- HTML article content imported from the original archive
- Category-based article browsing
- Individual article pages
- Django Admin content management
- Custom JSON import tooling for rebuilding the article database
- Docker support for local development

## Technology

The current implementation uses:

- **Python**
- **Django**
- **SQLite**
- **HTML / CSS**
- **Django Templates**
- **Docker**
- **Docker Compose**

SQLite is currently used to keep development simple and make the project easy to run locally. A future phase of the project will migrate the application to **PostgreSQL**.

## Historical Content Import

The original article archive is stored as JSON under the project's `data/` directory.

The JSON contains information such as:

- Article title
- Slug
- Author
- Original publication date
- Categories
- Article body
- Historical metadata

A custom Django management command imports this information into the database and associates posts with their corresponding Django users and categories.

The importer can be run with:

```bash
python manage.py import_posts data/all-posts.json
```

This allows the database to be rebuilt from the archived source data rather than relying solely on a pre-populated database.

## Running With Docker

Docker is the recommended way to run the project locally.

This avoids needing to install Python, create a Python virtual environment, or install the project's Python dependencies directly on the host computer.

### Requirements

Install:

- Docker
- Docker Compose

Docker Desktop includes Docker Compose on Windows and macOS.

### Start the Application

Clone the repository and enter the project directory:

```bash
git clone <repository-url>
cd the-high-screen-django
```

Build and start the Django container:

```bash
docker compose up --build
```

Once Django starts, open:

```text
http://localhost:8000
```

The local project directory is mounted into the container, allowing changes to Django templates, Python files, CSS, and other project files to be reflected during development without rebuilding the container for every change.

### Starting the Project Again

After the initial build, the application can normally be started with:

```bash
docker compose up
```

A rebuild may be necessary after changing the Dockerfile or Python dependencies:

```bash
docker compose up --build
```

### Stopping the Application

Press `Ctrl+C` in the terminal running Docker Compose, or run:

```bash
docker compose down
```

## Django Management Commands With Docker

Django management commands can be executed inside the running container without installing Python on the host system.

For example:

```bash
docker compose exec web python manage.py migrate
```

Create migrations:

```bash
docker compose exec web python manage.py makemigrations
```

Create an administrator:

```bash
docker compose exec web python manage.py createsuperuser
```

Import the historical article archive:

```bash
docker compose exec web python manage.py import_posts data/all-posts.json
```

## Running Without Docker

The project can also be run using a local Python installation and virtual environment.

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Apply the database migrations:

```bash
python manage.py migrate
```

Start the Django development server:

```bash
python manage.py runserver
```

The application will then be available at:

```text
http://127.0.0.1:8000
```

## Project Structure

```text
the-high-screen-django/
├── blog/
│   ├── management/
│   │   └── commands/
│   │       └── import_posts.py
│   ├── migrations/
│   ├── templates/
│   │   └── blog/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── data/
│   └── all-posts.json
│
├── img/
│
├── personal_blog/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── templates/
│   └── base.html
│
├── db.sqlite3
├── manage.py
├── requirements.txt
├── Dockerfile
├── compose.yaml
├── .dockerignore
└── README.md
```

### `blog/`

The primary Django application. It contains the models, views, URL routing, templates, administration configuration, migrations, and custom management commands used by The High Screen.

### `data/`

Contains source data used to rebuild the historical article archive, including the JSON export consumed by the custom import command.

### `img/`

Contains image assets associated with the site and its historical content.

### `personal_blog/`

The Django project configuration package. It contains the project's global settings, root URL configuration, and ASGI/WSGI entry points.

### `templates/`

Contains templates shared across the application, including the site's base layout.

### `db.sqlite3`

The SQLite development database.

## Database

The project currently uses SQLite for development.

Django's ORM separates most of the application's database logic from the underlying database engine, allowing the project to later move to PostgreSQL without rewriting the application's models and queries.

The planned database progression is:

```text
Historical JSON
      ↓
Custom Django Importer
      ↓
Django Models / ORM
      ↓
SQLite
      ↓
PostgreSQL
```

SQLite provides a lightweight environment while the Django application, templates, content structure, and styling are being developed. PostgreSQL will be introduced in a later phase as the project moves toward a more production-oriented configuration.

## Current Project Goals

The current phase of the Django implementation focuses on rebuilding the core functionality of The High Screen while becoming familiar with Django's application architecture.

This includes working with:

- Models and database relationships
- Django's ORM
- Authentication and users
- Django Admin
- URL routing
- Views
- Templates
- Custom management commands
- Historical data migration
- Containerized development

Once the core application and frontend are in place, the project can be expanded with PostgreSQL and additional deployment-oriented configuration.

## Status

This project is an active modernization of an older website and is intended primarily as a development and portfolio project.

The historical content has been imported into Django, including its original authors, categories, publication dates, and article bodies. The current focus is on refining the Django implementation and rebuilding the presentation layer while preserving the original archive.