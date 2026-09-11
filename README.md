# The High Screen — Django

A full-stack Django implementation of **The High Screen**, a former sports and entertainment blog rebuilt as a portfolio project for exploring modern web development, content management, data migration, and containerized development.

This version uses **Python and Django** to manage the site's content, application logic, routing, and presentation. Historical articles from the original website are imported into a relational database and rendered server-side using Django templates.

## About The High Screen

**The High Screen** was originally developed as a sports and entertainment blog inspired by sites such as Grantland. The original website used WordPress as its content management system and contained articles written by multiple contributors across several categories.

The project has since been revisited as a way to preserve the original content while exploring different approaches to building and managing the same website.

Several implementations of The High Screen are maintained:

- **Jekyll** — a static implementation of the archived site using Markdown, generated JSON feeds, and GitHub Pages.
- **WordPress** — a rebuilt CMS implementation using WordPress and PHP.
- **Django** — this repository, which rebuilds the site as a Python/Django web application backed by a relational database.

Each implementation uses the same historical content while demonstrating a different approach to web application architecture.

## Django Implementation

This version of The High Screen uses Django for the application's backend, content management, routing, database access, and server-rendered frontend.

Historical articles were exported into JSON and imported into Django using a custom management command. Posts are stored in the database and associated with their original authors and categories.

Django's built-in authentication system is used to represent the site's authors, while the Django Admin interface provides a backend for managing site content.

The public-facing site is rendered using Django templates rather than a separate client-side frontend framework. Shared page elements are defined in a base template, while individual templates handle the article index, category views, and article pages.

The application includes:

- Django models for posts, categories, and site configuration
- Django users representing the original article authors
- Many-to-many relationships between posts and categories
- Original publication dates preserved from the historical site
- Historical HTML article content imported from the original archive
- Category-based article browsing
- Individual article pages
- Server-rendered Django templates
- Shared template inheritance through `base.html`
- Bootstrap-based responsive layout
- Custom The High Screen styling
- Django Admin content management
- Custom JSON import tooling for rebuilding the article database
- Docker support for local development

## Technology

The current implementation uses:

- **Python**
- **Django**
- **SQLite**
- **HTML**
- **CSS**
- **Django Templates**
- **Bootstrap 5.3.8**
- **Docker**
- **Docker Compose**

Django handles application logic and server-side rendering, while Bootstrap and the project's custom stylesheet provide the public-facing layout and visual design.

No client-side JavaScript framework is required for rendering site content.

## Historical Content Import

The original article archive is stored as JSON under the project's `data/` directory.

The JSON contains information including:

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

This allows the SQLite database to be rebuilt from the archived source data rather than relying solely on a pre-populated database.

## Frontend

The public-facing site uses Django's built-in template system.

Shared site elements such as the document structure, masthead, navigation, Bootstrap resources, and custom stylesheet are defined in:

```text
templates/base.html
```

Page-specific templates are stored under:

```text
blog/templates/blog/
```

These templates receive data directly from Django views and render it server-side.

The primary templates include:

```text
index.html
detail.html
category.html
```

Reusable template fragments can be stored under:

```text
blog/templates/blog/partials/
```

For example, the article listing can reuse a shared post-preview template instead of duplicating the same markup across the homepage and category pages.

### Styling

The High Screen's custom styling is stored under Django's static-file structure:

```text
blog/static/blog/css/ths.css
```

The stylesheet contains the site's:

- Color palette
- Masthead styling
- Navigation styling
- Article preview typography
- Article metadata styling
- Responsive behavior
- Bootstrap component overrides

Bootstrap is stored separately from the project's custom CSS so third-party assets remain distinct from application-specific styling.

A typical static-file structure is:

```text
blog/static/blog/
├── css/
│   └── ths.css
└── vendor/
    └── bootstrap/
        ├── bootstrap.min.css
        └── bootstrap.bundle.min.js
```

