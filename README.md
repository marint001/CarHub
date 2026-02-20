# CarHub Backend: Car E-Commerce & Customization Engine

CarHub is a Django backend, it is a system that serves as a core for a digital car dealership. It handles everything from inventory management to a detailed vehicle customization system.

## Technical Specifications
- **Language:** Python 3.12
- **Backend Framework:** Django 6.0
- **Database:** MySQL

## Key Features
1. Unified Inventory System
Supports separate logic for New and Used vehicles:

Used: Tracks mileage, VIN, service history, and previous owners.

New: Tracks factory stock and availability.

2. Deep Customization Engine
The core of the project. The API allows users to "build" their car by selecting:

Base Models & Trims (Base, Sport, Luxury, etc.)

Exterior/Interior Palette (Paint codes, upholstery materials)

Performance Packages (Wheels, engine upgrades, tech packs)

Conflict Logic: Prevents selecting incompatible parts (e.g., specific wheels only available with Sport trim).

## Setup and Installation
1. **Clone the project:**
   `git clone <your-url>`

2. **Set up Virtual Env:**
   `python -m venv venv`
   `source venv/bin/activate`

3. **Install Packages:**
   `pip install -r requirements.txt`

4. **Configure Database:**
   Open `config/settings.py` and update the `DATABASES` section with your MySQL `USER` and `PASSWORD`.

5. **Initialize DB:**
   `python manage.py migrate`

6. **Create Admin Access:**
   `python manage.py createsuperuser`
   *(Follow the prompts to set your own login)*

7. **Run:**
   `python manage.py runserver`

## This Project is still in development and Frontend is pending