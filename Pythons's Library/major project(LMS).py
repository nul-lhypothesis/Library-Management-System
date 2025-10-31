import datetime

class LMS:
    def __init__(self, list_of_books, library_name):
        self.list_of_books = list_of_books
        self.library_name = library_name
        self.books_dict = {}
        id_count = 101
        try:
            with open(self.list_of_books, "r") as bk:
                content = bk.readlines()
                for line in content:
                    line = line.strip()
                    if line:
                        self.books_dict[str(id_count)] = {
                            "books_title": line,
                            "lender_name": "",
                            "Issue_date": "",
                            "Status": "Available"
                        }
                        id_count += 1
        except FileNotFoundError:
            print("Book list file not found. Make sure it exists in the folder.")

    # Display all books
    def display_books(self):
        print("\n----------------------------------------- LIST OF BOOKS -----------------------------------------")
        print("Book ID\t\tTitle")
        print("-------------------------------------------------------------------------------------------------")
        for key, value in self.books_dict.items():
            print(f"{key}\t\t{value['books_title']} - [{value['Status']}]")


    def Issue_books(self):
        book_id = input("Enter Book ID to issue: ").strip()
        if book_id in self.books_dict.keys():
            if self.books_dict[book_id]["Status"] == "Available":
                lender_name = input("Enter your name: ").strip()
                self.books_dict[book_id]["lender_name"] = lender_name
                self.books_dict[book_id]["Issue_date"] = datetime.date.today().strftime("%d-%m-%Y")
                self.books_dict[book_id]["Status"] = "Issued"
                print(f"\nBook '{self.books_dict[book_id]['books_title']}' has been issued to {lender_name}.")
            else:
                print(f"\nThis book is already issued to {self.books_dict[book_id]['lender_name']}.")
        else:
            print("Book ID not found. Please check again.")

    def add_books(self):
        new_books = input("Enter book title: ").strip()
        if new_books == "":
            print("Book title cannot be empty!")
            return self.add_books()
        elif len(new_books) > 50:
            print("BOOK TITLE TOO LONG! Keep it under 50 characters.")
            return self.add_books()
        else:
            with open(self.list_of_books, "a") as bk:
                bk.write(f"{new_books}\n")
            new_id = str(int(max(self.books_dict)) + 1)
            self.books_dict[new_id] = {
                "books_title": new_books,
                "lender_name": "",
                "Issue_date": "",
                "Status": "Available"
            }
            print(f"Book '{new_books}' added successfully!")

    def return_books(self):
        book_id = input("Enter Book ID to return: ").strip()
        if book_id in self.books_dict.keys():
            if self.books_dict[book_id]["Status"] == "Issued":
                self.books_dict[book_id]["lender_name"] = ""
                self.books_dict[book_id]["Issue_date"] = ""
                self.books_dict[book_id]["Status"] = "Available"
                print(f"\nBook '{self.books_dict[book_id]['books_title']}' returned successfully!")
            else:
                print("That book wasn’t issued.")
        else:
            print("Invalid Book ID!")

    def merge_sort(self, books):
        if len(books) > 1:
            mid = len(books)//2
            left = books[:mid]
            right = books[mid:]

            self.merge_sort(left)
            self.merge_sort(right)

            i = j = k = 0
            while i < len(left) and j < len(right):
                if left[i][1].lower() < right[j][1].lower():
                    books[k] = left[i]
                    i += 1
                else:
                    books[k] = right[j]
                    j += 1
                k += 1
            while i < len(left):
                books[k] = left[i]
                i += 1
                k += 1
            while j < len(right):
                books[k] = right[j]
                j += 1
                k += 1
        return books

    def merge_sort_books(self):
        books = [(key, value["books_title"], value["Status"]) for key, value in self.books_dict.items()]
        sorted_books = self.merge_sort(books)

        print("\n------------------------------------ SORTED BOOK LIST ------------------------------------")
        print("Book ID\t\tTitle")
        print("------------------------------------------------------------------------------------------")
        for b in sorted_books:
            print(f"{b[0]}\t\t{b[1]} - [{b[2]}]")

    def get_genre(self, title):
        title = title.lower()
        if any(word in title for word in ["gone girl", "girl on the train", "da vinci", "silent patient", "sharp objects", "big little lies", "couple next door"]):
            return "Mystery / Thriller"
        elif any(word in title for word in ["hobbit", "harry potter", "game of thrones", "witcher", "eragon", "percy jackson", "narnia"]):
            return "Fantasy / Adventure"
        elif any(word in title for word in ["pride and prejudice", "gatsby", "mockingbird", "book thief", "les mis", "anna karenina", "war and peace"]):
            return "Historical / Classic"
        elif any(word in title for word in ["1984", "brave new world", "fahrenheit", "maze runner", "dune", "left hand of darkness", "neuromancer"]):
            return "Sci-Fi / Dystopian"
        elif any(word in title for word in ["meluha", "nagas", "vayuputras", "circe", "norse mythology", "achilles", "iliad"]):
            return "Mythology / Epic"
        elif any(word in title for word in ["dracula", "frankenstein", "shining", "haunting", "interview with the vampire", "it ", "woman in black"]):
            return "Horror / Supernatural"
        elif any(word in title for word in ["bossypants", "good omens", "catch-22", "hitchhiker", "rosie project", "yes please", "me talk pretty"]):
            return "General / Others"
        else:
            return "General / Others"

    def browse_by_genre(self):
        genres = [
            "General / Others",
            "Fantasy / Adventure",
            "Historical / Classic",
            "Sci-Fi / Dystopian",
            "Mythology / Epic",
            "Horror / Supernatural",
            "Mystery / Thriller"
        ]

        print("\n-------------------- AVAILABLE GENRES --------------------")
        for i, g in enumerate(genres, start=1):
            print(f"{i}. {g}")

        try:
            choice = int(input("\nEnter the number of the genre you want to browse: "))
            if 1 <= choice <= len(genres):
                selected = genres[choice - 1]
                print(f"\n-------------------- BOOKS IN {selected.upper()} --------------------")
                print("Book ID\t\tTitle")
                print("-------------------------------------------------------------")

                found = False
                for key, value in self.books_dict.items():
                    if self.get_genre(value["books_title"]) == selected:
                        print(f"{key}\t\t{value['books_title']} - [{value['Status']}]")
                        found = True

                if not found:
                    print("No books found in this genre.")
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a valid number.")


