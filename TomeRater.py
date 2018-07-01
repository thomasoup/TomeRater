import weakref

class User(object):
    def __init__(self, name, email):
        self.name = name #this will be a string
        self.email = email #this will be a string
        self.books = {} #this will map a book object

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print("User's email has been updated")

    def __repr__(self):
        number_of_books_red = len(self.books)
        return "User {user}, email {email}, books read: {books_red}".format(user = self.name, email = self.email, books_red = number_of_books_red)

    def __eq__(self, other_user):
        if other_user.name == self.name:
            return other_user.email == self.email

    def read_book(self, book, rating = "None"):
        self.books[book] = rating

    def get_average_rating(self):
        total = 0
        average = 0
        for i in self.books:
            if self.books[i] != "None":
                total += self.books[i]
            else:
                continue
        if len(self.books.values()) > 0:
            average = total / len(self.books.values())
        return average



class Book(object):
    instances = set()

    def __init__(self, title, isbn, price = 0):
        self.title = title #this will be a string
        self.isbn = isbn #this will be a number
        self.instances.add(weakref.ref(self))
        self.rating = []
        self.price = price

    def isIsbnExist(self, isbn):
        print(isbn)
        if len(Book.instances) > 0:
            isbn_list = []
            for book in Book.instances:
                book = book()
                isbn_list.append(book.isbn)
            return isbn in isbn_list
        else:
            return False

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print("the book's ISBN has been updated")

    def add_rating(self, rating):
        if rating >= 0 and rating <= 4:
            self.rating.append(rating)
        else:
            print("invalid Rating. Please enter a rating between 0 and 4 both included")

    def __eq__(self, other_book):
        if other_book.title == self.title:
            return other_book.isbn == self.isbn

    def get_average_rating(self):
        total = 0
        average = 0
        for i in self.rating:
            total += i
        if len(self.rating) > 0:
            average = total / len(self.rating)
        return average

    def __hash__(self):
        return hash((self.title, self.isbn))


class Fiction(Book):
    def __init__(self, title, author, isbn, price = 0):
        super().__init__(title, isbn, price)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{title} by {author}".format(title = self.title, author = self.author)

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn, price = 0):
        super().__init__(title, isbn, price)
        self.subject = subject #this will be a string
        self.level = level #this will be a string

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{title}, a {level} manual on {subject}".format(title = self.title, level = self.level, subject = self.subject)

