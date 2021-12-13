def initialBooks():
    for book in bList:
        book = str(book).rstrip()
        firstTag = book.index("#")
        secondTag = firstTag+book[firstTag+1:].index("#")+1
        restricted = True
        if(book[secondTag+1:] == "True"):
            restricted =  True
        else:
            restricted = False
        bookList.append([str(book[:firstTag]),int(book[firstTag+1:secondTag]),restricted,0, int(book[firstTag+1:secondTag])])

def addBook(book):
    firstTag = book.index("#")
    secondTag = firstTag+book[firstTag+1:].index("#")+1
    toAdd = True
    for element in bookList:
        toAdd = True
        if book[secondTag+1:] == element[0]:
            element[1] += 1
            element[4] += 1
            toAdd = False
            break
    if(toAdd):
        bookList.append([str(book[secondTag+1:]), 1, False, 0])

def borrowBook(book):
    firstTag = book.index("#")
    secondTag = firstTag+book[firstTag+1:].index("#")+1
    thirdTag = secondTag+book[secondTag+1:].index("#")+1
    fourthTag = thirdTag+book[thirdTag+1:].index("#")+1
    found = False
    hasFine = False
    for fine in fineList:
        if # finish this
    for element in bookList:
        if book[thirdTag+1:fourthTag] == element[0]:
            if element[1] == 0:
                found = False
            else:
                found = True
                element[1] -= 1
    if found:
        borrowList.append([str(book[thirdTag+1:fourthTag]),str(book[secondTag+1:thirdTag]),
                   int(book[firstTag+1:secondTag]),int(book[fourthTag+1:])])
    else:
        print("We dont have that book, can't be borrowed")

def returnBook(book):
    firstTag = book.index("#")
    secondTag = firstTag+book[firstTag+1:].index("#")+1
    thirdTag = secondTag+book[secondTag+1:].index("#")+1
    for element in borrowList:
        if element[0] == book[thirdTag+1:] and element[1] == book[secondTag+1:thirdTag]:
            if element[3] > int(book[firstTag+1:secondTag])-(element[2]+element[3]):
                restricted = True
                for x in bookList:
                    if x[0] == book[thirdTag+1:]:
                        restricted = x[2]
                if restricted:
                    for person in fineList:
                        if person == book[secondTag+1:thridTag]:
                            book[1] += (int(book[firstTag+1:secondTag])-(element[2]+element[3]))*5]
                        else:
                            fineList.append([book[secondTag+1:thirdTag],(int(book[firstTag+1:secondTag])-(element[2]+element[3]))*5])
                else:
                    for person in fineList:
                        if person == book[secondTag+1:thridTag]:
                            book[1] += (int(book[firstTag+1:secondTag])-(element[2]+element[3]))*5]
                        else:
                            fineList.append([book[secondTag+1:thirdTag],(int(book[firstTag+1:secondTag])-(element[2]+element[3]))])

def libraryReader():


def tallyBook(days, bookName):
    True
def endTally():
    True
def mostPopular():
    True

def ratioBook():
    for book in bookList:
        book.append(float(book[4]/book[3]))

bList = open("Booklist.txt","r")
lLog = open("librarylog.txt", "r")

bookList = [] # [book name, num of copies, restriction, tally, total copies]
tallyList = [] # [book name, tally#]
fineList = [] # [person name, amount]
borrowList = [] # [book name, person name, day borrowed, days allowed]

currentDay = 0

initialBooks()
print(bookList)
addBook("A#1#Mice of Men")
addBook("A#1#Enders Game")
print(bookList)
borrowBook("B#1#adam#harry potter#6")
borrowBook("B#2#ben#Dune#10")
returnBook("R#10#adam#harry potter")
print(bookList)
print(borrowList)
print(fineList)

#Ben is a friend  of mine

