# Skillhunt Backend


## 📋 Overview

The backend for Skillhunt Job Portal provides a robust API infrastructure built with Django Rest Framework. It handles all server-side operations for employers, job seekers, and administrators, featuring secure authentication, real-time communications, and scalable data management.

## 🛠️ Technology Stack

- **Framework:** Django 5.1.2, Django Rest Framework 3.15.2
- **Database:** PostgreSQL
- **Authentication:** JWT (djangorestframework-simplejwt), Google OAuth
- **Real-time:** Channels, WebSockets (Daphne, Channels Redis)
- **Payment Processing:** Razorpay, Stripe
- **Deployment:** ASGI (Daphne)
- **Security:** OTP Verification, Token-based Authentication
- **File Handling:** Pillow

## ✨ Features

- **RESTful API:** Comprehensive API for all job portal operations
- **Multi-factor Authentication:** JWT + OTP verification
- **Social Authentication:** Google login integration
- **Real-time Communication:** WebSocket for chat and notifications
- **Payment Integration:** Razorpay and Stripe for subscriptions and services
- **Role-based Access Control:** Different permissions for job seekers, employers, and admins
- **File Upload/Download:** Resume and company profile document handling
- **Search & Filtering:** Advanced job and candidate search capabilities
- **Cross-Origin Support:** CORS configured for frontend integration

## 🚀 Installation

### Prerequisites

- Python 3.10+
- PostgreSQL
- Redis (for Channels)
- Virtual environment tool (venv, virtualenv)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/skillhunt-backend.git
   cd skillhunt-backend
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   cp .env.example .env
   ```
   Update the `.env` file with your configuration:

   ```
   # Database
   DATABASE_URL=postgres://user:password@localhost:5432/skillhunt

   # Django
   SECRET_KEY=your_secret_key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1

   # JWT
   JWT_SECRET_KEY=your_jwt_secret
   ACCESS_TOKEN_LIFETIME=5  # in hours
   REFRESH_TOKEN_LIFETIME=7  # in days

   # Redis
   REDIS_URL=redis://localhost:6379/0

   # Google Auth
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret

   # Payment
   RAZORPAY_KEY_ID=your_razorpay_key
   RAZORPAY_KEY_SECRET=your_razorpay_secret
   
   # Email (for OTP)
   EMAIL_HOST=smtp.example.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your_email@example.com
   EMAIL_HOST_PASSWORD=your_email_password
   EMAIL_USE_TLS=True
   ```

5. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

8. **For WebSocket support, run Daphne**
   ```bash
   daphne -p 8001 skillhunt.asgi:application
   ```

## 📁 Project Structure

```
backend/
├── api/              # User authentication and profiles
├── jobs/                  # Job listings and applications
├── employers/             # Employer functionality
├── resumes/               # Resume builder functionality
├── interviews/            # Interview scheduling
├── chat/                  # WebSocket-based chat
├── subscriptions/         # Payment plans and subscriptions
├── notifications/         # User notifications system
├── utils/                 # Utility functions and helpers
├── backend/
│   ├── settings.py        # Project settings
│   ├── urls.py            # Main URL routing
│   ├── asgi.py            # ASGI configuration
│   └── wsgi.py            # WSGI configuration
├── manage.py
├── requirements.txt
└── README.md
```

## 🔑 API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login and get tokens
- `POST /api/auth/token/refresh/` - Refresh access token
- `POST /api/auth/google/` - Google authentication
- `POST /api/auth/verify-otp/` - Verify OTP code
- `POST /api/auth/send-otp/` - Send OTP to email/phone

### Users
- `GET /api/users/me/` - Get current user profile
- `PUT /api/users/me/` - Update user profile
- `PATCH /api/users/me/` - Partial update user profile

### Jobs
- `GET /api/jobs/` - List all jobs with filters
- `POST /api/jobs/` - Create new job (employers only)
- `GET /api/jobs/{id}/` - Get job details
- `PUT /api/jobs/{id}/` - Update job
- `DELETE /api/jobs/{id}/` - Delete job

### Applications
- `GET /api/applications/` - List user's applications
- `POST /api/jobs/{id}/apply/` - Apply for a job
- `GET /api/applications/{id}/` - Get application details
- `PATCH /api/applications/{id}/` - Update application status

### Resume
- `GET /api/resumes/` - Get user's resumes
- `POST /api/resumes/` - Create new resume
- `GET /api/resumes/{id}/` - Get resume details
- `PUT /api/resumes/{id}/` - Update resume
- `DELETE /api/resumes/{id}/` - Delete resume

### Employers
- `GET /api/employers/` - List employers
- `GET /api/employers/{id}/` - Get employer details
- `GET /api/employers/{id}/jobs/` - Get employer's jobs

### Subscriptions
- `GET /api/subscriptions/plans/` - Get available plans
- `POST /api/subscriptions/subscribe/` - Subscribe to a plan
- `GET /api/subscriptions/my-plan/` - Get current subscription
- `POST /api/subscriptions/webhook/` - Payment webhook

### Admin (restricted)
- `GET /api/admin/users/` - List all users
- `GET /api/admin/jobs/` - List all jobs
- `GET /api/admin/subscriptions/` - List all subscriptions

## 💬 WebSocket Endpoints

- `/ws/chat/{room_id}/` - Chat room connection
- `/ws/notifications/` - Real-time notifications

## 🔐 Authentication Flow

The backend implements a secure multi-factor authentication flow:

1. **Registration:** User registers with email/password
2. **OTP Verification:** System sends OTP to verify email
3. **JWT Tokens:** Upon verification, system issues access and refresh tokens
4. **Token Refresh:** Access tokens refresh automatically using refresh tokens
5. **Social Auth:** Alternatively, users can authenticate via Google
6. **Permission Layers:** Different user roles (job seeker, employer, admin) have different permissions

## 📱 Testing

Run tests with:

```bash
# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test accounts
```

## 🌐 Deployment

### Production Setup

1. Set `DEBUG=False` in your `.env` file
2. Configure proper ALLOWED_HOSTS
3. Use a production-ready database
4. Set up a proper web server (Nginx/Apache)

### ASGI Deployment (for WebSockets)

Using Daphne:
```bash
daphne -b 0.0.0.0 -p 8001 skillhunt.asgi:application
```

Or with Gunicorn and Uvicorn workers:
```bash
gunicorn skillhunt.asgi:application -k uvicorn.workers.UvicornWorker
```

## 🔄 CI/CD Integration

- Automated tests run on GitHub Actions
- Automatic deployment to staging/production based on branch
- Database migration checks before deployment

## 📈 Performance Optimization

- Redis caching for frequent queries
- Database query optimization
- Connection pooling
- Rate limiting on API endpoints
- Asynchronous task processing for emails and notifications

## 🔒 Security Measures

- JWT token expiration
- CSRF protection
- OTP verification
- HTTPS only in production
- Password hashing with Django's authentication system
- Input validation and sanitization
- Rate limiting for auth endpoints

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact

For any questions or suggestions, please open an issue or contact the repository owners.

---

Made ❤️ by Nahima Machingal