class TomeRater(object):
    MessageIsbnAlreadyExists = "Sorry, this ISBN already exists, please choose another ISBN for this book"
    MessageUserAlreadyExists = "This user already exists. Please, choose add_book_to_user function in order to add book to this reader! Thanks mate"
    bookCreationDictionnary = {}

    def __init__(self):
        self.users = {} #this will map a user's email to the cooresponding User obeject
        self.books = {} #this will map a Book object to the number of Users that have read it

    def create_book(self, title, isbn, price = 0):
        if Book.isIsbnExist(self, isbn) == False:
            print("I am hereeeeeeeeeeeeeeeeeeeeeeeeeee")
            print(title)
            print(isbn)
            print(price)
            return Book(title, isbn, price)
        else:
            print(TomeRater.MessageIsbnAlreadyExists)

    def create_novel(self, title, author, isbn, price = 0):
        print("ATTENTION ATTENTION")
        if Book.isIsbnExist(self, isbn) == False:
            print("ah ah je t'a eu")
            print(Book.isIsbnExist(self, isbn))
            return Fiction(title, author, isbn, price)
        else:
            print(TomeRater.MessageIsbnAlreadyExists)

    def create_non_fiction(self, title, subject, level, isbn, price = 0):
        if Book.isIsbnExist(self, isbn) == False:
            return Non_Fiction(title, subject, level, isbn, price)
        else:
            print(TomeRater.MessageIsbnAlreadyExists)

    def add_book_to_user(self, book, email, rating = "None"):
        try:
            self.users[email]
            try:
                book.isbn
                self.users[email].read_book(book, rating)
                if rating != "None":
                    book.add_rating(rating)
                try:
                    self.books[book]
                    self.books[book] += 1
                except KeyError:
                    self.books[book] = 1
            except AttributeError:
                print("sorry the following book \"{book}\" could not be added to the user as it needs to be created first.".format(book = book))
        except KeyError:
            print("No user with email {email}".format(email = email))

    def add_user(self, name, email, user_books = "None"):
        try:
            self.users[email]
            print(TomeRater.MessageUserAlreadyExists)
        except KeyError:
            checkList = ["@", ".edu", '.org', '.com', '.try']
            sensor = 1
            needMessage = True
            while sensor < len(checkList):
                if checkList[0] in email and checkList[sensor] in email:
                    self.users[email] = User(name, email) #adds the email as Key in dictionnary of the class and add the User class as value
                    if user_books != "None":
                        for i in user_books:
                                self.add_book_to_user(i, email)
                    needMessage = False
                    break
                else:
                    sensor += 1
                    continue
            if needMessage == True:
                extension = ""
                for i in checkList[1:]:
                    extension += "\"" + i + "\" "
                print("Please check the email address of user and make sure it has the following characheters: \"@\" and one of the following extension: " + extension)
                #first test "\""
                # for check in checklist message = please check that you have and the following email extension " " + "\"" check +  "\"" + ","
                #print("Please check the email address of user and make sure it has the following characheters: \"@\" and \".edu\" \".com\" \".org\" ")


    def print_catalog(self):
        for i in self.books.keys():
            print(i.title)

    def print_users(self):
        for i in self.users.values():
            print(i)

    def get_most_read_book(self):
        total = 0
        most_read_book = ""
        for i in self.books:
            if self.books[i] > total:
                most_read_book = i.title
                total = self.books[i]
        return most_read_book

    def highest_rated_book(self):
        highest_average = 0
        highest_rated_book = ""
        for i in self.books:
            average_rating = i.get_average_rating()
            if average_rating > highest_average:
                highest_average = average_rating
                highest_rated_book = i.title
        return highest_rated_book

    def most_positive_user(self):
        highest_average = 0
        highest_positive_user = ""
        for i in self.users.values():
            average_rating = i.get_average_rating()
            if average_rating > highest_average:
                highest_average = average_rating
                highest_positive_user = i
        return highest_positive_user

    def get_n_most_read_books(self, n = 0):
        total = 0
        new_dict = dict(self.books)
        ordered_lst = []
        sensor = 1
        if n <= len(new_dict) and n >= sensor:
            while sensor <= n:
                for i in new_dict:
                    if new_dict[i] > total:
                        value = i.title
                        valueToRemove = i
                        total = self.books[i]
                        print(i)
                ordered_lst.append(value)
                new_dict.pop(valueToRemove)
                total = 0
                sensor += 1
            return ordered_lst
        else:
            return "Please choose a number between 1 and {number} both included".format(number = len(new_dict))

    def get_n_most_prolific_user(self, n = 0):
        total = 0
        temp_dic = dict(self.users)
        mostProlificUsers = []
        if n <= len(temp_dic) and len(temp_dic) > 0:
            while len(temp_dic) != 0:
                for user in temp_dic:
                    if len(temp_dic[user].books) > total:
                        value = temp_dic[user]
                        valueToRemove = user
                        total = len(temp_dic[user].books)
                mostProlificUsers.append(value)
                temp_dic.pop(valueToRemove)
                total = 0
            return mostProlificUsers[0: n]
        elif len(temp_dic) == 0:
            return "Your request cannot be processed since no users have been created. Pease create users before calling this request."
        else:
            return 'Your request exceed the number of users in the databse. Please choose a number between 1 and {number} both included'.format(number = len(temp_dic))
        #message for number of users lije the number of books red

    def get_n_most_expensive_books(self, n=4):
        total = -1
        temp_dic = {}
        price_lst = []
        book_name = []
        if len(Book.instances) > 0:
            for book in Book.instances:
                book = book()
                temp_dic[book.title] = book.price
            print(temp_dic)
            while len(temp_dic) != 0:
                for book in temp_dic:
                    #print(temp_dic)
                    if temp_dic[book] > total:
                        title_to_add = book
                        valueToRemove= book
                        price_to_add = temp_dic[book]
                        total = temp_dic[book]
            #            print(total)
                book_name.append(title_to_add)
                price_lst.append(price_to_add)
                temp_dic.pop(valueToRemove)
                total = -1
            nameAndPriceLst = list(zip(book_name, price_lst))
            print(nameAndPriceLst)
            if n <= len(nameAndPriceLst):
                for tuple in range(0, n):
                    sensor = 0
                    book = ""
                    price = 0
                    for item in nameAndPriceLst[tuple]:
                        if sensor == 0:
                            book = item
                            sensor = 1
                        else:
                            price = item
                            sensor = 0
                    print("The book's name is \"{book}\" coming with the following price ${price}".format(book = book, price = price))
                return "End of list"
            else:
                return "Please choose a number between 1 and {n} boh included".format(n = len(nameAndPriceLst))
        else:
            return "The book catalog is empty, please create some books first"

    def get_worth_of_user(self, user_email):
        try:
            self.users[user_email]
            total = 0
            for i in self.users[user_email].books:
                for book in Book.instances:
                    book = book()
                    if book.title == i.title:
                        value = book.price
                        total += value
            return "The sum of all costs of books read by {user} is ${value}".format(user = self.users[user_email].name, value = total)
        except KeyError:
            return "Sorry there is no user with this email address or no email address has been provided. Please check the provided email address"

    def __repr__(self):
        return "The most read book is \'{book_most_red}\' and the highest rated book is \'{book_highest_rated}\'. The most positive reader is \'{user}\'"\
        .format(book_most_red = self.get_most_read_book(), book_highest_rated = self.highest_rated_book(), user = self.most_positive_user())

    def MainMenu(self):
        print("Welcome to Tomerater. What would you like to do? Please select one of the following \
         \n [1] Print catalog \n [2] Print users \n [3] Create a book \n [4] Add user \n [5] Add book to user \n [6] Get most read book \
          \n [7] Get highest rated book \n [8] Get most positive user \n [9] Get n most read book \n [10] Get n most prolific users\
          \n [11] Get n most expensive books \n [12] Get worth of user \n [13] Print TomeRater \n [14] Exit")
        n = input()
        print(n)
        if n == "1":
            print("Please find below the catalog but note that only books that have been already read one time are there")
    #        book = self.bookCreationDictionnary["thomasplaya"]
    #        self.add_user("jean-pierre pernau", "JP@hothot.com", [book])
            self.print_catalog()
            print("")
            self.MainMenu()
        elif n == "2":
            self.print_users()
            print("")
            self.MainMenu()
        elif n == "3":
            self.MenuCreateBook()
        elif n == "4":
            self.MenuAddUser()
        elif n == "5":
            self.MenuAddBookToUser()
        elif n == "6":
            print(self.get_most_read_book())
            print("")
            self.MainMenu()
        elif n == "7":
            print(self.highest_rated_book())
            print("")
            self.MainMenu()
        elif n == "8":
            print(self.most_positive_user())
            print("")
            self.MainMenu()
        elif n == "9":
            self.MenuGetMostObjects(9)
        elif n == "10":
            self.MenuGetMostObjects(10)
        elif n == "11":
            self.MenuGetMostObjects(11)
        elif n == "12":
            self.MenuGetWorthOfUser()
        elif n == "13":
            print(self)
            print("")
            self.MainMenu()
        elif n == "14":
            print("End")
        else:
            print("Sorry, you selection is not valid, choose between the number given in the options")
            print("")
            self.MainMenu()


    def MenuCreateBook(self):
        print("Please, write the title of the book")
        title = str(input())
        print("Please give the ISBN of the book")
        isbn = input()
        sensor = 0
        while sensor == 0:
            try:
             int(isbn)
             sensor = 1
            except ValueError:
                print("Sorry your input is not valid. Pease insert a number")
                print("Please give the ISBN of the book")
                isbn = input()
        print("Please give the price of the book")
        price = input()
        sensor = 0
        while sensor == 0:
            try:
             int(price)
             sensor = 1
            except ValueError:
                print("Sorry your input is not valid. Pease insert a number")
                print("Please give the price of the book")
                price = input()
        print('what reference name would you like to use for the book? Please answer without space')
        name = input().replace(" ", "")
        print(self.bookCreationDictionnary)
        booktocreate = self.create_book(title, int(isbn), int(price))
        try:
            booktocreate.isbn
            self.bookCreationDictionnary[name] = booktocreate
            self.MainMenu()
        except AttributeError:
            print("Sorry the book could not have been created")
            self.MainMenu()

    def MenuAddUser(self):
        print("What is the name of the user?")
        name = input()
        print("Please give the email addres of the user")
        email = input()
        print("Would you like to add book to this user? \n [1] Yes \n [2] No")
        n = input()
        booklst = []
        bookToAdd = []
        if n == "1":
            sensor = 0
            while sensor == 0:
                for book in self.bookCreationDictionnary.keys():
                    booklst.append(book)
                print("Please choose one of the following book to add to the user (without strings)")
                print(booklst)
                book = input()
                if book in booklst:
                    bookToAdd.append(self.bookCreationDictionnary[book])
                    sensor = 1
                else:
                    print("Sorry your selection is not valid. Please choose a book among the list")
                    booklst = []
        if len(bookToAdd) > 0:
            self.add_user(name, email, bookToAdd)
        else:
            self.add_user(name, email)
        self.MainMenu()

    def MenuAddBookToUser(self):
        sensor = 0
        booklst = []
        while sensor == 0:
            for book in self.bookCreationDictionnary.keys():
                booklst.append(book)
            print("Please choose amoong the list, the book you would like to add (without string)")
            print(booklst)
            book = input()
            if book in booklst:
                bookToAdd = self.bookCreationDictionnary[book]
                sensor = 1
            else:
                print("sorry your entry is not correct. Please choose a book among the list")
                booklst = []
        sensor = 0
        userlst = []
        while sensor == 0:
            for user in self.users.keys():
                userlst.append(user)
            print("Please choose among the following email address the one you would like to choose (without string)")
            print(userlst)
            user = input()
            if user in userlst:
                userToSelect = user
                sensor = 1
            else:
                print("Sorry your entry is not valid. please check the email address in the list")
                userlst = []
        print("do you want to add a rating? \n [1] Yes \n [2] No")
        n = input()
        sensor = 0
        if n == "1":
            print("Please give the rating of the book between 0 and 4 both included")
            rating = input()
            while sensor == 0:
                try:
                    int(rating)
                    ratingToAdd = int(rating)
                    if ratingToAdd < 0 or ratingToAdd > 4:
                        print("Sorry insert a number between 0 and 4 both included")
                        rating = input()
                    else:
                        sensor = 1
                except ValueError:
                    print("Sorry your input is not valid. Pease insert a number")
                    print("Please give the rating of the book")
                    rating = input()
        else:
            ratingToAdd = "None"
        self.add_book_to_user(bookToAdd, userToSelect, ratingToAdd)
        self.MainMenu()

    def MenuGetMostObjects(self, x):
        print("How many books would you like to have on your list? Please insert a number")
        n = input()
        sensor = 0
        while sensor == 0:
            try:
                int(n)
                if x == 9:
                    print(self.get_n_most_read_books(int(n)))
                elif x == 10:
                    print(self.get_n_most_prolific_user(int(n)))
                else:
                    print(self.get_n_most_expensive_books(int(n)))
                sensor = 1
            except ValueError:
                print("sorry your entry is not valid. Please insert a number")
                n = input()
        self.MainMenu()

    def MenuGetWorthOfUser(self):
        userlst = []
        for user in self.users.keys():
            userlst.append(user)
        print("Please choose among the following email address the one you would like to know the value (without string)")
        print(userlst)
        user = input()
        print(self.get_worth_of_user(user))
        self.MainMenu()



