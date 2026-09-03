# OllamaBridge

**OllamaBridge** is a general-purpose LLM chat application built with Python, FastAPI, PostgreSQL, SQLAlchemy, and Ollama.

The application provides an authenticated conversational interface where users can interact with a Llama language model. Conversations and messages are persisted in PostgreSQL, allowing the chatbot to maintain context from previous messages within the same conversation thread.

The project focuses on building an API-driven LLM application with authentication, database persistence, request validation, rate limiting, and a Streamlit frontend.

---

## ✨ Features

* User signup and login
* JWT-based authentication
* Protected chat endpoint
* General-purpose AI chatbot
* Llama integration through Ollama
* Conversation context within the same thread
* Persistent conversation and message storage
* PostgreSQL database
* SQLAlchemy ORM
* Pydantic data validation
* Rate limiting of **5 requests per minute**
* Streamlit-based frontend
* REST API built with FastAPI

> **Current limitation:** OllamaBridge currently supports a single conversation thread and does not yet provide multiple independent conversations.

---

## 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │      User           │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Streamlit Frontend │
                         └──────────┬──────────┘
                                    │
                              HTTP Requests
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │       FastAPI       │
                         │                     │
                         │  Authentication     │
                         │  JWT Authorization  │
                         │  Chat API           │
                         │  Request Validation │
                         │  Rate Limiting     │
                         └──────┬────────┬─────┘
                                │        │
                    ┌───────────┘        └────────────┐
                    │                                  │
                    ▼                                  ▼
          ┌──────────────────┐               ┌─────────────────┐
          │    PostgreSQL    │               │     Ollama      │
          │                  │               │                 │
          │ Users            │               │ Llama           │
          │ Conversations    │               │ Language Model  │
          │ Messages         │               │                 │
          └──────────────────┘               └─────────────────┘
```

### Request Flow

```text
User
  │
  ▼
Streamlit
  │
  ▼
POST /chat
  │
  ▼
JWT Authentication
  │
  ▼
Retrieve conversation context
  │
  ▼
Ollama + Llama
  │
  ▼
Generate response
  │
  ▼
Store message and response
  │
  ▼
Return response to Streamlit
```

---

## 🛠️ Tech Stack

| Technology     | Purpose                          |
| -------------- | -------------------------------- |
| **Python**     | Backend programming language     |
| **FastAPI**    | REST API framework               |
| **Uvicorn**    | ASGI server                      |
| **PostgreSQL** | Relational database              |
| **SQLAlchemy** | ORM and database interaction     |
| **Pydantic**   | Request and response validation  |
| **JWT**        | Authentication and authorization |
| **Ollama**     | Local LLM serving                |
| **Llama**      | Language model                   |
| **Streamlit**  | Frontend interface               |

---

## 📁 Project Structure

```text
OllamaBridge/
│
├── db/
│   ├── connections.py       # PostgreSQL database connection
│   └── models.py            # SQLAlchemy database models
│
├── routes/
│   ├── auth.py              # Signup and authentication routes
│   ├── oauth2.py            # OAuth2/JWT authentication logic
│   ├── olllamaAPI.py        # Ollama and LLM integration
│   └── user.py              # User-related functionality
│
├── app.py                   # Application-level functionality
├── main.py                  # FastAPI application setup
├── models.py                # Pydantic models
├── utility.py               # Utility/helper functions
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
├── .gitignore               # Git ignored files
└── README.md                # Project documentation
```

---

## 🔐 Authentication

OllamaBridge uses **JWT-based authentication** to protect access to the chatbot.

The authentication flow is:

```text
┌──────────────┐
│     User     │
└──────┬───────┘
       │
       │ Signup
       ▼
┌─────────────────┐
│     FastAPI     │
└────────┬────────┘
         │
         ▼
    PostgreSQL
         │
         │
       Login
         │
         ▼
┌─────────────────┐
│ Validate User   │
│ Credentials     │
└────────┬────────┘
         │
         ▼
    JWT Token
         │
         ▼
┌─────────────────┐
│ Protected Chat  │
│    Endpoint     │
└─────────────────┘
```

After a successful login, the application generates a JWT token. The token is then used to authenticate requests to protected endpoints.

---

## 🗄️ Database

PostgreSQL is used to persist application data, with SQLAlchemy providing the ORM layer.

The current database consists of three primary entities:

```text
User
 │
 └────── Conversation
             │
             └────── Message
```

### User

Stores registered user information and authentication-related data.

### Conversation

Represents the user's current conversation thread.

### Message

Stores messages exchanged between the user and the LLM.

The stored messages are used to provide previous conversation context to the Llama model, allowing the chatbot to maintain continuity within the same thread.

---

## 🤖 LLM Integration

OllamaBridge uses **Ollama** to run the Llama language model locally.

The FastAPI backend communicates with Ollama to generate responses:

```text
FastAPI
   │
   ▼
Ollama
   │
   ▼
Llama
   │
   ▼
