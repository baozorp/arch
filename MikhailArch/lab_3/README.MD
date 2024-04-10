 # Chat API Methods

This API provides endpoints for managing chats and their data.

## Available Methods:

1. Retrieve a Chat:
   - Endpoint: `GET /chat/{chat_id}`
   - Purpose: Fetch details of a specific chat.
   - Parameters:
     - `chat_id`: The unique ID of the chat to retrieve.
   - Response: Returns the chat data as a JSON object, or a 404 error if the chat is not found.

2. Create a Chat:
   - Endpoint: `POST /chat`
   - Purpose: Create a new chat.
   - Request Body: A JSON object containing the chat details, structured as a `ChatModel` object.
   - Response:  Returns a JSON object with a `chat_id` property indicating the newly created chat's unique ID.

3. Change Chat Name:
   - Endpoint: `PUT /chat/{chat_id}/name`
   - Purpose: Update the name of an existing chat.
   - Parameters:
     - `chat_id`: The unique ID of the chat to update.
     - `name`: The new name to assign to the chat.
   - Response: Returns a success message if the name is updated successfully, or a 404 error if the chat is not found.

4. Add Message to a Chat:
   - Endpoint: `POST /chat/{chat_id}/message`
   - Purpose: Post a new message to a chat.
   - Parameters:
     - `chat_id`: The unique ID of the chat to receive the message.
     - `message`: A JSON object representing the message, structured as a `Message` object.
   - Response: Returns a success message if the message is added successfully, or a 404 error if the chat is not found.

5. Add Member to a Chat:
   - Endpoint: `POST /chat/{chat_id}/member`
   - Purpose: Add a new member to a chat.
   - Parameters:
     - `chat_id`: The unique ID of the chat to which the member will be added.
     - `member`: The identifier of the member to be added (e.g., user ID).
   - Response: Returns a success message if the member is added successfully, or a 404 error if the chat is not found.
