# Trekking Management System 
This is a web application developed my me; 24f350047 Om Shiv Verma for my MAD-1 Project for keeping and maintaning the trekking, booking, staff and trekkers record in one place to access it smartly and easily as much as possible and look professional.

# Project Overview
## 📋 Project Overview

The Trekking Management System is designed for adventure organizations that conduct multiple trekking events throughout the year. Managing participants, trek leaders, schedules, and bookings manually can become difficult as the number of treks increases.

This application provides separate dashboards for **Admin**, **Staff**, and **Trekkers**, allowing each user to access only the features relevant to their role. The system also helps prevent duplicate bookings, manages available slots, tracks trek history, and keeps all trek-related information organized in one place.

---

# 🚀 Features

## 👨‍💼 Admin

- Login using predefined admin account
- Add new trekking events
- Edit trek information
- Delete existing treks
- View all available treks
- View all registered staff members
- View all registered trekkers
- Approve or reject staff registrations
- Blacklist or unblacklist staff members
- Search users by ID or name
- Search treks by ID or name
- View all trek bookings

---

## 🧑‍💼 Trek Staff

- View assigned treks
- Update available slots
- Update trek status
- View participants assigned to each trek
- Update personal profile information

---

## 🥾 Trekker

- Register and login
- View upcoming treks
- Search treks by location and difficulty
- Book trekking events
- Cancel booked treks
- View booked treks
- View completed trek history

---

# 🧱 Tech Stack

| Layer | Technology |
|--------|------------|
| Backend | Flask (Python) |
| Frontend | HTML5, CSS3 |
| Database | SQLite3 |
| ORM | SQLAlchemy |
| Template Engine | Jinja2 |
| Authentication | Flask Session |
| Version Control | Git & GitHub |

---

# 📂 Project Structure

```text
TREKKING-MANAGEMENT-SYSTEM/
│
├── app.py                     # Main Flask application
├── models.py                  # Database models
├── config.py                  # Application configuration
│
├── trekking_management.db     # SQLite database
│
├── static/
│   ├── style.css
│   └── images/
│
├── templates/
│   │
│   ├── home-page.html
│   ├── login.html
│   ├── register.html
│   │
│   ├── admin/
│   │   ├── add-trek.html
│   │   ├── edit-trek.html
│   │   ├── view-treks.html
│   │   ├── view-users.html
│   │   ├── view-bookings.html
│   │   ├── search-ppl.html
│   │   └── search-trek.html
│   │
│   ├── staff/
│   │   ├── assigned-treks.html
│   │   ├── participants.html
│   │   ├── edit-trek-slots.html
│   │   ├── edit-trek-status.html
│   │   └── update-profile.html
│   │
│   ├── trekker/
│   │   ├── available-treks.html
│   │   ├── booked-treks.html
│   │   ├── completed-treks.html
│   │   └── search-treks.html
│   │
│   └── dashboard/
│       ├── admin.html
│       ├── staff.html
│       └── trekker.html
│
├── README.md
└── requirements.txt
```

---

# 🗄️ Database Models

### User

Stores information about every registered user.

- Admin
- Trek Staff
- Trekker

---

### Trek

Stores all trekking event details.

- Trek Name
- Location
- Difficulty
- Duration
- Available Slots
- Assigned Staff
- Start Date
- End Date
- Trek Status

---

### Booking

Maintains records of trek bookings.

- Trekker
- Trek
- Booking Date
- Booking Status

---

# 🔑 User Roles

### Admin

Responsible for managing the complete trekking system including treks, users, staff approvals, bookings, and trek assignments.

### Staff

Responsible for handling assigned treks, monitoring participants, updating trek progress, and managing trek availability.

### Trekker

Can browse available treks, search based on preferences, book or cancel treks, and maintain personal trek history.

---

# ▶️ Running the Project

### Clone the repository

```bash
git clone https://github.com/your-username/trekking-management-system.git
```

### Move into the project directory

```bash
cd trekking-management-system
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the environment

Windows

```bash
venv\Scripts\activate
```

Mac/Linux

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the application

```bash
python app.py
```

The application will be available at

```
http://127.0.0.1:5000/
```

---

# 📌 Future Improvements

- Medical certificate upload for trekkers
- Email notifications for booking confirmation
- Payment gateway integration
- Trek image gallery
- GPS-based trek tracking
- Weather updates for trekking locations
- Admin analytics dashboard

---

# 👩‍💻 Developed By

**Om Shiv Verma**

Bachelor of Technology (Computer Science)

Academic Project – Trekking Management System using Flask & SQLite