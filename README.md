# Vendor Management System
A RESTful API for managing vendors and tracking purchase orders (POs), along with monitoring vendor performance metrics. Built with Django and Django REST Framework, this system allows organizations to efficiently manage their vendor relationships and ensure high-quality service delivery.
## Table of Contents

- [Features](#features)
- [Tech Stack](#techstack)
- [Project Structure](#project_structure)
- [Installation](#installation)
- [Usage](#usage)
    - [Running the Deployment Server](#running_server)
    - [API Endpoints](#api_endpoints)
- [Testing](#testing)
- [Additional Notes](#add_notes)

## Features <a name = "features"></a>

- ### Vendor Profile Management
    - Create, list, retrieve, update, and delete vendor profiles.

- ### Purchase Order Tracking
    - Create, list (with optional filtering by vendor), retrieve, update, and delete purchase orders.

- ### Vendor Performance Metrics
    - Retrieve on-time delivery rate and average quality rating for each vendor.

- ### Comprehensive Testing
    - Unit tests covering models, serializers, views, and URL routing to ensure reliability.

## Tech Stack <a name = "techstack"></a>

- Backend Framework: Django 5.x
- API Framework: Django REST Framework
- Database: SQLite (default)
- Language: Python 3.x

### Project Structure<a name = "project_structure"></a>

A well-organized project structure enhances maintainability and scalability. Here's an overview of the project's directory layout:
```
Vendor and PO Management/
├── manage.py
├── vendor_management/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── vendors/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── ... (migration files)
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests/
│       ├── __init__.py
│       ├── test_models.py
│       ├── test_serializers.py
│       ├── test_views.py
│       └── test_urls.py
├── requirements.txt
├── README.md
└── .gitignore

```

#### Explanation

- ```Vendor and PO Management/```: Root project directory.
  - ```manage.py```: Django's command-line utility.
  - ```vendor_management/```: Project-level configurations.
      - ```settings.py```: Configuration settings.
      - ```urls.py```: Root URL configurations.
      - ```wsgi.py```: WSGI application for deployment.
  - ```vendors/```: Django app managing vendors and purchase orders.
    - ```models.py```: Database models (Vendor and PurchaseOrder).
    - ```serializers.py```: DRF serializers for converting models to/from JSON.
    - ```views.py```: API views using DRF viewsets.
    - ```urls.py```: App-specific URL configurations.
    - ```tests/```: Test suite covering models, serializers, views, and URLs.
      - ```test_models.py```: Tests for models.
      - ```test_serializers.py```: Tests for serializers.
      - ```test_views.py```: Tests for API views.
      - ```test_urls.py```: Tests for URL routing.
    - ```admin.py```: Django admin configurations.
    - ```apps.py```: App configuration.
    - ```migrations/```: Database migration files.
  -```requirements.txt```: Project dependencies.
  -```db.sqlite3```: Database
  -```README.md```: Project documentation.
  -```.gitignore```: Specifies files/directories to be ignored by Git.



### Installation<a name = "installation"></a>

Follow these steps to set up the project locally:

#### Prerequisites
Python 3.x installed on your machine. You can download it from <a link="https://www.python.org/downloads/">python.org</a>.
Git installed for version control. Download from <a link="https://git-scm.com/downloads">git-scm.com</a>.
#### Steps
##### 1. Clone the Repository
```
git clone https://github.com/Ultronoss/Vendor-and-PO-management.git
cd Vendor-and-PO-management-main
```
##### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies.
```
python3 -m venv venv
```
##### 3. Activate the virtual Environment
``` venv\Scripts\activate```

##### 4. Install Dependencies
```pip install -r requirements.txt```

##### 5. Apply Database Migrations
```
python manage.py makemigrations
python manage.py migrate
```

##### 6. Create a Superuser (Optional)

To access Django's admin interface.
```
python manage.py createsuperuser
```

##### 7. Run tests
```
python manage.py test
```

### Usage<a name='usage'></a>
#### Running the Development Server
Start the Django development server to interact with the API.
```
python manage.py runserver
```
The API will be accessible at ```http://127.0.0.1:8000/api/```.

#### API Endpoints
The API provides endpoints for managing vendors, purchase orders, and retrieving vendor performance metrics.

#### 1. Vendor Profile Management
  - ##### Create a New Vendor
    - URL: `/api/vendors/`
    - Method: POST
    - Body:
      ```
        {
          "name": "Vendor Name",
          "contact_details": "Contact Information",
          "address": "Vendor Address",
          "vendor_code": "UNIQUE_CODE"
        }
      ```
  - ##### List All Vendors
    - URL: `/api/vendors/`
    - Method: GET
  - ##### Retrieve a Specific Vendor's Details
    - URL: `/api/vendors/{vendor_id}/`
    - Method: GET
  - ##### Update a Vendor's Details
    - URL: `/api/vendors/{vendor_id}/`
    - Method: PATCH (for partial updates) or PUT (for full updates)
    - Body: (Example for partial update)
      
      `
      {
        "name": "Updated Vendor Name"
      }
      `
  - ##### Delete a Vendor
    - URL: `/api/vendors/{vendor_id}/`
    - Method: DELETE

#### 2. Purchase Order Tracking
  - ##### Create a Purchase Order
    - URL: /api/purchase_orders/
    - Method: POST
    - Body:
      
      ```
      {
        "po_number": "PO123",
        "vendor": 1,  // Vendor ID
        "order_date": "2024-10-02T10:00:00Z",
        "delivery_date": "2024-10-10T10:00:00Z",
        "items": {"item1": "Description1", "item2": "Description2"},
        "quantity": 100,
        "status": "pending",  // Choices: pending, completed, canceled
        "quality_rating": 4.5,  // Optional (1.0 - 5.0)
        "issue_date": "2024-10-02T10:00:00Z",
        "delivered_date": null  // Nullable
      }
      ```
  - ##### List All Purchase Orders (With Optional Vendor Filtering)
    - URL: `/api/purchase_orders/`
    - Method: GET
  - ##### Query Parameters:
    - vendor: Filter POs by vendor ID (e.g., `/api/purchase_orders/?vendor=1`)
    - Retrieve a Specific Purchase Order's Details
    - URL: `/api/purchase_orders/{po_id}/`
    - Method: GET
  - ##### Update a Purchase Order
    - URL: `/api/purchase_orders/{po_id}/`
    - Method: PATCH (for partial updates) or PUT (for full updates)
    - Body: (Example for partial update)
      
      ```
      {
      "status": "completed",
      "quality_rating": 4.0,
      "delivered_date": "2024-10-09T10:00:00Z"
      }
      ```
  - ##### Delete a Purchase Order
    - URL: `/api/purchase_orders/{po_id}/`
    - Method: DELETE
#### 3. Vendor Performance Endpoint
  - ##### Retrieve Performance Metrics for a Specific Vendor
    - URL: `/api/vendors/{vendor_id}/performance/`
    - Method: GET
    - Response:
      ```
      {
        "on_time_delivery_rate": 95.0,  // Percentage
        "quality_rating_avg": 4.5        // Average rating
      }
      ```

## Testing <a name = "testing"></a>

Comprehensive tests ensure the reliability and correctness of your application. The project includes unit tests for models, serializers, views, and URL routing.

### 1. Running the Test Suite
Ensure the Virtual Environment is Activated

`venv\Scripts\activate`
### 2. Run Tests

`python manage.py test`

### Test Coverage
- #### Models Tests:

    - Validate creation and performance metrics calculation for Vendor and PurchaseOrder models.

- #### Serializers Tests:

    - Ensure serializers correctly serialize/deserialize data and enforce validation rules.

- #### Views Tests:

    - Test all API endpoints for expected behavior, including CRUD operations and performance metrics retrieval.

- #### URLs Tests:

    - Confirm that URLs are correctly routed to the intended views.
### Example Test Commands
- #### Run All Tests
    
    `python manage.py test`

- #### Run Specific Test
    
    `python manage.py test vendors.tests.test_views.PurchaseOrderAPITest.test_update_purchase_order`

## Additional Notes<a name="add_notes"></a>
- ### Admin Interface: 
    - While not included in this README, you can access Django's admin interface by navigating to /admin/ after creating a superuser. 
    - This allows you to manage vendors and purchase orders through a web interface.

- ### Error Handling: 
    - The API provides detailed error messages for invalid requests. 
    - Ensure that your requests adhere to the expected data formats and constraints.

- ### Extensibility: 
    - The project structure is designed to be scalable. 
    - You can easily add more features, such as authentication, advanced filtering, or integration with external services.

Made by Raj Mishra aka Ultronoss