# Movie Rating Project

This is a comprehensive movie management system that allows users to log in, view movies, create new movies, update existing ones, and rate them. The project also includes an admin role to manage reported movies.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Project Structure](#project-structure)
3. [Dependencies](#dependencies)
4. [API Endpoints](#api-endpoints)
5. [API Endpoint Documentation](#api-endpoint-documentation)
6. [Contributing](#contributing)

## Getting Started

To get started with this project, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/noman62/movie_rating_project.git
   ```

2. **Install dependencies**:
   ```bash
   cd movie-rating-project
   pip install -r requirements.txt
   ```

3. **Run database migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Create a superuser (admin)**:
   ```bash
   python manage.py createsuperuser
   ```

5. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

The project should now be running at `http://localhost:8000`.

## Project Structure

The project's folder structure is as follows:
```
MOVIE_RATING_PROJECT/
│
├── requirements.txt            # Lists the project's dependencies
├── manage.py                  # Command-line utility for administrative tasks
│
├── movie_project/            # Project configuration directory
│   ├── __init__.py          # Indicates that this directory is a Python package
│   ├── settings.py          # Contains settings and configurations for the Django project
│   ├── urls.py              # URL routing for the project
│   ├── wsgi.py              # Entry point for WSGI-compatible web servers
│   └── asgi.py              # Entry point for ASGI-compatible web servers
│
├── movies/                   # Main application directory for movie rating functionality
│   ├── __init__.py          # Indicates that this directory is a Python package
│   ├── apps.py              # Application configuration for the 'movies' app
│   ├── models.py            # Database models defining the structure of movie-related data
│   ├── views.py             # Contains the view logic for handling requests and responses
│   ├── urls.py              # URL routing specific to the 'movies' app
│   └── serializers.py       # Serializers for converting complex data types to JSON and vice versa
```

## Dependencies
Make sure to install the required dependencies by running `pip install -r requirements.txt`.

## API Endpoints

The project exposes the following API endpoints:

### Authentication
- `POST /api/auth/login`: Login with username/email and password

### Movie Management
- `POST /api/movies/`: Add a new movie
- `GET /api/movies/`: Get all movie list
- `PUT /api/movies/{id}`: Update the information of an existing movie by its ID

### Movie Ratings
- `POST /api/ratings/`: Submit a rating for a movie by its ID
- `GET /api/ratings/{id}/`: Retrieve the rating for a specific movie by its ID
- `PUT /api/ratings/{id}/`: Modify the rating for a movie by its ID
- `GET /api/ratings/`: Retrieve all ratings for movies

### Movie Reporting
- `POST /api/reports/`: Submit a report for a movie
- `GET /api/reports/`: Retrieve a list of all movie reports
- `GET /api/reports/{id}`: Retrieve details of a single movie report by its ID

### Admin Access
- `GET /api/admin/reports/`: Retrieve all movie reports for admin access
- `GET /api/admin/reports/{id}/resolve/`: Retrieve and mark a specific movie report as resolved

Note: All endpoints except `/login` require authentication. The admin-specific endpoints are only accessible to users with the admin role.

## API Endpoint Documentation

This document provides a comprehensive overview of the API endpoints available in the application.

### Authentication

#### Register User
**Endpoint**: `POST /api/auth/register/`  
**Description**: Create a new user account.  
**Request Body**:
```json
{
    "email": "user@example.com",
    "username": "user123",
    "password": "your_password"
}
```
**Response**:
```json
{
    "status": "success",
    "data": {
        "user": {
            "id": 1,
            "username": "user123",
            "email": "user@example.com"
        },
        "tokens": {
            "refresh": "refresh_token_string",
            "access": "access_token_string"
        }
    }
}
```

#### Login User
**Endpoint**: `POST /api/auth/login/`  
**Description**: Authenticate a user and receive access/refresh tokens.  
**Request Body**:
```json
{
    "email": "user@example.com",
    "password": "your_password"
}
```
**Response**:
```json
{
    "status": "success",
    "data": {
        "user": {
            "id": 1,
            "username": "user123",
            "email": "user@example.com"
        },
        "tokens": {
            "refresh": "refresh_token_string",
            "access": "access_token_string"
        }
    }
}
```

### Movies

#### List Movies
**Endpoint**: `GET /api/movies/`  
**Description**: Retrieve a list of all movies.  
**Response**:
```json
[
    {
        "id": 1,
        "title": "Movie 1",
        "description": "Description of Movie 1",
        "released_at": "2023-04-01",
        "duration": 120,
        "genre": "Drama",
        "language": "English",
        "created_by": "user123",
        "avg_rating": 4.5,
        "total_ratings": 10,
        "created_at": "2023-04-01T10:00:00Z",
        "updated_at": "2023-04-01T10:00:00Z"
    },
    {
        "id": 2,
        "title": "Movie 2",
        "description": "Description of Movie 2",
        "released_at": "2023-05-01",
        "duration": 90,
        "genre": "Comedy",
        "language": "English",
        "created_by": "user456",
        "avg_rating": 3.8,
        "total_ratings": 20,
        "created_at": "2023-05-01T12:00:00Z",
        "updated_at": "2023-05-01T12:00:00Z"
    }
]
```

#### Create Movie
**Endpoint**: `POST /api/movies/`  
**Description**: Create a new movie.  
**Request Body**:
```json
{
    "title": "New Movie",
    "description": "Description of the new movie",
    "released_at": "2023-06-01",
    "duration": 110,
    "genre": "Action",
    "language": "English"
}
```
**Response**:
```json
{
    "id": 3,
    "title": "New Movie",
    "description": "Description of the new movie",
    "released_at": "2023-06-01",
    "duration": 110,
    "genre": "Action",
    "language": "English",
    "created_by": "user123",
    "avg_rating": 0.0,
    "total_ratings": 0,
    "created_at": "2023-06-01T08:00:00Z",
    "updated_at": "2023-06-01T08:00:00Z"
}
```

#### Rate a Movie
**Endpoint**: `POST /api/ratings/`  
**Description**: Rate a movie.  
**Request Body**:
```json
{
    "id": 2,
    "movie": 1
}
```
**Response**:
```json 
{
    "id": 2,
    "movie": 1,
    "user": "raisa",
    "rating": 1,
    "created_at": "2024-11-05T11:03:42.597918Z"
}
```

#### Retrieve all ratings for movies
**Endpoint**: `GET /api/ratings/`  
**Description**: Retrieve all ratings for movies  
**Response**:
```json 
[
    {
        "id": 1,
        "movie": 2,
        "user": "raisa",
        "rating": 5,
        "created_at": "2024-11-05T09:56:49.391523Z"
    },
    {
        "id": 2,
        "movie": 1,
        "user": "raisa",
        "rating": 1,
        "created_at": "2024-11-05T11:03:42.597918Z"
    }
]
```

#### Retrieve the rating for a specific movie by its ID
**Endpoint**: `POST /api/ratings/`  
**Description**: Retrieve the rating for a specific movie by its ID.  
**Response**:
```json 
{
    "id": 1,
    "movie": 2,
    "user": "raisa",
    "rating": 5,
    "created_at": "2024-11-05T09:56:49.391523Z"
}
```

#### Modify the rating for a movie by its ID
**Endpoint**: `PUT /api/ratings/{id}/`  
**Description**: Modify the rating for a movie by its ID.  
**Request Body**:
```json
{
    "movie": 2,
    "rating": 3
}
```
**Response**:
```json 
{
    "id": 1,
    "movie": 2,
    "user": "raisa",
    "rating": 3,
    "created_at": "2024-11-05T09:56:49.391523Z"
}
```

### Reporting

#### Report a Movie
**Endpoint**: `POST /api/reports/`  
**Description**: Report a movie.  
**Request Body**:
```json
{
    "movie": 1,
    "reason": "NOT GOOD"
}
```
**Response**:
```json
{
    "id": 3,
    "movie": 1,
    "movie_title": "my name is khan",
    "reported_by": "raisa",
    "reason": "NOT GOOD",
    "created_at": "2024-11-05T18:09:59.558633Z",
    "resolved": false,
    "resolved_at": null,
    "admin_notes": ""
}
```

#### View Reports (User)
**Endpoint**: `GET /api/reports/`  
**Description**: View the reports created by the current user.  
**Response**:
```json
[
   {
    "id": 3,
    "movie": 1,
    "movie_title": "my name is khan",
    "reported_by": "raisa",
    "reason": "NOT GOOD",
    "created_at": "2024-11-05T18:09:59.558633Z",
    "resolved": false,
    "resolved_at": null,
    "admin_notes": ""
   }
]
```

#### Retrieve details of a single movie report by its ID
**Endpoint**: `GET /api/reports/{id}`  
**Description**: Retrieve details of a single movie report by its ID.  
**Response**:
```json
{
    "id": 1,
    "movie": 1,
    "movie_title": "my name is khan",
    "reported_by": "raisa",
    "reason": "Inappropriate content",
    "created_at": "2024-11-05T12:12:05.425014Z",
    "resolved": true,
    "resolved_at": "2024-11-05T12:30:13.880096Z",
    "resolved_by": "haron",
    "admin_notes": "Action taken: Content reviewed and found appropriate"
}
```

#### View Reports (Admin)
**Endpoint**: `GET /api/admin/reports/`  
**Description**: View all reports (admin access required). Admins must log in with their email and password to receive an authorization token.  
**Response**:
```json
[
    {
        "id": 3,
        "movie": 1,
        "movie_title": "my name is khan",
        "reported_by": "raisa",
        "reason": "NOT GOOD",
        "created_at": "2024-11-05T18:09:59.558633Z",
        "resolved": false,
        "resolved_at": null,
        "admin_notes": ""
    },
    {
        "id": 2,
        "movie": 2,
        "movie_title": "Example Movie Title",
        "reported_by": "raisa",
        "reason": "not good",
        "created_at": "2024-11-05T12:13:22.988239Z",
        "resolved": false,
        "resolved_at": null,
        "admin_notes": ""
    }
]
```

#### Resolve a Report (Admin)
**Endpoint**: `POST /api/admin/reports/{id}/resolve/`  
**Description**: Resolve a report (admin access required).  
**Request Body**:
```json
{
    "action": "resolve",
    "notes": "Content reviewed and found appropriate"
}
```
**Response**:
```json
{
    "status": "success",
    "message": "Report resolved successfully",
    "data": {
        "id": 1,
        "movie": 1,
        "movie_title": "Movie 1",
        "reported_by": "user123",
        "reason": "Inappropriate content",
        "created_at": "2023-06-01T09:00:00Z",
        "resolved": true,
        "resolved_at": "2023-06-03T16:00:00Z",
        "resolved_by": "admin_user",
        "admin_notes": "Content reviewed and found appropriate"
    }
}
```

#### Get Reporting Statistics (Admin)
**Endpoint**: `GET /api/admin/reports/statistics/`  
**Description**: Retrieve reporting statistics (admin access required).  
**Response**:
```json
{
    "total_reports": 2,
    "pending_reports": 1,
    "resolved_reports": 1,
    "resolution_rate": "50.00%"
}
```

Please note that the access token obtained from the login endpoint needs to be included in the `Authorization` header for all authenticated requests (e.g., `Authorization: Bearer access_token_string`).

## Contributing

If you would like to contribute to this project, please follow the standard GitHub workflow:
1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Commit your changes
4. Push your branch to your forked repository
5. Submit a pull request