Tome_Rater = TomeRater()
#cerate some books:
Tome_Rater.bookCreationDictionnary["book1"] = Tome_Rater.create_book("Society of Mind", 12345678, 20)
Tome_Rater.bookCreationDictionnary["novel1"] = Tome_Rater.create_novel("Alice In Wonderland", "Lewis Carroll", 12345, 15)
Tome_Rater.bookCreationDictionnary["notification1"] = Tome_Rater.create_non_fiction("Automate the Boring Stuff", "Python", "beginner", 1929452, 23)
Tome_Rater.bookCreationDictionnary["notification2"] = Tome_Rater.create_non_fiction("Computing Machinery and Intelligence", "AI", "advanced", 11111938, 44)
Tome_Rater.bookCreationDictionnary["novel2"] = Tome_Rater.create_novel("The Diamond Age", "Neal Stephenson", 10101010, 12)
Tome_Rater.bookCreationDictionnary["novel3"] = Tome_Rater.create_novel("There Will Come Soft Rains", "Ray Bradbury", 10001000, 7)

#create users:
Tome_Rater.add_user("Alan Turing", "alan@turing.com")
Tome_Rater.add_user("David Marr", "david@computation.org")

#add a user with three books already read:
Tome_Rater.add_user("Marvin Minsky", "marvin@mit.edu", user_books=[Tome_Rater.bookCreationDictionnary["book1"], Tome_Rater.bookCreationDictionnary["novel1"], Tome_Rater.bookCreationDictionnary["notification1"]])