try:
    myLMS = LMS("list_of_books.txt", "Python's")
    press_key_list = {
        "D": "Display Books",
        "I": "Issue Books",
        "A": "Add Books",
        "R": "Return Books",
        "S": "Sort Books (A–Z)",
        "G": "Browse Books by Genre",
        "Q": "Quit"
    }

    key_press = ""
    while key_press != "q":
        print(f"\n---------------------- Welcome to {myLMS.library_name} Library Management System ----------------------\n")
        for key, value in press_key_list.items():
            print("Press", key, "To", value)

        key_press = input("\nPress key: ").lower()

        if key_press == "d":
            print("\nCurrent Selection : Display Books\n")
            myLMS.display_books()
        elif key_press == "i":
            print("\nCurrent Selection : Issue Books\n")
            myLMS.Issue_books()
        elif key_press == "a":
            print("\nCurrent Selection : Add Books\n")
            myLMS.add_books()
        elif key_press == "r":
            print("\nCurrent Selection : Return Books\n")
            myLMS.return_books()
        elif key_press == "s":
            print("\nCurrent Selection : Sort Books\n")
            myLMS.merge_sort_books()
        elif key_press == "g":
            print("\nCurrent Selection : Browse Books by Genre\n")
            myLMS.browse_by_genre()
        elif key_press == "q":
            print("Exiting Library System... Goodbye!")
            break
        else:
            print("Invalid input! Try again.")

except Exception as e:
    print("Something went wrong. Please check your input or file.")