Generated Response
```

When a user sends a message, the backend can retrieve the existing conversation context from PostgreSQL and provide it to the LLM along with the new message.

The generated response is then returned to the frontend and persisted in the database.

---

## 🔌 API Endpoints

OllamaBridge currently exposes three primary API endpoints.

| Method | Endpoint  | Description                                                   | Authentication |
| ------ | --------- | ------------------------------------------------------------- | -------------- |
| `POST` | `/signup` | Creates a new user account                                    | No             |
| `POST` | `/login`  | Authenticates a user and returns a JWT token                  | No             |
| `POST` | `/chat`   | Sends a message to the LLM and returns the generated response | JWT Required   |

### `/signup`

Creates a new user account.

```text
POST /signup
```

The submitted user information is validated using Pydantic and stored in PostgreSQL.

### `/login`

Authenticates an existing user.

```text
POST /login
```

After successful authentication, the API returns a JWT token that can be used to access protected endpoints.

### `/chat`

Sends a user message to the chatbot.

```text
POST /chat
```

The endpoint:

1. Validates the user's JWT token.
2. Retrieves the relevant conversation context.
3. Sends the context and new message to Ollama.
4. Receives the Llama-generated response.
5. Stores the conversation data in PostgreSQL.
6. Returns the response to the client.

---

## 🚦 Rate Limiting

OllamaBridge currently limits requests to:

```text
5 requests per minute
```

This provides basic protection against excessive requests and helps control the number of requests sent to the locally hosted LLM.

---

## 🖥️ Frontend

The frontend is built using **Streamlit**.

The interface provides the user with a simple way to:

* Sign up
* Log in
* Authenticate with the backend
* Send messages
* Receive LLM responses
* Continue a conversation within the same thread

The Streamlit application communicates with the FastAPI backend through HTTP requests.

The frontend does not directly access PostgreSQL or Ollama.

---

## ⚙️ Environment Variables

OllamaBridge uses environment variables to keep configuration and sensitive information outside the source code.

Create a `.env` file containing the required configuration.

Example:

```env
DATABASE_URL=your_postgresql_connection_string
SECRET_KEY=your_jwt_secret
OLLAMA_URL=http://localhost:11434
EXPIRE_IN=30
```

### Environment Variable Description

| Variable       | Description                        |
| -------------- | ---------------------------------- |
| `DATABASE_URL` | PostgreSQL connection string       |
| `SECRET_KEY`   | Secret used for JWT authentication |
| `OLLAMA_URL`   | URL of the local Ollama server     |
| `EXPIRE_IN`    | JWT expiration time in minutes     |

### Security

The actual `.env` file should **never be committed to GitHub**.

A `.env.example` file can be committed instead:

```env
DATABASE_URL=
SECRET_KEY=
OLLAMA_URL=http://localhost:11434
EXPIRE_IN=30
```

---

## 🚀 Installation

### Prerequisites

Before running OllamaBridge, make sure you have:

* Python 3.x
* PostgreSQL
* Ollama
* Git

You will also need the Llama model configured in Ollama.

---

### 1. Clone the Repository

```bash
git clone <repository-url>
cd OllamaBridge
```

---

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment.

#### Windows

```bash
venv\Scripts\activate
```

#### macOS/Linux

```bash
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure PostgreSQL

Create a PostgreSQL database and configure the connection string in your `.env` file.

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
```

---

### 5. Configure Ollama

Install and start Ollama, then make sure the required Llama model is available locally.

The application expects Ollama to be accessible at:

```text
http://localhost:11434
```

---

### 6. Configure Environment Variables

Create a `.env` file:

```env
DATABASE_URL=your_postgresql_connection_string
SECRET_KEY=your_secret_key
OLLAMA_URL=http://localhost:11434
EXPIRE_IN=30
```

---

## ▶️ Running the Application

### Start the FastAPI Backend

Run:

```bash
uvicorn main:app --reload
```

The FastAPI application will then be available locally.

### Start the Streamlit Frontend

Run:

```bash
streamlit run app.py
```

The Streamlit interface will open in your browser.

---

## 💬 Example Usage

A typical interaction with OllamaBridge follows this flow:

```text
1. User signs up
       ↓
2. Account is stored in PostgreSQL
       ↓
3. User logs in
       ↓
4. FastAPI validates credentials
       ↓
5. JWT token is generated
       ↓
6. User sends a message
       ↓
7. JWT is validated
       ↓
8. Previous conversation context is retrieved
       ↓
9. Context + new message are sent to Ollama
       ↓
10. Llama generates a response
       ↓
11. Message and response are stored
       ↓
12. Response is displayed in Streamlit
```

---



---

## 🔮 Future Improvements

Potential improvements planned for future versions include:

* Multiple conversation threads
* Conversation history management
* Creating and deleting conversations
* Conversation naming
* Streaming LLM responses
* Support for additional LLM models
* Automated testing
* Docker containerization
* CI/CD pipeline
* Cloud deployment
* Improved frontend functionality
* More advanced rate limiting

---

## 🤝 AI-Assisted Development

AI tools were used during development to assist with the design and implementation of the Streamlit frontend.

The project was developed with a focus on understanding and implementing the backend architecture, authentication, database persistence, API design, and LLM integration.

AI assistance was used as a development aid for areas where additional guidance was needed, particularly frontend development with Streamlit.

---

## 📌 Project Status

**MVP / Active Development**

OllamaBridge currently provides:

* User signup
* User login
* JWT authentication
* LLM-powered chat
* Conversation persistence
* PostgreSQL integration
* Ollama + Llama integration
* Streamlit frontend
* Basic request rate limiting

Multiple conversation support and additional production-oriented features are planned for future iterations.

---

## 📄 License

This project is intended for educational and portfolio purposes.