#add books to a user one by one, with ratings:
Tome_Rater.add_book_to_user(Tome_Rater.bookCreationDictionnary["book1"], "alan@turing.com", 1)
Tome_Rater.add_book_to_user(Tome_Rater.bookCreationDictionnary["novel1"], "alan@turing.com", 3)
Tome_Rater.add_book_to_user(Tome_Rater.bookCreationDictionnary["notification1"], "alan@turing.com", 3)
Tome_Rater.add_book_to_user(Tome_Rater.bookCreationDictionnary["notification2"], "alan@turing.com", 4)
Tome_Rater.add_book_to_user(Tome_Rater.bookCreationDictionnary["novel3"], "alan@turing.com", 1)
Tome_Rater.add_book_to_user(Tome_Rater.bookCreationDictionnary["novel2"], "marvin@mit.edu", 2)
Tome_Rater.add_book_to_user(Tome_Rater.bookCreationDictionnary["novel3"], "marvin@mit.edu", 2)
Tome_Rater.add_book_to_user(Tome_Rater.bookCreationDictionnary["novel3"], "david@computation.org", 4)

print("Here is the catalog of TomeRater:")
Tome_Rater.print_catalog()
print("")

print("Here is the list of users:")
Tome_Rater.print_users()
print("")

print("Here is what happens when we want to create a book with an existing ISBN. The try is to create a book2 called \"\" Sneaky ISBN \"\" with the existing ISBN: 12345678")
Tome_Rater.bookCreationDictionnary["book2"] = Tome_Rater.create_book("Sneaky ISBN", 12345678, 28)
print("")

