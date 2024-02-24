# Book Management System

## Overview

This is a Book Management System built with Django, utilizing Docker and Docker Compose for easy deployment.

## Setup

1. Clone the repository:

   git clone <repository_url>
   cd <repository_directory>

# Build and run the Docker containers:

  docker-compose up --build

# Access the application at 
  
  http://localhost:8000



## API Endpoints

  # Authentication

  POST http://127.0.0.1:8000/create_user/

  sample request body:

  {
    "username": "John",
    "password": "12345678"
  }

  # Token generation

  POST http://127.0.0.1:8000/api/token/

  sample:

  {
    "username": "John",
    "password": "12345678"
  }

  after successful authentication we will get the Auth token

  sample response:

  {
    "token": "8308c91023781986c518af79e8e4dfce4232be7f"
  }


  # Add token in the Authorization headers for authentication.

  key: Authorization   value: Token 8308c91023781986c518af79e8e4dfce4232be7f



  # Authors

  GET /authors/

  Retrieve a list of all authors.

  GET /authors/{author_id}/books/

  Retrieve a list of books written by a specific author.

  POST /authors/

  Create a new author. Provide the author's name and user relation in the request body.

  sample:

  {
    "user": 1,
    "name": "John Doe"
  }


# Books

  GET /books/

  Retrieve a list of all books.

  GET /books/{book_id}/reviews/

  Retrieve a list of reviews for a specific book.

  POST /books/

  Create a new book. Provide the book's title and author ID in the request body.


  Sample Input:

  {
  "title": "The Art of Programming",
  "author": 1
  }


# Reviews

  GET /reviews/

  Retrieve a list of all reviews.

  POST /reviews/

  Create a new review. Provide the rating, comment, author ID, and book ID in the request body.

  Sample Input:

  {
  "rating": 4.5,
  "comment": "Great read!",
  "author": 1,
  "book": 1
  }

