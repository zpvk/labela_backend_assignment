# Auto API Assignment

# Developer Local and Docker Setup ⚙️

## Requirements
- Python 3.8 or higher
- PostgreSQL (for local setup)
- Docker (for Docker setup)
- Docker Compose (for Docker setup)

## 🧑‍💻 Developer Local Setup 

### Step 1: Clone the Repository
```
git clone https://github.com/zpvk/labela_backend_assignment.git
cd your-repository
```
### Step 2: Create a Virtual Environment (Optional but recommended)
```
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```
### Step 3: Install Dependencies
```
pip install -r requirements.txt
```
### Step 4: Set Environment Variables
Create a `.env` file in the project root and add the following variables:
```
DEBUG=True
SECRET_KEY=my_secret_key
DB_NAME=my_database
DB_USER=my_user
DB_PASSWORD=my_password
DB_HOST=localhost
DB_PORT=5432
```

### Step 5: Run PostgreSQL Server (If not using Docker)
Make sure your PostgreSQL server is running, and the database and user specified in the `.env` file are created.

### Step 6: Apply Migrations
```
python manage.py makemigrations
python manage.py migrate
```
### Step 7: Create a Superuser (for accessing the admin panel)
```
python manage.py createsuperuser
```
### Step 8: Run the Development Server
```
python manage.py runserver
```

## 🧑‍💻 Developer Docker Setup

### Repeat Steps 1-2 for Cloning the Repository

### Step 3: Run Docker Compose
```
docker-compose up -d
```
### Step 4: Create Admin user
```
docker compose run web python manage.py createsuperuser
```

## User Stories and API Endpoints
### Access Swagger UI For Quick View Endpoints
I have also implemented Swagger, but it is not automatically generated with the Swagger library. Instead, I have integrated it using the Postman collection. Kindly utilize Postman for API testing
Visit http://localhost:8000/api/swagger-ui/ to explore the implemented API endpoints.

### API Test Postman 
For testing the endpoint, please utilize the Postman collection JSON available in the repository named `AutoCompany.postman_collection.json` The mentioned endpoints are outlined below.

1. User Registration and Token Retrieval
    - Endpoint: `/register`
    - Method: POST
    - Request Body:
      ``` 
        {   
            "email: "your@email.com",
            "username": "your_username",
            "password": "your_password"
        }
      ```

2. Company - Add Products to Database
    - Endpoint: `/api/admin/products`
    - Method: POST
    - Requires authentication: Yes (Admin)
    - Request Body: Include product details

3. Client - Add Product to Shopping Cart
    - Endpoint: `/api/cart/add`
    - Method: POST
    - Requires authentication: Yes (User)
    - Request Body: Include product details

4. Client - Remove Product from Shopping Cart
    - Endpoint: `/api/cart/remove/<id>`
    - Method: DELETE
    - Requires authentication: Yes (User)

5. Client - Order Products in Shopping Cart with Select Delivery Date and Time
    - Endpoint: `/api/checkout`
    - Method: POST
    - Requires authentication: Yes
    - Request Body: Include delivery date (User)

7. Client - View All Products (pagination page number with page size limit)
    - Endpoint: `/api/products/?page= &page_size= `
    - Method: GET
    - Requires authentication: No

8. Client - View Details of a Product
    - Endpoint: `/api/products/<id>`
    - Method: GET
    - Requires authentication: No
