# MazalTov CRM 🎉

A full-stack CRM system designed for photographers, focused on managing clients, leads, and event details in a simple and secure way.

🔗 Live Demo: https://mazaltovcrm.com/

---

## 📌 About The Project

MazalTov CRM is a personal project built to solve a real business need in a specific photographers community.  
The system allows photographers to manage their clients efficiently, collect event details via a personal public link, and automatically send documents to clients via email.

This project was designed, developed, and deployed end-to-end.

---

## ✨ Key Features

- 👤 **User Authentication**
  - Secure login system for photographers
  - Each user manages only their own data

- 🔗 **Personal Public Form**
  - Each user receives a unique link to send to clients
  - Clients can fill in their event details without logging in
  - The form is fully separated from the internal system for security

- 📋 **Lead & Client Management**
  - Create, update, and delete leads
  - View full client details in a clean dashboard

- 📧 **Email Automation**
  - Automatically send documents to clients via email
  - Server-side email handling using Django

- 🔐 **Security & Best Practices**
  - CSRF protection
  - Environment variables for secrets
  - Production deployment with HTTPS

---

## 📸 Screenshots

### Custom Fields
Users can create, edit, and delete custom fields for their deal details.
Each custom field can also be overridden for a specific lead.

<img alt="Custom fields management" src="https://github.com/user-attachments/assets/045ca219-579c-4662-8c9e-3345e5af1ef6" />


### User Dashboard
Users can manage their personal details, which are used for generating PDF documents sent to clients.
They can also upload a regulations file that will be attached to the public submission form.

<img alt="User dashboard" src="https://github.com/user-attachments/assets/918b7d00-8d00-43b8-b045-97a0803f87ea" />


### Lead List View
Users can view a list of their clients, visually organized by Hebrew months and weeks using color coding.
The list also supports searching by client name or event date.

<img alt="Lead list view" src="https://github.com/user-attachments/assets/ac0af032-a5a9-4330-86ff-949d43cdd6f2" />


### Public Client Form
Clients receive a unique personal link that allows them to securely submit their event details without logging in.
The form is fully separated from the internal CRM system to prevent unauthorized access.

<img alt="Public client form" src="https://github.com/user-attachments/assets/3cd47fde-be27-4572-a3ee-3b879a3af9e6" />

---

## 🛠️ Tech Stack

- **Backend:** Python, Django  
- **Frontend:** HTML, CSS (Django Templates)  
- **Database:** PostgreSQL  
- **Authentication:** Django Auth  
- **Deployment:** Railway  
- **Domain & SSL:** Custom domain with HTTPS  

---

## 🚀 Deployment

The application is deployed to production using Railway and connected to a custom domain.

- Production-ready configuration (`DEBUG = False`)
- Environment variables for sensitive data
- Automatic HTTPS enabled

---

## 🧠 What I Learned

- Designing a real-world product from idea to production
- Building secure authentication-based systems
- Separating public and private application flows
- Deploying and maintaining a Django application in production
- Thinking like an end user, not just a developer

---

## 📷 Target Audience

Photographers who need a simple CRM solution to:
- Collect event details from clients
- Manage leads and customer information
- Automate repetitive communication tasks

---

## 📬 Contact

Developed by **Adi Gross**  
GitHub: https://github.com/ADI1GROSS

---

⭐ If you are a recruiter or developer reviewing this project — feel free to explore the live demo or the codebase.