print("Here is what happens when we try to create a user with an invalid email address. The try is to create a user with the emal address: user@doesnotwork.fail:")
Tome_Rater.add_user("User", "user@doesnotwork.self.fail")
print("")

print("Here is what happens when we want to add a user that alrady exists:")
Tome_Rater.add_user("Alan Turing", "alan@turing.com")
print("")

print("Here is the most read book:")
print(Tome_Rater.get_most_read_book())
print("")

print("Here is the highest_rated_book:")
print(Tome_Rater.highest_rated_book())
print("")

print("Here is the most positive user:")
print(Tome_Rater.most_positive_user())
print("")

print("Here are the 3 most read books:")
print(Tome_Rater.get_n_most_read_books(3))
print("")

print("Here are the 2 most prolific users:")
print(Tome_Rater.get_n_most_prolific_user(2))
print("")

print("Here are the 4 most expensive books:")
print(Tome_Rater.get_n_most_expensive_books(4))
print("")

print("Here is the worth value of the user: Alan Turing with email address: alan@turing.com:")
print(Tome_Rater.get_worth_of_user("alan@turing.com"))
print("")

print("Here how TomeRater looks like when it is printed:")
print(Tome_Rater)
print("")

Tome_Rater.MainMenu()

"""
ideas
Ask the user to decide what he wants to do and get the most efficient books on a certain topic"
Put some introduction sentence before outputs
sorted elements?
add commments of book in string in string

add a message about number of users for the most prolific Users

do the 2 last functions about price of books
try to create a chatboat and see if I add extra stuff like comment (? not so sure) tu prends un bouquin et tu cherche dans chaque user. comments si le bouquin est là est tu affiche le comment
OU autre idee c'est de chercher les utilisateur qui ont donné un certain rating au bouquin et d'afficher les commentaires. dans user creer dico avec livre qui renvoie à une liste de valeur [ratin, comment]
Put some introduction sentence before outputs
add comments and clean
upload
"""
