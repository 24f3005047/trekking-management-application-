# Trekking Management System 
This is a web application developed my me; 24f350047 Om Shiv Verma for my MAD-1 Project for keeping and maintaning the trekking, booking, staff and trekkers record in one place to access it smartly and easily as much as possible and look professional.

## 📋 Project Overview

The Trekking Management System is designed for adventure organizations and trekking communities that conduct multiple trekking events throughout the year. Managing participants, trek leaders, schedules, and bookings manually can become difficult as the number of treks increases. So

This application provides separate dashboards for **Admin**, **Staff**, and **Trekkers**, allowing each user to access only the features relevant to their role. The system also helps prevent duplicate bookings, manages available slots, tracks trek history, and keeps all trek-related information organized in one place.

---

# 🚀 Features

## 👨‍💼 Admin

- Login using predefined admin account
- Add new treks
- Edit trek information; name,location,duration,slots,dates,staff it is assigned to etc
- Delete existing treks
- View all treks
- View all registered staff members
- View all registered trekkers
- Approve staff memeber's account to let them login
- Change approval status of a trekker to pending to stop them from logging in
- Switch a staff member's or trekker's blacklisted status between active and blacklisted
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
- Book treks
- Cancel booked treks
- View booked treks
- View completed trek history

---

# 🧱 Tech Stack

| Layer           | Technology     |
|-----------------|----------------|
| Backend         | Flask (Python) |
| Frontend        | HTML5, CSS3    |
| Database        | SQLite3        |
| ORM             | SQLAlchemy     |
| Template Engine | Jinja2         |
| Authentication  | Flask Session  |
| Version Control | Git & GitHub   |

---

# 📂 Project Structure

```text
TREKKING-MANAGEMENT-APP/
│
├── app.py                     # Main Flask application
├── models.py                  # Database models
├── config.py                  # Application configuration
│
├── static/
│   ├── css/
|   |   |
|   |   └──style.css
|   |   
│   └── images/
|       |
│       └── images/
|
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
├── report.pdf
└── requirements.txt
```

---

# 🗄️ Database Models

### User

Stores all information about every registered user- Admin,Staff,Trekker

- User ID
- Name
- Email
- Password
- Contact
- Role
- Approved
- Blacklisted

---

### Trek

Stores all trekking event details.

- Trek ID
- Trek Name
- Location
- Difficulty
- Duration
- Available Slots
- Assigned Staff ID
- Trek Status
- Start Date
- End Date

---

### Booking

Maintains records of trek bookings.

- Boking ID
- Trekker Id
- Trek ID
- Booking Date
- Booking Status

---

# 🔑 User Roles

### Admin

The admin can add treks, edit treks, view staff members, view trekkers, mark staff and trekkers as blacklisted and approved, search for staff and trekkers using their user_id or name, search for treks using trek_id or its name and also view the bookings done by the trekkers.

### Staff

Staff members can view treks that are assigned to them, edit trek slots and status of the assigned treks, view the participants that have booked for the trek he/she has been assigned to, staff member can also update his profile- name, contact, email.

### Trekker

Trekkers can view the available(upcoming) treks, and book the treks from the upcoming treks by clicking on the book button, view the treks for which they have done the booking, view the treks that they have completed until present date, they can also see the treks according to the difficulty and location of the treks.

---

# 📌 Future Improvements we can make

- Medical certificate upload for trekkers for better trek recommendations
- Email notifications for booking confirmation
- Payment gateway integration for booking amount which will be minimal
- Trek image gallery, for better booking 
- Weather updates for trekking locations
- Admin analytics dashboard

---

# Image used in the project

I took this background image of mountains from a website name unsplash and the user and the image link are given below I give the credit for the image to him.
[text](https://unsplash.com/photos/snowy-mountain-g30P1zcOzXo?utm_source=unsplash&utm_medium=referral&utm_content=creditShareLink)

---

# 👩‍💻 Developed By

**Om Shiv Verma**

Academic Project – Trekking Management System using HTML,CSS,Bootstrap,Flask & SQLAlchemy