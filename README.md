If you're using PostgreSQL for your Expense Tracker API, you'll need to update your `README.md` to reflect the PostgreSQL setup. Here’s how you can include PostgreSQL-specific instructions:

### Updated `README.md` for PostgreSQL

```markdown
# Expense Tracker API

A simple REST API created using FastAPI and PostgreSQL.

## Run Locally

### Clone the Project

```bash
git clone https://github.com/meghanabv05/expensetracker.git
```

### Go to the Project Directory

```bash
cd expensetracker
```

### Set Up the Environment

Create a `.env` file in the project root and add the necessary configuration. For PostgreSQL, you need to specify the database URL. For example:

```env
DATABASE_HOST="YOUR_DATABASE_HOST"
DATABASE_PORT="YOUR_DATABASE_PORT"
DATABASE_PASSWORD="YOUR_DATABASE_PASSWORD"
DATABASE_NAME="YOUR_DATABASE"
DATABASE_USERNAME="YOUR_DATABASE_USERNAME"
SECRET_KEY="YOUR_SECRET_KEY"
ALGORITHM="ALGORITHM"
ACCESS_TOKEN_EXPIRE_MINUTES="YOUR_ACCESS_TOKEN_EXPIRE_MINUTES"
```

Replace `username`, `password`, `localhost`, and `expense_tracker` with your actual PostgreSQL username, password, host, and database name, secrete-key, algorithm, access token expire minutes

### Install Dependencies

Ensure you have Python and `pip` installed, then install the project dependencies:

```bash
pip install -r requirements.txt
```

### Create the Database

Create a database in PostgreSQL:

1. Open the PostgreSQL command line or a database management tool.
2. Run the following SQL command to create the database:

   ```sql
   CREATE DATABASE expense_tracker;
   ```

### Build and Run the App

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The app will start running at [http://localhost:8000](http://localhost:8000).

## Swagger - API Documentation

You can explore the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs) (UI format) or [http://localhost:8000/redoc](http://localhost:8000/redoc) (JSON format).

## Explore REST APIs

### User Authentication

| Method | URL                   | Description | Return             |
|--------|-----------------------|-------------|--------------------|
| POST   | /users/register/      | Sign-up     | JSON Web Token     |
| POST   | /users/login/         | Login       | JSON Web Token     |

### Categories

| Method | URL                        | Description                          | Return                  |
|--------|----------------------------|--------------------------------------|-------------------------|
| GET    | /categories/               | Get all categories                   | Array of JSON objects   |
| GET    | /categories/{id}           | Get a category by id                 | Single JSON object      |
| POST   | /categories/               | Create a new category                | Created JSON object     |
| PUT    | /categories/{id}           | Update an existing category          | Updated JSON object     |
| DELETE | /categories/{id}           | Delete a category                    | Success message         |

### Transactions

| Method | URL                                | Description                                       | Return                  |
|--------|------------------------------------|---------------------------------------------------|-------------------------|
| GET    | /categories/{cid}/transactions/    | Get all transactions of category "cid"           | Array of JSON objects   |
| GET    | /categories/{cid}/transactions/{tid} | Get a single transaction by "tid" of category "cid" | Single JSON object      |
| POST   | /categories/{cid}/transactions/    | Insert a new transaction for category "cid"      | Created JSON object     |
| PUT    | /categories/{cid}/transactions/{tid} | Update an existing transaction                   | Updated JSON object     |
| DELETE | /categories/{cid}/transactions/{tid} | Delete a transaction                            | Success message         |

**NOTE:** The endpoints of "Categories" and "Transactions" are restricted. To access these endpoints, use the token generated after logging in as the value of the Bearer in the Authorization header as follows: `"Authorization: Bearer Token_id"`

## Sample Request Body

### User - Register

```json
{
  "firstName": "Thomas",
  "lastName": "Shelby",
  "email": "shelby@gmail.com",
  "password": "test123"
}
```

### User - Login

```json
{
  "email": "shelby@gmail.com",
  "password": "test123"
}
```

### Categories

```json
{
  "title": "Shopping",
  "description": "All shopping expenses in xyz mall"
}
```

### Transactions

```json
{
  "amount": 4000,
  "note": "Spent higher than last time",
  "transactionDate": "2024-08-18"
}
```
```

### Key Points to Note:
- **Database URL:** The `DATABASE_URL` format for PostgreSQL is `postgresql://username:password@localhost:5432/database_name`.
- **Database Creation:** You need to manually create the PostgreSQL database as shown.
- **Configuration:** Ensure that your `.env` file contains accurate details for your PostgreSQL setup.

If you need further details or adjustments, let me know!
