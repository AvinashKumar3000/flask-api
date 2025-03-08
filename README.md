"""
Flask API for user authentication and management.

This API provides endpoints for user signup, login, and deletion using JWT for authentication.

Endpoints:

- POST /signup: Create a new user.

  - Request JSON body:
    - username (str): The username for the new user.
    - password (str): The password for the new user.
  - Responses:
    - 201: User created successfully.
    - 400: Username and password are required, or username already exists.

- POST /login: Authenticate a user and return a JWT token.

  - Request JSON body:
    - username (str): The username of the user.
    - password (str): The password of the user.
  - Responses:
    - 200: Authentication successful, returns a JWT token.
    - 400: Username and password are required.
    - 401: Invalid username or password.

- DELETE /delete: Delete a user account.
  - Request headers:
    - Authorization (str): The JWT token of the authenticated user.
  - Responses:
    - 200: User deleted successfully.
    - 401: Token is required, or invalid/expired token.
    - 404: User not found.

Helper Functions:

- generate_token(user_id): Generate a JWT token for the given user ID.
- verify_token(token): Verify the given JWT token and return the user ID if valid.

In-memory user storage is used for demonstration purposes.
"""

## Testing with Postman:

The repository includes Postman collection and environment files in the `postman` directory:

- `auth_api.postman_collection.json`: Contains all API endpoints
- `auth_api.environment.json`: Contains environment variables

To use:

1. Import both files into Postman
2. Select the "Auth API Environment"
3. The `base_url` is preset to `http://localhost:5000`
4. After login, the `auth_token` will be automatically set for subsequent requests

| Endpoint | Method | Description                          |
| -------- | ------ | ------------------------------------ |
| /signup  | POST   | Create a new user                    |
| /login   | POST   | Authenticate a user and return a JWT |
| /delete  | DELETE | Delete a user account                |
