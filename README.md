# 📇 Digital Contact Book — Modern Desktop Edition

A modernized, high-performance desktop contact management system built using **Python 3**, **CustomTkinter**, and a resilient **Dual-Engine Database (PostgreSQL + SQLite Auto-Fallback)**.

---

## ✨ Features

- **🎨 Modern Single-Window UI**:
  - Unified two-column desktop interface with sidebar navigation and responsive viewport.
  - Consistent modern dark and light mode themes with polished rounded cards and typography.
- **📊 Interactive Dashboard**:
  - Real-time metric cards displaying total contacts, family, work, and friends counts.
  - Quick action shortcuts and recent contacts list.
- **👥 Dynamic Contacts Directory**:
  - **Live Search**: Filter contacts instantly as you type by name, phone number, or email.
  - **Category Pills**: Filter by groups (All, Family, Work, Friends, Other).
  - **Initials Avatars**: Deterministic, vibrant avatar generator for every contact.
  - **Quick Actions**: One-click phone/email copying to clipboard, in-place edit, and soft delete.
- **➕ Smart Add & Edit View**:
  - Live initials avatar preview reflecting the contact name in real time.
  - Phone number validation and digit formatting.
  - Form validation with floating feedback notifications.
- **🗑️ Recycle Bin (Trash Recovery)**:
  - Soft-delete protection prevents accidental data loss.
  - 1-click contact restoration or permanent removal.
- **🗄️ Dual-Engine Database Resilience**:
  - Automatically attempts connection to PostgreSQL.
  - If PostgreSQL is offline or unreachable, seamlessly falls back to embedded SQLite (`contacts.db`) with zero manual configuration.

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- Install dependencies:
  ```bash
  pip install customtkinter psycopg2-binary
  ```

### 2. Run the Application
Launch the application by executing:
```bash
python3 main.py
```

---

## 📁 Project Structure

```
Digital-contact-Book/
├── main.py          # Application entry point, layout, and sidebar navigation
├── config.py        # Database manager (PostgreSQL + SQLite fallback) and root app config
├── theme.py         # Color palette, group styles, and avatar generator
├── dashboard.py     # Dashboard view with metrics and recent contacts
├── view.py          # Contacts directory, live search, and recycle bin
├── add.py           # Add and edit contact views with live avatar preview
├── setting.py       # Theme switcher, database status, and app info
├── events.py        # Upcoming events and birthday tracker
└── contacts.db      # SQLite local database
```

---

## 👥 Authors
Created by **Sahil, Litto and Anant**.

---

## 📜 License
Licensed under the [MIT License](LICENSE).
