# 🚗 Car Website (Django)

This repository contains a **Django-based web application** for exploring motorsport data, focusing on Formula One and Cars. It includes races, drivers, teams, and circuits, with detailed statistics and filtering options For Fomula1.

## Future developments
- [ ] create an API for car app
- [ ] develop car app 

> The Django project is located inside a subfolder, and the virtual environment is **not included**. This README guides you through setting up the project from scratch.

---

## 📂 Repository Structure

```
car-website-vnv/
│
├── car-website/          # Django project folder
│   ├── manage.py
│   ├── car_website/      # Django project settings
│   ├── apps/             # Django apps (e.g. FormulaOne)
│   └── requirements.txt
│
└── README.md             # This file
```


---

## ⚙️ Prerequisites

- **Python 3.10+**
- **pip**
- **Git**
- (Optional but recommended) **virtualenv**

---

## 🧪 Step 1: Clone the Repository

```bash
    git clone <your-repository-url>
    cd car-website-vnv
```
<br>

## ✔️ Step 2: Create and Activate a Virtual Environment
  - windows
    ```bash
        python -m venv venv
        venv\Scripts\activate
    ```
  - macOS / Linux
    ```bash
        python3 -m venv venv
        source venv/bin/activate
    ```
<br>

## 📦 Step 3: Install Dependencies
```bash
    cd car-website
    pip install -r requirements.txt
```
<br>

## 🔐 Step 4: Environment Variables
Create it based on a file named .env.example in this folder 

<br>

## 🗄️ Step 5: Apply Database Migrations
```bash
    python manage.py makemigrations
    python manage.py migrate
```
<br>

## 👤 Step 6: Create a Superuser (Optional)
```bash
    python manage.py createsuperuser
```
<br>

## ▶️ Step 7: Run the Development Server
```bash
    python manage.py runserver
```
then Open your browser at http://127.0.0.1:8000


# 📄 License

This project is for educational and personal use.