Bootstrap's JavaScript bundle is retained for Bootstrap components such as the responsive navigation menu.

The site currently does not require a separate custom JavaScript file.

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

A rebuild is generally only necessary after changing the Dockerfile or Python dependencies:

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

Apply database migrations:

```bash
docker compose exec web python manage.py migrate
```

Create new migrations:

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
│   │   ├── __init__.py
│   │   └── commands/
│   │       ├── __init__.py
│   │       └── import_posts.py
│   │
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── ...
│   │
│   ├── static/
│   │   └── blog/
│   │       ├── css/
│   │       │   └── ths.css
│   │       └── vendor/
│   │           └── bootstrap/
│   │               ├── bootstrap.min.css
│   │               └── bootstrap.bundle.min.js
│   │
│   ├── templates/
│   │   └── blog/
│   │       ├── index.html
│   │       ├── detail.html
│   │       ├── category.html
│   │       └── partials/
│   │           └── post_preview.html
│   │
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── context_processors.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── data/
│   └── all-posts.json
│
├── img/
│   └── ...
│
├── personal_blog/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── templates/
│   └── base.html
│
├── .dockerignore
├── .gitignore
├── compose.yaml
├── Dockerfile
├── db.sqlite3
├── manage.py
├── README.md
└── requirements.txt
```

## Project Structure Details

### `blog/`

The primary Django application.

It contains the models, views, URL routing, templates, static files, administration configuration, migrations, context processors, and custom management commands used by The High Screen.

### `blog/management/`

Contains custom Django management commands.

The `import_posts` command rebuilds the historical article database from the archived JSON data.

### `blog/migrations/`

Contains Django's database migration history.

Migration files describe changes to the application's database schema and are managed through Django's migration system.

### `blog/templates/blog/`

Contains templates specific to the blog application.

These templates extend the site's shared base template and render the article index, individual articles, category pages, and reusable template fragments.

### `blog/static/blog/`

Contains static resources used by the public-facing site.

Custom The High Screen styling is stored separately from third-party Bootstrap resources.

### `data/`

Contains source data used to rebuild the historical article archive, including the JSON export consumed by the custom import command.

### `img/`

Contains image assets associated with the site and its historical content.

### `personal_blog/`

The Django project configuration package.

It contains the project's global settings, root URL configuration, and ASGI/WSGI entry points.

### `templates/`

Contains templates shared across the application.

The primary shared template is:

```text
templates/base.html
```

This defines the site's common document structure, masthead, navigation, static resources, and content area.

### `db.sqlite3`

The SQLite database used by the Django application.

## Database

The project uses SQLite with Django's ORM.

The historical archive is reconstructed through the following flow:

```text
Historical JSON
      ↓
Custom Django Importer
      ↓
Django Models / ORM
      ↓
SQLite
```

Posts are represented through Django models and associated with Django users and categories through relational database fields.

The import process preserves the original authors, article categories, publication dates, and article body content while allowing the archive to be managed through Django.

## Django Template Architecture

The application uses Django template inheritance to avoid duplicating shared HTML across pages.

The basic rendering flow is:

```text
Django Models
      ↓
Django ORM
      ↓
views.py
      ↓
Template Context
      ↓
Django Templates
      ↓
Rendered HTML
```

`base.html` defines the common site layout.

Individual templates extend it:

```text
base.html
│
├── index.html
│   └── post_preview.html
│
├── category.html
│   └── post_preview.html
│
└── detail.html
```

This keeps shared elements such as the masthead, navigation, Bootstrap resources, and site styling in one location while allowing each page to define its own content.

## Status

The Django implementation contains the historical The High Screen article archive with its original authors, categories, publication dates, and article bodies.

The archive is stored relationally through Django's ORM, managed through Django Admin, rendered using Django templates, styled using Bootstrap and custom CSS, and can be run locally through Docker Compose or a standard Python development environment.