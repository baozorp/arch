 **# FastAPI Users API**

**Version:** 0.1.0

**Description:** This API provides endpoints for managing user data.

## Endpoints

### Users

**Find By Name**

* **GET** /api/users/find_by_name
* **Parameters:**
    * first_name (string): The first name of the user.
    * second_name (string): The second name of the user.
* **Responses:**
    * 200: Successful Response
    * 422: Validation Error

**Find By Login**

* **GET** /api/users/find_by_login
* **Parameters:**
    * login (string): The login of the user.
* **Responses:**
    * 200: Successful Response
    * 422: Validation Error

**Get User Info**

* **GET** /api/users/user_info
* **Parameters:**
    * id (integer): The ID of the user.
* **Responses:**
    * 200: Successful Response
    * 422: Validation Error

**New User**

* **POST** /api/users/new_user
* **Request Body:**
    ```json
    {
        "user_name": string,
        "first_name": string,
        "second_name": string,
        "password": string
    }
    ```
* **Responses:**
    * 200: Successful Response
    * 422: Validation Error

**Update User**

* **PUT** /api/users/update
* **Parameters:**
    * user_id (integer): The ID of the user to update.
* **Request Body:**
    ```json
    {
        "user_name": string,
        "first_name": string,
        "second_name": string,
        "password": string
    }
    ```
* **Responses:**
    * 200: Successful Response
    * 422: Validation Error

**Delete User**

* **DELETE** /api/users/delete
* **Parameters:**
    * user_id (integer): The ID of the user to delete.
* **Responses:**
    * 200: Successful Response
    * 422: Validation Error

## Error Responses

**HTTPValidationError:**

* **Description:** Indicates a validation error in the request body.
* **Schema:**
    ```json
    {
        "detail": [
            {
                "loc": [string, ...],
                "msg": string,
                "type": string
            }
        ]
    }
    ```

**ValidationError:**

* **Description:** Represents a single validation error.
* **Schema:**
    ```json
    {
        "loc": [string, ...],
        "msg": string,
        "type": string
    }
    ```

## Additional Information

* **Base URL:** [To be provided]
* **Authentication:** [To be provided]
* **OpenAPI specification:** [To be provided]
