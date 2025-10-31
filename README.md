# Mini CRM

A lightweight Customer Relationship Management (CRM) system built with Django and Django REST Framework. This API-first application helps manage client relationships, track interactions, and monitor sales pipeline progress.

## Features

- Client management with customizable fields
- Stage-based pipeline tracking (Lead, In Progress, Active)
- Client interaction logging (Calls, Emails, Meetings, Notes)
- User authentication with JWT tokens
- Staff assignment and tracking
- Statistics and reporting dashboard
- RESTful API with comprehensive endpoints

## Technology Stack

- Python 3.x
- Django 5.x
- Django REST Framework
- MySQL database
- JWT authentication (djangorestframework-simplejwt)
- python-decouple for configuration management

## Installation

### Prerequisites

- Python 3.8 or higher
- MySQL server
- pip package manager

### Setup Steps

1. Clone the repository:

```bash
git clone <repository-url>
cd mini-crm
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with the variables from `.env.example`

5. Create the database:

```bash
mysql -u root -p
CREATE DATABASE mini_crm;
exit;
```

6. Run migrations:

```bash
python manage.py migrate
```

7. Create a superuser:

```bash
python manage.py createsuperuser
```

8. Start the development server:

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## Data Models

### Client

- Personal information (name, email, phone, company)
- Address and notes
- Pipeline stage (Lead, In Progress, Active)
- Assignment tracking (created_by, assigned_to)
- Timestamps (created_at, updated_at)

### ClientInteraction

- Linked to a specific client
- Interaction type (Call, Email, Meeting, Note)
- Subject and description
- Creator tracking
- Timestamp

## Authentication

The API uses JWT (JSON Web Token) authentication. Obtain tokens and use them to access protected endpoints.

### Obtaining Tokens

```bash
POST /api/token/
{
  "username": "your_username",
  "password": "your_password"
}
```

Response:

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Using Tokens

Include the access token in the Authorization header:

```
Authorization: Bearer <access_token>
```

### Refreshing Tokens

```bash
POST /api/token/refresh/
{
  "refresh": "your_refresh_token"
}
```

## API Documentation

For detailed API endpoints, request/response formats, and examples, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

## API Testing with Postman

### Quick Start with Postman

1. **Import the collection:**

   - Open Postman
   - Click "Import" button
   - Select `Mini_CRM_API.postman_collection.json`
   - Select `Mini_CRM_Local.postman_environment.json`

2. **Select the environment:**

   - Click the environment dropdown (top right)
   - Select "Mini CRM - Local"

3. **Obtain authentication tokens:**

   - Go to "Authentication" folder
   - Run "Obtain Token Pair" request
   - Tokens are automatically saved to variables

4. **Start testing:**
   - All other requests will automatically use the saved token
   - Try creating a client, adding interactions, viewing statistics

### Collection Features

- Pre-configured requests for all API endpoints
- Automatic token management (tokens saved automatically)
- Environment variables for easy configuration
- Request examples with sample data
- Organized by functional area (Clients, Interactions, Statistics)
