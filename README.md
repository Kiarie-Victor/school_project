# 🗳️ University Student Delegate Voting System

This is a web-based voting platform for conducting secure and transparent delegate elections across multiple faculties in a university setting. The system is built with Django (Python) and optionally integrates with a blockchain backend for immutable vote storage.

---

## 🔧 Features

* **Student Authentication**

  * Login with registration number and OTP verification.

* **Candidate Management (Admin-only)**

  * Accept and register candidates for delegate positions.
  * Start and end elections for each year and faculty.

* **Voting System**

  * Vote for delegate candidates within your year and faculty.
  * Weighted voting:

    * Vote for 1 candidate → 1 full vote
    * Vote for 2 candidates → each gets 0.5 vote

* **Results Calculation**

  * Top N candidates per year win (configurable per faculty).
  * Admin declares winners after vote tallying.

* **Blockchain Integration**

  * Votes are stored immutably on a blockchain via smart contracts.
  * Provides transparent, tamper-proof election records.

* **Student Dashboard**

  * View elections, vote status, results, and verifiable records.
  * Hamburger-style navigation menu.

---

## 🏛️ System Structure

### 🎓 Faculties Supported

* CIT
* Business
* Engineering
* Social Sciences
* Media & Communication
* Science & Technology

### 📊 Voting Rules

* Each student votes **only** for candidates in their **year and faculty**.
* Voting limits are enforced based on number of candidates.
* Delegate winners per year (example configuration):

  * 1st & 2nd year: top 3
  * 3rd & 4th year: top 2

---

## 🗂️ Tech Stack

| Component      | Tech              |
| -------------- | ----------------- |
| Backend        | Django, Python    |
| Frontend       | HTML, Bootstrap   |
| Blockchain     | Solidity, Web3.py |
| Database       | PostgreSQL        |
| Authentication | Custom with OTP   |

---

## 📁 Project Structure

```
voting_system/
├── accounts/              # Handles auth and user models
├── core/                  # Student dashboard, voting logic
├── templates/             # HTML templates
├── static/                # CSS, JS, Images
├── contracts/             # Smart contracts (Solidity)
├── manage.py
├── README.md
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/voting_system.git
cd voting_system
```

### 2. Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure `.env`

```env
DEBUG=True
DATABASE_NAME=your_db
DATABASE_USER=your_user
DATABASE_PASSWORD=your_pass
DATABASE_HOST=localhost
DATABASE_PORT=5432
DJANGO_SECRET_KEY=your-secret-key
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

### 7. Run the Server

```bash
python manage.py runserver
```

---

## ⛓️ Blockchain Integration

* Smart contracts are written in Solidity and deployed on a local or testnet Ethereum blockchain.
* Django interacts with the blockchain using Web3.py.
* Votes are pushed to the smart contract during election, ensuring immutability and transparency.

> More details in the `/contracts` directory and upcoming deployment guide.

---

## 🧪 Tests

To run tests:

```bash
python manage.py test
```

---

## 📜 License

MIT License

---