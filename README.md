# 🛍️ Ecommerce Project API

A robust and scalable Ecommerce RESTful API built with **Django** and **Django Rest Framework (DRF)**. This project provides a complete backend solution for an online store, featuring user authentication, product management, shopping cart functionality, and order processing.
- THIS README WAS MADE WITH AI BUT I LIKE IT

---

## 🚀 Features

- **🔐 User Authentication**: Secure Sign-up, Login, Logout, and Profile management using Token-based authentication.
- **📦 Product Management**: Full CRUD operations for products and categories with advanced filtering and search capabilities.
- **🛒 Shopping Cart**: Add, update, and remove items from a persistent shopping cart.
- **📝 Order Processing**: seamless checkout process, order tracking, and cancellation with automatic stock management.
- **🔍 Advanced Filtering**: Filter products by various criteria and search through categories and items.
- **📊 Aggregations**: Built-in endpoints for calculating total inventory value and individual product statistics.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.x, Django 6.1
- **API Framework**: Django Rest Framework (DRF) 3.18
- **Database**: SQLite (Default)
- **Authentication**: DRF Token Authentication
- **Imaging**: Pillow (for product images)

---

## 📁 Project Structure

```text
Ecommerce_Project/
├── auth/            # Authentication logic & User profiles
├── cart/            # Shopping cart management
├── products/        # Catalog management (Products & Categories)
├── orders/          # Order processing & Stock management
├── users/           # Custom user models (if applicable)
├── media/           # Product images storage
└── requirements.txt # Project dependencies
```

---

## 🚦 Getting Started

### 1. Prerequisites
- Python 3.8+
- pip

### 2. Installation
Clone the repository and install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Database Setup
```bash
python manage.py migrate
```

### 4. Create a Superuser
```bash
python manage.py createsuperuser
```

### 5. Run the Server
```bash
python manage.py runserver
```
The API will be available at `http://127.0.0.1:8000/api/`

---

## 🔌 API Endpoints

### 🔑 Authentication
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/auth/signup/` | Register a new user |
| `POST` | `/api/auth/login/` | Login and receive Token |
| `POST` | `/api/auth/logout/` | Logout and invalidate Token |
| `GET` | `/api/auth/profile/` | Get current user profile |

### 👕 Products & Categories
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/products/` | List all products (supports search/filter) |
| `POST` | `/api/products/` | Create a product (Admin only) |
| `GET` | `/api/products/{id}/` | Get product details |
| `GET` | `/api/categories/` | List all categories |
| `GET` | `/api/products/total-value/` | Get total inventory value |

### 🛒 Shopping Cart
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/cart/` | View current cart |
| `POST` | `/api/cart/add/` | Add item to cart |
| `PUT` | `/api/cart/{id}/update/` | Update item quantity |
| `DELETE` | `/api/cart/clear/` | Empty the cart |

### 📦 Orders
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/orders/` | List user orders |
| `POST` | `/api/orders/` | Place an order (Checkout) |
| `GET` | `/api/orders/{id}/` | Get order details |
| `POST` | `/api/orders/{id}/cancel/` | Cancel an order |

---

## 🔒 Authentication Guide

To access protected endpoints, include the token in your HTTP header:

```http
Authorization: Token <your_token_here>
```
