# 📘 StudyMate

**StudyMate** is a desktop-based educational management system built using **Python** and **PyQt5** that provides dedicated dashboards for **Students** and **Professors**. It allows seamless interaction between students and educators for academic tasks like managing assignments, quizzes, course materials, and notifications.

## 🎯 Project Features

### 👨‍🏫 Professor Dashboard
- View dashboard summary (total quizzes, assignments, notifications).
- **Create Assignments** with title, description, and deadline.
- **Add Quizzes** to test students.
- **Upload Course Material** (PDFs, videos, etc.).
- **Send Notifications** (e.g., important updates or alerts).
- Manage and track saved assignments.

### 👩‍🎓 Student Dashboard
- View personalized welcome message.
- See a summary of:
  - 📝 Due Assignments Count
  - 📚 Due Quizzes Count
  - 📊 Grades
  - 🔔 Notifications
- Real-time rendering of all assignments and deadlines.
- Notifications section for important professor messages.

---

## 🛠️ Tech Stack

- **Language**: Python 3
- **GUI Framework**: PyQt5
- **UI Design**: QWidgets, QVBoxLayout, QStackedWidget
- **Data Handling**: Python lists & dictionaries (no database used for now)

---

## 🚀 How to Run

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/StudyMate.git
   cd StudyMate

2. **Install dependencies**

   ```bash
   pip install PyQt5
   ```

3. **Run the main file**

   ```bash
   python main.py
   ```

---

## 📂 Project Structure


StudyMate/
│
├── main.py                    # Entry point of the application
├── student_dashboard.py       # Student dashboard logic and UI
├── professor_dashboard.py     # Professor dashboard logic and UI
├── utils/
│   └── assignments.py         # Assignment data and logic (list-based)
├── assets/                    # Icons, images, and static files (optional)
└── README.md                  # Project documentation


