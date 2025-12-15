# Lost and Found Management System

## 📌 Overview
The Lost and Found Management System is a web-based application that enables users to report lost and found items and helps match them efficiently. Administrators manage users, categories, and item data to ensure system integrity and accuracy.

## 🎯 Objectives
- Digitize lost and found item management
- Reduce manual effort and data loss
- Provide intelligent matching between lost and found items
- Enable admin-level monitoring and control

## 👥 User Roles
### 1. User
- Register and log in
- Add lost items
- Add found items
- View lost items
- View found items
- View matching items

### 2. Admin
- Login securely
- Manage users
- Add and manage categories
- View found items
- Monitor system activity

## 🔄 System Modules
### Authentication Module
- User Registration
- User Login
- Admin Login

### User Module
- Add Lost Item
- Add Found Item
- View Lost Items
- View Found Items
- View Matching Items

### Admin Module
- Manage Users
- Add Category
- View Found Items

### Matching Module
- Matches lost and found items based on category, location, and description

## 🗄️ Database Tables
- `user_tb`
- `admin_tb`
- `category_tb`
- `lost_tb`
- `found_tb`
- `matching_tb`

## 🧩 Data Flow Diagram (DFD)
The system follows a structured DFD approach where:
- Users and Admins interact with system processes
- Data is stored and retrieved from dedicated database tables
- Matching logic connects lost and found records

## 🛠️ Technology Stack
- Backend: Python (Django / Flask)
- Frontend: HTML, CSS, JavaScript
- Database: MySQL / SQLite
- Image Processing (optional): OpenCV
- Authentication: Session-based / JWT

## 🚀 How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/lost-and-found-management-system.git
