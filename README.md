# JobRad Customer Chat

## Challenge
Imagine a situation where you need to implement a chat software for our customer service to interact with our customers.

**How would the quick win solution look like and how would the state-of-the-art solution look like?**

Implement a simple solution for a chat that enables customers to send messages to customer service.

### Talking points / topics to be considered:

- Which objects / classes would you create?
- How do they interact?
- How does the frontend interact with your classes?
- Which enhancements come to your mind when talking about chat software solutions?


## Init repository over make

For the first setup of the repository, start `make` in the command line from the root directory. The Makefile stored
for this will automatically set up the following preparations for you:

- Initialize the venv directory (based on Python 3.11)
- Update pip
- Installation of pre-commit and autopep8
- Installation of the requirements for function and tests.


## Version 1 - Web-based chat

- [ ] client-server-model over web interface
- - [ ] FastAPI for better websockets integration
- [ ] archiving chats option
  - [ ] automatic archiving of chats after 1 week
- [ ] docker image and container for server, client and database
- [ ] implementation of a relational database (PostgreSQL)
  - from version 4 onwards, AI integration will be based on a chatbot, which will be extended by a knowledge
    database using RAG. (*pgvector*)
- [ ] asynchronous communication for faster data transfer, more scalable, resource-efficient and better for integration
      in later versions with `FastAPI`
- [ ] use of websockets for data exchange and better expandability for version 2 and following
- [ ] saving passwords exclusively encrypted via bcrypt
- [ ] communication encryption via AED
- [ ] preventing SQL injections with prepared statements and SQLAlchemy
- [ ] uuid for users and chats
- [ ] the supporter can select a chat from a list of active chats and join it
- [ ] logs for client errors and server errors are written to separate files under `/var/logs/chat/`
- [ ] when a user logs on to the chat, a session token is created which is valid for 1 hour
  - [ ] this is sent with every message
  - [ ] expansion of the JWT payload
      ```json
      {
         "user_id": "123e4567-e89b-12d3-a456-426614174000",
         "role": "user",
         "exp": 1700000000
      }
      ```
  - [ ] if the token has expired, the user must log in again.
- [ ] `curses` is used for an interactive CLI
- [ ] the client should be able to establish a connection to the server using the following command:
  - `python client.py --server-ip <SERVER-IP-ADDRESS> --role user | supporter`
- [ ] time zone is set to Europe/Berlin to enable standardized time stamps
- [ ] Supporter can take over & end chats

### Database model

- users
  ```postgresql
  CREATE TABLE users (
      id SERIAL PRIMARY KEY,
      uuid UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
      username TEXT NOT NULL,
      role TEXT CHECK (role IN ('user', 'supporter')) NOT NULL,
      password_hash TEXT,
      created_at TIMESTAMP DEFAULT NOW()
  );
  ```

- chats
  ```postgresql
  CREATE TABLE chats (
      id SERIAL PRIMARY KEY,
      user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
      supporter_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
      status TEXT CHECK (status IN ('open', 'assigned', 'closed')) NOT NULL DEFAULT 'open',
      created_at TIMESTAMP DEFAULT NOW(),
      archived_at TIMESTAMP
  );
  ```

- messages
  ```postgresql
  CREATE TABLE messages (
      id SERIAL PRIMARY KEY,
      chat_id INTEGER REFERENCES chats(id) ON DELETE CASCADE,
      sender_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
      content BYTEA NOT NULL,
      timestamp TIMESTAMP DEFAULT NOW()
  );
  ```

- tokens
  ```postgresql
  CREATE TABLE tokens (
      id SERIAL PRIMARY KEY,
      user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
      token TEXT NOT NULL,
      expires_at TIMESTAMP NOT NULL
  );
  ```

- active_chats
  ```postgresql
  CREATE TABLE active_chats (
      id SERIAL PRIMARY KEY,
      chat_id INTEGER REFERENCES chats(id) ON DELETE CASCADE,
      supporter_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
      assigned_at TIMESTAMP DEFAULT NOW()
  );
  ```

- archived_chats
  ```postgresql
  CREATE TABLE archived_chats (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    supporter_id UUID REFERENCES users(id),
    chat_content JSONB,
    archived_at TIMESTAMPTZ DEFAULT NOW()
  );
  ```

## Version 2 - Web-based chat, incl. automatic text module suggestions

- [ ] extension of the database by a table with suggested answers, which can be suggested by the AI depending on
      the weighting.

### Database model

- suggested_replies
  ```postgresql
  CREATE TABLE suggested_replies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    message_id UUID REFERENCES messages(id) ON DELETE CASCADE,
    reply TEXT NOT NULL,
    confidence FLOAT,
    created_at TIMESTAMPTZ DEFAULT NOW()
  );
  ```

## Version 3 - AI-based web chat, incl. RAG knowledge database

- [ ]
