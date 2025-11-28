import streamlit as st
import json
import random
import string
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------
# BACKEND LIBRARY CLASS (SAME LOGIC AS YOUR TERMINAL VERSION)
# ---------------------------------------------------------

class Library:
    database = "library.json"
    data = {"books": [], "members": []}

    # Load data on startup
    if Path(database).exists():
        with open(database, "r") as fs:
            content = fs.read().strip()
            if content:
                data = json.loads(content)
    else:
        with open(database, "w") as fs:
            json.dump(data, fs, indent=4)

    @classmethod
    def save_data(cls):
        with open(cls.database, 'w') as fs:
            json.dump(cls.data, fs, indent=4, default=str)

    @staticmethod
    def gen_id(prefix="B"):
        return prefix + "-" + "".join(
            random.choice(string.ascii_uppercase + string.digits)
            for _ in range(5)
        )

    # Add a book
    def add_book(self, title, author, copies):
        book = {
            "id": Library.gen_id(),
            "title": title,
            "author": author,
            "total_copies": copies,
            "available_copies": copies,
            "added_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        Library.data["books"].append(book)
        Library.save_data()

    # Add a member
    def add_member(self, name, email):
        member = {
            "id": Library.gen_id("M"),
            "name": name,
            "email": email,
            "borrowed": []
        }
        Library.data["members"].append(member)
        Library.save_data()

    # Borrow a book
    def borrow_book(self, member_id, book_id):
        members = [m for m in Library.data["members"] if m["id"] == member_id]
        if not members:
            return False, "Member not found"
        member = members[0]

        books = [b for b in Library.data["books"] if b["id"] == book_id]
        if not books:
            return False, "Book not found"
        book = books[0]

        if book["available_copies"] <= 0:
            return False, "No copies available"

        borrow_data = {
            "book_id": book["id"],
            "title": book["title"],
            "borrow_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        member["borrowed"].append(borrow_data)
        book["available_copies"] -= 1
        Library.save_data()
        return True, "Book borrowed successfully"

    # Return a book
    def return_book(self, member_id, borrowed_index):
        members = [m for m in Library.data["members"] if m["id"] == member_id]
        if not members:
            return False, "Member not found"

        member = members[0]

        if borrowed_index >= len(member["borrowed"]):
            return False, "Invalid selection"

        selected = member["borrowed"].pop(borrowed_index)

        books = [b for b in Library.data["books"] if b["id"] == selected["book_id"]]
        if books:
            books[0]["available_copies"] += 1

        Library.save_data()
        return True, "Book returned successfully"


lib = Library()

# ---------------------------------------------------------
# STREAMLIT UI
# ---------------------------------------------------------

st.set_page_config(page_title="Library Management System", layout="wide")

st.title("📚 Library Management System")

menu = st.sidebar.radio(
    "Navigation",
    ["Add Book", "List Books", "Add Member", "List Members", "Borrow Book", "Return Book"]
)

# ---------------------------------------------------------
# ADD BOOK
# ---------------------------------------------------------
if menu == "Add Book":
    st.header("➕ Add a New Book")
    
    title = st.text_input("Book Title")
    author = st.text_input("Author Name")
    copies = st.number_input("Number of Copies", min_value=1, step=1)

    if st.button("Add Book"):
        lib.add_book(title, author, copies)
        st.success("Book added successfully!")


# ---------------------------------------------------------
# LIST BOOKS
# ---------------------------------------------------------
elif menu == "List Books":
    st.header("📘 All Books")

    if not lib.data["books"]:
        st.warning("No books found.")
    else:
        st.table(lib.data["books"])


# ---------------------------------------------------------
# ADD MEMBER
# ---------------------------------------------------------
elif menu == "Add Member":
    st.header("👤 Add New Member")

    name = st.text_input("Member Name")
    email = st.text_input("Email ID")

    if st.button("Add Member"):
        lib.add_member(name, email)
        st.success("Member added successfully!")


# ---------------------------------------------------------
# LIST MEMBERS
# ---------------------------------------------------------
elif menu == "List Members":
    st.header("👥 Members List")

    if not lib.data["members"]:
        st.warning("No members found.")
    else:
        for m in lib.data["members"]:
            st.subheader(f"{m['name']} ({m['id']})")
            st.write(f"📧 {m['email']}")
            st.write("Borrowed Books:")
            st.json(m["borrowed"])
            st.markdown("---")


# ---------------------------------------------------------
# BORROW BOOK 
# ---------------------------------------------------------
elif menu == "Borrow Book":
    st.header("📖 Borrow a Book")

    # Create display-friendly dropdown labels
    member_options = {
        m["id"]: f"{m['name']}  ({m['id']})"
        for m in lib.data["members"]
    }

    book_options = {
        b["id"]: f"{b['title']} - {b['author']}  ({b['id']}) | Available: {b['available_copies']}"
        for b in lib.data["books"]
    }

    if not member_options:
        st.error("No members available!")
    elif not book_options:
        st.error("No books available!")

    else:
        member_id = st.selectbox(
            "Select Member",
            list(member_options.keys()),
            format_func=lambda x: member_options[x]
        )

        book_id = st.selectbox(
            "Select Book",
            list(book_options.keys()),
            format_func=lambda x: book_options[x]
        )

        if st.button("Borrow"):
            status, msg = lib.borrow_book(member_id, book_id)
            if status:
                st.success(msg)
            else:
                st.error(msg)



# ---------------------------------------------------------
# RETURN BOOK 
# ---------------------------------------------------------
elif menu == "Return Book":
    st.header("📤 Return a Book")

    members = {m["id"]: m for m in lib.data["members"]}

    if not members:
        st.error("No members available to return books.")

    # Member dropdown with improved display
    member_dropdown = {
        m_id: f"{members[m_id]['name']} ({m_id})"
        for m_id in members
    }

    member_id = st.selectbox(
        "Select Member",
        list(member_dropdown.keys()),
        format_func=lambda x: member_dropdown[x]
    )

    selected_member = members[member_id]
    borrowed = selected_member["borrowed"]

    # Build book return display labels
    borrowed_books_labels = [
        f"{b['title']} ({b['book_id']}) | Borrowed On: {b['borrow_on']}"
        for b in borrowed
    ]

    if not borrowed_books_labels:
        st.warning("This member has no borrowed books.")

    else:
        index = st.selectbox(
            "Select Book to Return",
            list(range(len(borrowed_books_labels))),
            format_func=lambda x: borrowed_books_labels[x]
        )

        if st.button("Return Book"):
            status, msg = lib.return_book(member_id, index)
            if status:
                st.success(msg)
            else:
                st.error(msg)
