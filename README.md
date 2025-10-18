Streamoid Backend — CSV Upload API

A lightweight Django REST API containerized with Docker, designed to upload and parse CSV files and store them into the database.

Features

Upload and parse CSV files via REST API

Store parsed data into a Django model (e.g., Product)

Search, filter, and paginate results

Fully containerized with Docker Compose

API Documentation
Base URL
http://localhost:8000/

1️⃣ Upload CSV

Endpoint:

POST /upload/

Description:
Uploads a CSV file and stores the data into the database.

Request (form-data):

Key	: file	
Type : file	
Description : CSV file to upload

Response(Success):
{
    "stored": number of uploads,
    "failed_count": number of failed counts,
    "failed_rows": []
}

2️⃣ Get Products

Endpoint:

GET /products/

Description:
Fetches all stored records (from CSV upload).

Response(Success):
{
    [
        {
            "id": 1,
            "sku": "TSHIRT-RED-001",
            "name": "Classic Cotton T-Shirt",
            "brand": "StreamThreads",
            "color": "Red",
            "size": "M",
            "mrp": 799,
            "price": 499,
            "quantity": 20
        },
        {
            ...
        },
        ...
    ]
}

⚙️ Setup Instructions

1️⃣ Clone the Repository

git clone https://github.com/<your-username>/streamoid-backend.git
cd streamoid-backend

2️⃣ Build and Run with Docker

docker compose up --build

This will:

Build the Django image
Start the backend container
Run the app at: http://localhost:8000/

🧪 Testing the API

Using Postman

Run the container with docker compose up

Send a POST request to http://localhost:8000/upload/

Attach a CSV file in the form-data body

🧱 Project Structure

streamoid_backend/
│
├── manage.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── streamoid_backend/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── catalog/
    ├── models.py
    ├── views.py
    └── urls.py

🧑‍💻 Author

Parth
📧 [parth.purwar.ece23@itbhu.ac.in
]
