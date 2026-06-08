# Smart-Scholarship-Recommender-Portal
Smart Scholarship Recommender Portal is a web-based platform that helps students discover and apply for scholarships based on eligibility criteria such as education, category, income, and location. Built using Python, Django, PostgreSQL, and REST APIs


# 🎓 Smart Scholarship Recommender Portal

A centralized web-based scholarship management platform that helps students discover, apply for, and track scholarships based on eligibility criteria such as education, category, income, and location.

Built using **Python, Django, Django REST Framework (DRF), PostgreSQL, Postman, Git, and GitHub**.

---

# 📌 Problem Statement

Students often struggle to find scholarships that match their academic background, category, income level, and eligibility criteria. Scholarship information is scattered across multiple government and private portals, making the application process time-consuming and confusing.

Current challenges include:

* Difficulty discovering relevant scholarships
* Lack of personalized recommendations
* Manual application tracking
* Missed scholarship deadlines
* Complex eligibility verification
* Inefficient scholarship management for providers
* No centralized platform for administration and monitoring

There is a need for a centralized scholarship portal that simplifies scholarship discovery, eligibility matching, application management, and tracking for all stakeholders.

---

# 💡 Solution

The Smart Scholarship Recommender Portal provides a centralized platform connecting Students, Scholarship Providers, and Administrators.

The system allows:

* Students to discover and apply for scholarships.
* Scholarship Providers to create and manage scholarship programs.
* Administrators to verify providers, manage users, and monitor the platform.

The portal uses profile-based filtering to recommend scholarships according to student eligibility.

---

# 👥 User Roles

## 👨‍🎓 Student

Students can:

* Register and Login
* Complete Profile
* Search Scholarships
* Filter Scholarships
* Save Scholarships
* Apply for Scholarships
* Upload Documents
* Track Application Status
* Receive Notifications

---

## 🏢 Scholarship Provider

Providers can:

* Register Organization
* Create Scholarships
* Set Eligibility Criteria
* Manage Scholarship Listings
* Review Applications
* Approve/Reject Applications
* Generate Reports

---

## 👨‍💼 Admin

Administrators can:

* Manage Users
* Verify Scholarship Providers
* Approve Scholarship Listings
* Monitor Activities
* Generate Reports
* Manage Notifications
* Maintain Platform Security

---

# 🚀 Key Features

### Authentication & Authorization

* Multi-role Registration
* Email Verification
* Mobile OTP Verification
* Login with Email or Mobile Number
* Forgot Password
* Role-Based Access Control

### Scholarship Management

* Scholarship Creation
* Scholarship Search
* Scholarship Filtering
* Eligibility Matching
* Scholarship Recommendations

### Application Management

* Online Applications
* Document Upload
* Application Tracking
* Status Updates

### Notification System

* Email Notifications
* OTP Verification
* Application Updates
* Scholarship Deadline Reminders

### Administration

* User Management
* Provider Verification
* Analytics Dashboard
* Audit Logs

---

# 🛠 Technology Stack

## Backend

* Python
* Django
* Django REST Framework (DRF)

## Database

* PostgreSQL

## API Testing

* Postman

## Version Control

* Git
* GitHub

---

# 📂 Project Structure

```bash
Smart-Scholarship-Recommender-Portal/
│
├── config/                     # Project Settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── users/                      # Authentication & User Management
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── permissions.py
│
├── students/                   # Student Module
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── providers/                  # Scholarship Provider Module
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── scholarships/               # Scholarship Management
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── applications/               # Scholarship Applications
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── notifications/              # Email & OTP Notifications
│   ├── services.py
│   ├── views.py
│   └── urls.py
│
├── reports/                    # Analytics & Reports
│   ├── views.py
│   └── services.py
│
├── media/                      # Uploaded Documents
│
├── static/                     # Static Files
│
├── requirements.txt
├── manage.py
└── README.md
```

---

# 🔐 Authentication Flow

1. User Selects Role

   * Student
   * Scholarship Provider
   * Admin

2. Registration

3. Mobile OTP Verification

4. Email Verification

5. Account Activation

6. Login

   * Email + Password
   * Mobile Number + Password

7. Forgot Password

8. OTP Verification

9. Reset Password

10. Login Again

---

# 📊 Database Modules

PostgreSQL Database Stores:

* Users
* Roles
* Student Profiles
* Provider Profiles
* Scholarships
* Eligibility Criteria
* Applications
* Uploaded Documents
* Notifications
* Reports
* Audit Logs

---

# 🔄 API Endpoints

```http
POST /api/register/
POST /api/login/
POST /api/send-otp/
POST /api/verify-otp/
POST /api/forgot-password/
POST /api/reset-password/

GET  /api/scholarships/
POST /api/scholarships/

POST /api/applications/
GET  /api/applications/

GET  /api/providers/
GET  /api/students/
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/your-username/Smart-Scholarship-Recommender-Portal.git
cd Smart-Scholarship-Recommender-Portal
```

## Create Virtual Environment

```bash
python -m venv venv
```

## Activate Environment

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure PostgreSQL Database

Update database configuration in:

```python
config/settings.py
```

## Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Run Server

```bash
python manage.py runserver
```

---

# 🎯 Future Enhancements

* AI-Based Scholarship Recommendation Engine
* SMS Gateway Integration
* Document Verification System
* Scholarship Deadline Alerts
* Advanced Analytics Dashboard
* Mobile Application
* Machine Learning Recommendation Model

---

# 👩‍💻 Team Project

Academic Project

Smart Scholarship Recommender Portal

A Scholarship Discovery, Recommendation, Application Tracking and Management System.

---

# 📄 License

This project is developed for educational and academic purposes.
