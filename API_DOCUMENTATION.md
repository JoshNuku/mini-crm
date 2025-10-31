# API Documentation

Complete reference for the Mini CRM REST API.

## Base URL

```
http://localhost:8000/api
```

## Authentication

All endpoints (except token endpoints) require JWT authentication. Include the access token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

## Authentication Endpoints

### 1. Obtain Token Pair

Authenticate and receive access and refresh tokens.

**Endpoint:** `POST /api/token/`

**Authentication:** Not required

**Request Body:**

```json
{
  "username": "string",
  "password": "string"
}
```

**Response:** `200 OK`

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Example:**

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password123"}'
```

### 2. Refresh Access Token

Get a new access token using a refresh token.

**Endpoint:** `POST /api/token/refresh/`

**Authentication:** Not required

**Request Body:**

```json
{
  "refresh": "string"
}
```

**Response:** `200 OK`

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## Client Endpoints

### 1. List All Clients

Retrieve a paginated list of all clients.

**Endpoint:** `GET /api/clients/`

**Authentication:** Required

**Query Parameters:**

- `page` (optional): Page number for pagination

**Response:** `200 OK`

```json
{
  "count": 100,
  "next": "http://localhost:8000/api/clients/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "first_name": "John",
      "last_name": "Doe",
      "email": "john.doe@example.com",
      "phone": "+1234567890",
      "company": "Acme Corp",
      "stage": "LEAD",
      "created_by_name": "admin",
      "assigned_to_name": "sales_user",
      "created_at": "2025-01-15T10:30:00Z",
      "updated_at": "2025-01-15T10:30:00Z"
    }
  ]
}
```

**Example:**

```bash
curl -X GET http://localhost:8000/api/clients/ \
  -H "Authorization: Bearer <your_token>"
```

### 2. Create a New Client

Add a new client to the CRM.

**Endpoint:** `POST /api/clients/`

**Authentication:** Required

**Request Body:**

```json
{
  "first_name": "string (required)",
  "last_name": "string (required)",
  "email": "string (required, unique)",
  "phone": "string (optional)",
  "company": "string (optional)",
  "address": "string (optional)",
  "notes": "string (optional)",
  "stage": "LEAD | IN_PROGRESS | ACTIVE (optional, default: LEAD)",
  "assigned_to": "integer (optional, user ID)"
}
```

**Response:** `201 Created`

```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone": "+1234567890",
  "company": "Acme Corp",
  "address": "123 Main St, New York, NY",
  "notes": "Interested in premium package",
  "stage": "LEAD",
  "created_by": 1,
  "created_by_name": "admin",
  "assigned_to": 2,
  "assigned_to_name": "sales_user",
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z",
  "interactions": []
}
```

**Example:**

```bash
curl -X POST http://localhost:8000/api/clients/ \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Smith",
    "email": "jane.smith@example.com",
    "company": "Tech Solutions",
    "stage": "LEAD"
  }'
```

### 3. Get Client Details

Retrieve detailed information about a specific client, including all interactions.

**Endpoint:** `GET /api/clients/{id}/`

**Authentication:** Required

**Response:** `200 OK`

```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone": "+1234567890",
  "company": "Acme Corp",
  "address": "123 Main St, New York, NY",
  "notes": "Interested in premium package",
  "stage": "IN_PROGRESS",
  "created_by": 1,
  "created_by_name": "admin",
  "assigned_to": 2,
  "assigned_to_name": "sales_user",
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-20T14:15:00Z",
  "interactions": [
    {
      "id": 1,
      "client": 1,
      "interaction_type": "CALL",
      "subject": "Initial contact",
      "description": "Discussed product features and pricing",
      "created_by": 2,
      "created_by_name": "sales_user",
      "created_at": "2025-01-16T09:00:00Z"
    }
  ]
}
```

**Example:**

```bash
curl -X GET http://localhost:8000/api/clients/1/ \
  -H "Authorization: Bearer <your_token>"
```

### 4. Update Client

Update all fields of an existing client.

**Endpoint:** `PUT /api/clients/{id}/`

**Authentication:** Required

**Request Body:** Same as Create Client (all fields required)

**Response:** `200 OK`

### 5. Partial Update Client

Update specific fields of an existing client.

**Endpoint:** `PATCH /api/clients/{id}/`

**Authentication:** Required

**Request Body:**

```json
{
  "stage": "ACTIVE",
  "notes": "Updated notes"
}
```

**Response:** `200 OK`

**Example:**

```bash
curl -X PATCH http://localhost:8000/api/clients/1/ \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"phone": "+9876543210"}'
```

### 6. Delete Client

Remove a client from the system.

**Endpoint:** `DELETE /api/clients/{id}/`

**Authentication:** Required

**Response:** `204 No Content`

**Example:**

```bash
curl -X DELETE http://localhost:8000/api/clients/1/ \
  -H "Authorization: Bearer <your_token>"
