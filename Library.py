##Collaborators:  Ben Siri, Yuval Levi, Jack Scott, Nathaniel Yerage

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
        global currentDay
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
    has3Books = False
    booksOut = 0
    for fine in fineList:
        if fine[0] == book[secondTag+1:thirdTag]:
            hasFine = True
    for x in borrowList:
        if x[1] == book[secondTag+1:thirdTag]:
            booksOut += 1
    if booksOut >= 3:
        has3Books = True
    if not(hasFine and has3Books):
        for element in bookList:
            if book[thirdTag+1:fourthTag] == element[0]:
                if element[1] == 0:
                    found = False
                else:
                    found = True
                    element[1] -= 1
    if not(hasFine and has3Books) and found:
        borrowList.append([str(book[thirdTag+1:fourthTag]),str(book[secondTag+1:thirdTag]),
                   int(book[firstTag+1:secondTag]),int(book[fourthTag+1:])])

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
    paid=int(task[tag3+1])
    for x in fineList:
        if(x[0]==person):
            x[1]=x[1]-paid
        if(x[1]<=0):
            fineList.pop(fineList.index(x))

def endTally():
    for book in borrowList:
        for element in bookList:
            if(element[0] == book[0]):
                element[3]+=currentDay-book[2]

def returnBook(book):
    firstTag = book.index("#")
    secondTag = firstTag+book[firstTag+1:].index("#")+1
    thirdTag = secondTag+book[secondTag+1:].index("#")+1

    day = book[firstTag+1:secondTag]
    name = book[secondTag+1:thirdTag]
    bookName = book[thirdTag+1:]
    for element in borrowList:
        #element[0] = book name, [1] person name, [2] day borrowed, [3] days allpwed
        if element[0] == bookName and element[1] == name:
            for x in bookList:
                if x[0] == bookName:
                    x[1] += 1
            borrowList.pop(borrowList.index(element))
            tallyBook(int(day)-(element[2]), element[0])
            if element[3] < (int(day)-(element[2])):
                print("Line 104: book to be added")
                addFine(int(day)-element[2], element[3], bookName, name)

def addFine(days, allowedDays, bookName, name):
    #print("days:", days, "allowedDays:", allowedDays, "bookName:", bookName, "name:", name)
    print(fineList)
    restricted = True
    for x in bookList:
        #x[0] = bookName, x[2] = restriction
        if x[0] == bookName:
            restricted = x[2]
    if restricted:
        if len(fineList) == 0:
            fineList.append([name,(days-allowedDays)*5])
        else:
            found = False
            for fine in fineList:
                if fine[0] == name:
                    found = True
                    fine[1] += (days-allowedDays)*5
            if not(found):
                fineList.append([name,(days-allowedDays)*5])
    else:
        if len(fineList) == 0:
            fineList.append([name,days-allowedDays])
        else:
            found = False
            for fine in fineList:
                if fine[0] == name:
                    found = True
                    fine[1] += (days-allowedDays)
            if not(found):
                fineList.append([name,days-allowedDays])
    print(fineList)

def endFine():
    global currentDay
    print("Line 133: end fine")
    for book in borrowList:
        for element in bookList:
            if(currentDay - book[2] > book[3]):
                if(element[0] == book[0]):
                    if(element[2]):
                        fine = (currentDay - book[2] + book[3])*5
                        flag = True
                        for i in fineList:
                            if(book[1] == i[0]):
                                i[1]+= fine
                                flag = False
                        if(flag):
                            fineList.append([book[1],fine])
                    else:
                        fine = (currentDay - book[2] + book[3])
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
        book.append(float(book[3]/book[4]))

def tallySort():
    global bookList
    bklst=[]
    bklst = bookList.copy()
    out = []

    while len(bklst) > 0:
        temp = bklst[0]
        for x in range( len(bklst) ):
            if bklst[x][3] < temp[3]:
                temp = bklst[x]
        out.append(bklist.index(temp))
        bklst.remove(bklist.index(temp))



def ratioSort():
    global bookList
    bklst=[]
    bklst = bookList.copy()
    out = []
    while len(bklst) > 0:
        temp = bklst[0]
        for x in range( len(bklst) ):
            if bklst[x][6] < temp[6]:
                temp = bklst[x]
        out.append(bklst.index(temp))
        bklst.remove(bklst.index(temp))

bList = open("booklist-2.txt","r")
lLog = open("librarylog-3.txt", "r")

bookList = [] # [book name, num of copies, restriction, tally, total copies]
fineList = [] # [person name, amount]
borrowList = [] # [book name, person name, day borrowed, days allowed]

currentDay = 0

initialBooks()
libraryRead()
endFine()
endTally()
ratioBook()
ratioSort()
tallySort()
mostPopular()

print(bookList)
print(fineList)
print(borrowList)

# comment
