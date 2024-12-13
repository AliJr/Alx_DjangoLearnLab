# Social Media API

## Setup

1. Install dependencies:
    ```bash
    pip install django djangorestframework djangorestframework-simplejwt
    ```

2. Set up the project:
    ```bash
    django-admin startproject social_media_api
    cd social_media_api
    python manage.py startapp accounts
    ```

3. Add `rest_framework` and `accounts` to `INSTALLED_APPS` in `settings.py`.

4. Run migrations:
    ```bash
    python manage.py migrate
    ```

5. Start the server:
    ```bash
    python manage.py runserver
    ```

## API Endpoints


### Acocounts
- **POST /api/accounts/register/**: Register a new user.
- **POST /api/accounts/login/**: Log in and get a token.
- **GET /api/accounts/profile/**: Get the profile information of the logged-in user (authenticated).

### Posts

- **GET /api/posts/**: List all posts.
- **POST /api/posts/**: Create a new post. **Requires authentication**.
  - **Body**: `{"title": "Post Title", "content": "Post content"}`
- **GET /api/posts/{id}/**: Retrieve a post by ID.
- **PUT /api/posts/{id}/**: Update a post. **Requires authentication**.
  - **Body**: `{"title": "Updated Title", "content": "Updated content"}`
- **DELETE /api/posts/{id}/**: Delete a post. **Requires authentication**.

### Comments

- **GET /api/comments/**: List all comments.
- **POST /api/comments/**: Create a new comment. **Requires authentication**.
  - **Body**: `{"post": 1, "content": "This is a comment"}`
- **GET /api/comments/{id}/**: Retrieve a comment by ID.
- **PUT /api/comments/{id}/**: Update a comment. **Requires authentication**.
  - **Body**: `{"content": "Updated comment"}`
- **DELETE /api/comments/{id}/**: Delete a comment. **Requires authentication**.


## User Model

- `bio`: Text field for user biography.
- `profile_picture`: Image field for profile picture.
- `followers`: Many-to-many self-reference for user followers.