```

### 7. Update Client Stage

Update the onboarding stage of a client and automatically log the change.

**Endpoint:** `PATCH /api/clients/{id}/update_stage/`

**Authentication:** Required

**Request Body:**

```json
{
  "stage": "LEAD | IN_PROGRESS | ACTIVE"
}
```

**Response:** `200 OK`

```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "stage": "ACTIVE",
  "..."
}
```

**Example:**

```bash
curl -X PATCH http://localhost:8000/api/clients/1/update_stage/ \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"stage": "ACTIVE"}'
```

### 8. Get Clients by Stage

Filter clients by their current pipeline stage.

**Endpoint:** `GET /api/clients/by_stage/`

**Authentication:** Required

**Query Parameters:**

- `stage` (optional): LEAD, IN_PROGRESS, or ACTIVE

**Response:** `200 OK` (Returns array of clients)

**Example:**

```bash
curl -X GET "http://localhost:8000/api/clients/by_stage/?stage=LEAD" \
  -H "Authorization: Bearer <your_token>"
```

## Interaction Endpoints

### 1. List All Interactions

Retrieve all client interactions with optional filtering.

**Endpoint:** `GET /api/interactions/`

**Authentication:** Required

**Query Parameters:**

- `client` (optional): Filter by client ID
- `page` (optional): Page number for pagination

**Response:** `200 OK`

```json
{
  "count": 50,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "client": 1,
      "interaction_type": "CALL",
      "subject": "Follow-up call",
      "description": "Discussed contract terms",
      "created_by": 2,
      "created_by_name": "sales_user",
      "created_at": "2025-01-16T09:00:00Z"
    }
  ]
}
```

**Example:**

```bash
# All interactions
curl -X GET http://localhost:8000/api/interactions/ \
  -H "Authorization: Bearer <your_token>"

# Interactions for specific client
curl -X GET "http://localhost:8000/api/interactions/?client=1" \
  -H "Authorization: Bearer <your_token>"
```

### 2. Create Interaction

Log a new interaction with a client.

**Endpoint:** `POST /api/interactions/`

**Authentication:** Required

**Request Body:**

```json
{
  "client": "integer (required, client ID)",
  "interaction_type": "CALL | EMAIL | MEETING | NOTE (required)",
  "subject": "string (required)",
  "description": "string (required)"
}
```

**Response:** `201 Created`

```json
{
  "id": 1,
  "client": 1,
  "interaction_type": "EMAIL",
  "subject": "Proposal sent",
  "description": "Sent detailed proposal for premium package",
  "created_by": 2,
  "created_by_name": "sales_user",
  "created_at": "2025-01-17T11:30:00Z"
}
```

**Example:**

```bash
curl -X POST http://localhost:8000/api/interactions/ \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "client": 1,
    "interaction_type": "MEETING",
    "subject": "Product demo",
    "description": "Demonstrated all product features"
  }'
```

### 3. Get Interaction Details

Retrieve details of a specific interaction.

**Endpoint:** `GET /api/interactions/{id}/`

**Authentication:** Required

**Response:** `200 OK`

### 4. Update Interaction

Update an existing interaction.

**Endpoint:** `PUT /api/interactions/{id}/` or `PATCH /api/interactions/{id}/`

**Authentication:** Required

**Response:** `200 OK`

### 5. Delete Interaction

Remove an interaction record.

**Endpoint:** `DELETE /api/interactions/{id}/`

**Authentication:** Required

**Response:** `204 No Content`

## Statistics Endpoint

### Get CRM Statistics

Retrieve comprehensive statistics and analytics.

**Endpoint:** `GET /api/statistics/`

**Authentication:** Required

**Response:** `200 OK`

```json
{
  "total_clients": 150,
  "clients_by_stage": {
    "lead": 60,
    "in_progress": 45,
    "active": 45
  },
  "recent_clients_30_days": 25,
  "clients_by_staff": {
    "sales_user": 50,
    "sales_manager": 40,
    "admin": 10
  },
  "total_interactions": 320,
  "recent_interactions_30_days": 85,
  "conversion_rate_percentage": 30.0,
  "funnel": {
    "lead": 60,
    "in_progress": 45,
    "active": 45
  }
}
```

**Example:**

```bash
curl -X GET http://localhost:8000/api/statistics/ \
  -H "Authorization: Bearer <your_token>"
```

## User Endpoint

### Get Current User

Retrieve information about the currently authenticated user.

**Endpoint:** `GET /api/me/`

**Authentication:** Required

**Response:** `200 OK`

```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "first_name": "Admin",
  "last_name": "User"
}
```

**Example:**

```bash
curl -X GET http://localhost:8000/api/me/ \
  -H "Authorization: Bearer <your_token>"
```

## Field Constraints

### Client

- `email`: Must be unique and valid email format
- `stage`: Must be one of: LEAD, IN_PROGRESS, ACTIVE
- `first_name`, `last_name`: Maximum 100 characters
- `phone`: Maximum 20 characters
- `company`: Maximum 200 characters

### ClientInteraction

- `interaction_type`: Must be one of: CALL, EMAIL, MEETING, NOTE
- `subject`: Maximum 200 characters
- `client`: Must reference an existing client ID
