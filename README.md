# Comrade-FinanceTracker-Backend
# Finance Tracking AI App - Backend Documentation

## 📋 Project Overview
The **Finance Tracking AI App** is designed to help university students in Kenya manage their finances effectively. The backend is powered by **Django** and **Django REST Framework (DRF)**, providing secure APIs for tracking expenses, managing budgets, and integrating AI-driven financial insights.

---

## 🚀 Features
- **Expense Tracking:** Automatically categorize expenses and allow manual entries.
- **Budgeting Tools:** Set, track, and receive alerts for budgets.
- **Savings Goals:** Create, track, and predict savings goals.
- **Personalized Insights:** AI-powered recommendations based on spending habits.
- **Authentication:** Secure user authentication with JWT.
- **Localized Integrations:** Support for M-Pesa and Kenyan currency.

---

## 🏗️ Technology Stack
- **Backend Framework:** Django, Django REST Framework
- **Database:** PostgreSQL
- **Authentication:** JWT (JSON Web Tokens)
- **AI/ML:** Scikit-learn, TensorFlow (for future AI features)
- **Deployment:** Docker (optional), Cloud Platforms

---

## ⚙️ Setup Instructions

### 1️⃣ Prerequisites
- Python 3.10+
- PostgreSQL
- Virtualenv (recommended)

### 2️⃣ Installation
```bash
# Clone the repository
git clone https://github.com/your-username/finance-tracking-backend.git
cd finance-tracking-backend

# Create a virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure PostgreSQL settings in settings.py or .env file

# Apply migrations
python manage.py migrate

# Run the development server
python manage.py runserver
```

### 3️⃣ Environment Variables
Create a `.env` file:
```ini
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=postgres://username:password@localhost:5432/your_db
```

---

## 🗂️ Project Structure
```
finance-tracking-backend/
├── finance_app/           # Core Django app
│   ├── models.py          # Database models (Expense, Budget, SavingsGoal)
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API views
│   └── urls.py            # App-specific routes
├── finance_ai/            # AI models and logic
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies
```

---

## 🔐 Authentication
Using **JWT (JSON Web Tokens)** for secure API access.

- **Obtain Token:**
  ```bash
  POST /api/token/
  { "username": "user", "password": "pass" }
  ```
- **Refresh Token:**
  ```bash
  POST /api/token/refresh/
  { "refresh": "your_refresh_token" }
  ```
- **Secure Requests:**
  Add the token to the `Authorization` header:
  ```bash
  Authorization: Bearer your_access_token
  ```

---

## 📊 API Endpoints
| Method | Endpoint              | Description                 |
|--------|-----------------------|-----------------------------|
| GET    | /expenses/            | List all expenses           |
| POST   | /expenses/            | Create a new expense        |
| GET    | /budgets/             | Retrieve budgets            |
| POST   | /savings-goals/       | Set a new savings goal      |
| POST   | /api/token/           | User login (obtain token)   |
| POST   | /api/token/refresh/   | Refresh JWT token           |

> **Note:** All endpoints (except auth) require authentication.

---

## 🤖 AI Integration (Planned)
- **Spending Pattern Analysis** (Clustering, Time Series)
- **Budget Recommendations** (Regression, Predictive Models)
- **Anomaly Detection** (Fraud Detection)
- **Financial Literacy Chatbot** (NLP)

AI modules will be served via APIs or integrated directly within the Django app.

---

## 🧪 Running Tests
```bash
python manage.py test
```

---

## 🙌 Contributing
1. Fork the repository
2. Create a new branch (`git checkout -b feature-xyz`)
3. Commit changes (`git commit -m 'Add feature xyz'`)
4. Push to your branch (`git push origin feature-xyz`)
5. Open a Pull Request

---

## 📄 License
[MIT License](LICENSE)

---

## 💡 Contact
For questions or support:
- **Email:** yourname@example.com
- **GitHub:** [@your-username](https://github.com/your-username)

> *Empowering Kenyan students with smarter financial tools!*

