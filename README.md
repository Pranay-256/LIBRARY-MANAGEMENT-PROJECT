# LIBRARY-MANAGEMENT-PROJECT

This project is a Library Management System built using Python and Streamlit, designed to manage books, members, and borrowing/return operations.
It uses a lightweight JSON file as the database, making it easy to run without any external setup. The main.py file was used to write the core logic of the code and the app.py file is the transformed GUI version of that code with the help of streamlit library of python created with the help of CURSOR AI.

# FEATURES

🔹 Book Management

Add new books with title, author, and copies.

View complete list of books with availability status.

Each book gets a unique auto-generated ID.

🔹 Member Management

Add new members with name and email.

List all members along with borrowed book history.

Each member receives a unique Member ID.

🔹 Borrowing System

Borrow books through an interactive dropdown.

Dropdown shows Book Title + Author + Book ID + Available Copies.

Member dropdown shows Member Name + Member ID.

Automatically updates available copies.

Stores borrow time and book details under the member.

🔹 Return System

Display all books borrowed by a selected member.

Return dropdown shows Book Title + Book ID + Borrow Date.

Automatically updates available copies and member history.

🔹 JSON Database

All data is stored in library.json.


| Technology    | Purpose                      |
| ------------- | ---------------------------- |
| **Python**    | Core language                |
| **Streamlit** | UI / Frontend                |
| **JSON**      | Lightweight backend database |
| **Pathlib**   | File handling                |
| **Datetime**  | Timestamp management         |





No SQL or external database required.

Fully portable and easy to back up.


to run install streamlit - 
write this in new terminal - pip install streamlit
and after installation write this in new terminal - python -m streamlit run app.py
