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

def libraryRead():
    for x in lLog:
        task = str(x).rstrip()
        if(task[0]=="B"):
            borrowBook(task)
        elif(task[0]=="R"):
            returnBook(task)
        elif(task[0]=="P"):
            payFine(task)
        elif(task[0]=="A"):
            addBook(task)
        else:
            currentDay=int(task)

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
        bookList.append([str(book[secondTag+1:]), 1, False, 0, 1])

def borrowBook(book):
    firstTag = book.index("#")
    secondTag = firstTag+book[firstTag+1:].index("#")+1
    thirdTag = secondTag+book[secondTag+1:].index("#")+1
    fourthTag = thirdTag+book[thirdTag+1:].index("#")+1
    found = False
    hasFine = False
    for fine in fineList:
        if fine[0] == book[secondTag+1:thirdTag]:
            hasFine = True
    if not(hasFine):
        for element in bookList:
            if book[thirdTag+1:fourthTag] == element[0]:
                if element[1] == 0:
                    found = False
                else:
                    found = True
                    element[1] -= 1
    if not(hasFine) and found:
        borrowList.append([str(book[thirdTag+1:fourthTag]),str(book[secondTag+1:thirdTag]),
                   int(book[firstTag+1:secondTag]),int(book[fourthTag+1:])])
    else:
        #print("Can't be borrowed")

def tallyBook(days, bookName):
    for book in bookList:
        if(book[0] == bookName):
            book[3]+=days

def payFine(task):
    tag1=int(task.index("#"))
    tag2=int(task.find("#",tag1+1))
    tag3=int(task.find("#",tag2+1))
    person=task[tag2+1:tag3]
    day=task[tag1+1:tag2]
    paid=task[tag3+1]
    for x in fineList:
        if(x[0]==person):
            x[1]=x[1]-paid
        if(x[1]<=0):
            fineList.pop(x)

def endTally():
    for book in borrowList:
        for element in bookList:
            if(element[0] == book[0]):
                element[3]+=currentDay-book[2]

def returnBook(book):
    firstTag = book.index("#")
    secondTag = firstTag+book[firstTag+1:].index("#")+1
    thirdTag = secondTag+book[secondTag+1:].index("#")+1
    for element in borrowList:
        if element[0] == book[thirdTag+1:] and element[1] == book[secondTag+1:thirdTag]:
            tallyBook(int(book[firstTag+1:secondTag])-(element[2]), element[0])
            if element[3] > (int(book[firstTag+1:secondTag])-(element[2]+element[3])):
                addFine(int(book[firstTag+1:secondTag])-element[2], element[3], book[thirdTag+1:] ,book[secondTag+1:thirdTag])

def addFine(days, allowedDays, bookName, name):
    restricted = True
    for x in bookList:
        if x[0] == bookName:
            restricted = x[2]
    if restricted:
        for fine in fineList:
            if fine[0] == name:
                fine[1] += (days-allowedDays)*5
            else:
                fineList.append([name,(days-allowedDays)*5])
    else:
        for fine in fineList:
            if fine[0] == name:
                fine[1] += (days-allowedDays)
            else:
                fineList.append([name,days-allowedDays])

def endFine():
    for book in borrowList:
        for element in bookList:
            if(currentDay - book[2] < book[3]):
                if(element[0] == book[0]):
                    if(element[2]):
                        fine = (book[2] + book[3] - currentDay)*5
                        flag = True
                        for i in fineList:
                            if(book[1] == i[0]):
                                i[1]+= fine
                                flag = False
                        if(flag):
                            fineList.append([book[1],fine])
                    else:
                        fine = (book[2] + book[3] - currentDay)
                        flag = True
                        for i in fineList:
                            if(book[1] == i[0]):
                                i[1]+= fine
                                flag = False
                            if(flag):
                                fineList.append([book[1],fine])


def ratioBook():
    for book in bookList:
        book.append(float(book[4]/book[3]))

def mostPopular():
    currentName="none"
    currentMost=0
    for book in bookList:
         if(int(book[3])>currentMost):
             currentMost=int(book[3])
             currentName=book[0]
    #How do we want to output this function?

def ratioBook():
    for book in bookList:
        book.append(float(book[4]/book[3]))

bList = open("booklist-2.txt","r")
lLog = open("librarylog-3.txt", "r")

bookList = [] # [book name, num of copies, restriction, tally, total copies]
tallyList = [] # [book name, tally#]
fineList = [] # [person name, amount]
borrowList = [] # [book name, person name, day borrowed, days allowed]

currentDay = 0

initialBooks()
libraryRead()
endFine()
endTally()
ratioBook()
mostPopular()
#Ratio Sorting function
#Tally Sorting function
print(bookList)
print(fineList)
print(borrowList)

# comment
