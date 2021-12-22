#Carson Pedaci, TJ DeFrancesco, Tanush Sanjay


#Returns a 2d list from booklist
def booklistMaker(fread,n):
    #n will always be the last day
    #First index is a list of book titles
    #Second index is a list of number of copies
    #Third index is a list of restriction statuses
    #Fourth index is the day the book was added to the library (0)
    #Fifth index is the number of days it can be borrowed
    fread.seek(0)
    bline = fread.readline()
    titles = []
    copies = []
    restrictions = []
    datesadded = []
    possibledays = []
    while bline != '':
        b = bline.rstrip('\n')
        a = b.split('#')
        titles.append(a[0])
        copies.append(int(a[1]))
        restrictions.append(a[2])
        datesadded.append(int("0"))
        possibledays.append(copies[-1]*(n-1))
        bline = fread.readline()
    return titles, copies, restrictions, datesadded, possibledays

#Traverses through the log until the end or a certain date. Adjusts the contents of mainlist.
def checklog(fread, lst, n):
    #fread is log, lst is mainlist
    fread.seek(0)
    s = fread.readline()
    booktitles = lst[0]
    copies = lst[1]
    datesadded = lst[3]
    possibledays = lst[4]
    new = True
    while s!="":
        s = s.rstrip ("\n")
        #a == list of contents of a line in library log, split by #. Changes every time a new line is read.
        a = s.split('#')
        #Meaning that we have not read the last line yet, which is just one number.
        if len(a)>1:
            day = int(a[1])
            if day <= n:
                status = a[0]
                day = a[1]
                #Adjusting book information based on what happened before the specified day.
                for i in range(len(booktitles)):
                    if status=='B' or status=='R':
                        name = a[2]
                        book = a[3]
                        if book==booktitles[i]:
                            #Subtracts a copy when the book is borrwed.
                            if status=='B':
                                bdays = int(a[4])
                                copies[i]-=1
                            elif status=='R':
                                copies[i]+= 1            
                if status=='A':
                    day = int(a[1])
                    book = a[2]
                    for i in range(len(booktitles)):
                        if book == booktitles[i]:
                            new = False
                            if not new:
                                copies[i]+=1
                                possibledays[i] = possibledays[i] + (n-day)
                    if new:
                        booktitles.append(book)
                        copies.append(int("1"))
                        lst[2].append("FALSE")
                        datesadded.append(day)
                        possibledays.append(n-day)
                elif status=='P':
                    money = a[3]
        s = fread.readline()

#Checks if there are any copies of a book left
def copycheck(lst,book):
    #Call with mainlist
    blist = lst[0]
    copieslist = lst[1]
    for i in range(0,len(blist)):
        if book == blist[i]:
            if copieslist[i] > 0:
                return True
            else:
                return False

#Makes a list of restricted books
def restrictedbooks(lst):
    #call with mainlist
    restrictedlist = []
    for i in range(0,len(lst[2])):
      if lst[2][i] == 'TRUE':
        restrictedlist.append(lst[0][i])
    return restrictedlist

#Makes a list of all borrows and returns        
def brlistcreation(fread,lst,n):
    #call with log as reader, mainlist as lst
    currentday = lastday
    booktitles = lst[0]
    copies = lst[1]
    #day, name, book, intended days, copies remaining
    borlist = [[],[],[],[],[]]
    
    #day, name, book, copies remaining
    retlist = [[],[],[],[]]
    
    fread.seek(0)
    s = fread.readline()
    while s!= '':
        s = s.rstrip('\n')
        a = s.split('#')
        #Meaning that we have not read the last line yet, which is just one number.
        if len(a)>1:
            day = int(a[1])
            if day <= n:
                status = a[0]
                day = a[1]
                #Adjusting book info based on what happened until the specified day
                for i in range(len(booktitles)):
                    if status=='B' or status=='R':
                        name = a[2]
                        book = a[3]
                        if book==booktitles[i]:
                            #Subtracts a copy when the book is borrwed.
                            if status=='B':
                                bdays = int(a[4])
                                copies[i]-=1
                                borlist[0].append(day)
                                borlist[1].append(name)
                                borlist[2].append(book)
                                borlist[3].append(bdays)
                                borlist[4].append(copies[i])
                            elif status=='R':
                                copies[i]+= 1
                                retlist[0].append(day)
                                retlist[1].append(name)
                                retlist[2].append(book)
                                retlist[3].append(copies[i])
        s = fread.readline()
    return borlist, retlist

#Add new books to booklist
def makeaddlist(fread, lst, n):
    #fread is log, lst is staticmainlist, n is the specified day
    fread.seek(0)
    s = fread.readline()
    booktitles = lst[0]
    copies = lst[1]
    #day, book, copies after addition, whether or not the book was a new addition
    addlist = [[],[],[],[]]
    while s!="":
        s = s.rstrip ("\n")
        a = s.split('#')
        #Meaning that we have not read the last line yet, which is just one number.
        if len(a)>1:
            status = a[0]
            day = int(a[1])
            if day <= n:
                #Adjusting book info based on what happened until the specified day
                if status=='A':
                    book = a[2]
                    new = True
                    addlist[0].append(day)
                    addlist[1].append(book)
                    for j in range(len(booktitles)):
                        if book == booktitles[j]:
                            i = j
                            new = False
                    if not new:
                        copies[i]+=1
                        addlist[2].append(copies[i])
                    elif new:
                        addlist[2].append(copies[-1])
                    addlist[3].append(new)
        s = fread.readline()
    return addlist


#***Can a student borrow a book on a certain day for a certain number of days?***

def borrowcheck(fread,reslist,tlst,n):
    #fread is log
    #reslst is restrictedlist
    #tlist is list of book titles from mainlist[0]
    #n is current day
    student = input("Enter the student: ")
    book = input("What book would you like to borrow? ")
    days = int(input("For how many days? "))
    #day borrowed,book,due date
    duedates = []
    
    #book, day returned
    returndates = []

    outbooks = []

    paid = 0
    log.seek(0)
    #Check for only one student
    li = log.readline()
    while li != "":
        b = li.rstrip("\n")
        a = b.split("#")
        if len(a)>1:
            if int(a[1]) <= n:
                if a[0] == "B":
                    day = int(a[1])
                    name = a[2]
                    title = a[3]
                    if name == student:
                        outbooks.append(title)
                        due = day+int(a[4])
                        duedates.append([day,title,due])
                elif a[0] == "R":
                    day = int(a[1])
                    name = a[2]
                    title = a[3]
                    if name == student:
                        outbooks.remove(title)
                        returndates.append([title,day])
                elif a[0] == "P":
                    name = a[2]
                    if name == student:
                        paid += int(a[3])
        li = log.readline()
    #Determining pending fines based off of late returns
    diff = 0
    fine = 0
    overduebook = ''
    for r in returndates:
        diff = 0
        #check every book returned
        for b in duedates:
            if r[0] == b[1]:
                diff = r[1]-b[2]
                if diff > 0:
                    overduebook = r[0]                
    if diff > 0:
        if overduebook in reslist:
            fine = 5*diff
        else:
            fine = 1*diff

    fine = fine - paid


    if book in restrictedlist:
        maxdays = 7
    elif book not in restrictedlist:
        maxdays = 28


    canborrow = True
    if days > maxdays:
        print("You cannot borrow this book for so many days!")
        canborrow = False
    elif book not in tlst:
        print("The library does not have this book!")
        canborrow = False
    elif fine > 0:
        print("You have outstanding fines and cannot borrow a book!")
        canborrow = False
    elif len(outbooks) >= 3:
        print("You already have more than 3 books out!")
        canborrow = False
    elif copycheck(mainlist,book) == False:
        print("Sorry, there are no copies of this book left!")
        canborrow = False
    elif book in outbooks:
        print("You already have a copy of this book taken out!")
        canborrow = False
    else:
        print("You can borrow this book!")
        canborrow = True



#***What are the most borrowed/popular books in the library (Days they were borrowed vs not borrowed)***
def borrowedbooks(fread,lst,alst,n,x):
    #fread is log
    #lst is mainlist
    #alist is addlist
    #n is current day 
    sumlist = []
    for book in range(len(lst[0])):
        total = lst[1][book]
        day = 1
        copiesout = 0
        numerator = 0
        addition = False
        for i in range(len(alst)):
            if alst[i] == lst[0][book]:
                day = nreservelist[i]
                adjn = n - day
                addition = True
        fread.seek(0)
        bline = fread.readline()
        while day < n:
            if bline != '':
                b = bline.rstrip('\n')
                a = b.split('#')
                if addition:
                    while len(a) > 1 and int(a[1]) < day:
                        bline = fread.readline()
                        b = bline.rstrip('\n')
                        a = b.split('#')
                if len(a) > 1 and int(a[1]) == day:
                    if a[0] == 'A':
                        if not addition:
                            if a[2] == lst[0][book]:
                                total += 1
                    elif a[3] == lst[0][book]:
                        if a[0] == 'B':
                            copiesout += 1
                        elif a[0] == 'R':
                            copiesout -= 1
                    bline = fread.readline()
                else:
                    numerator += int(copiesout)
                    day += 1
        sumlist.append(numerator)
    ratiolist = [[],[]]
    for book in range(len(lst[0])):
        if x == 1:
            print(lst[0][book],"was borrowed", sumlist[book],"days out of",lst[4][book])
        ratiolist[0].append(lst[0][book])
        ratiolist[1].append(int(sumlist[book])/int(lst[4][book]))
    return ratiolist

    
    
#***Borrow ratio***

def borrowRATIO(rlist):
    for i in range(len(rlist[0])):
        print(rlist[0][i],"ratio is",rlist[1][i])
    

#***Sort ratios***

def ratiosort(rlist):
    #ratios
    lst1 = rlist[1]
    #titles
    lst2 = ratiolist[0]
    i = 0
    while i < len(lst1):
        sm = i
        j = i
        while j < len(lst1):
            if lst1[j] < lst1[sm]:
                sm = j
            j += 1
        temp = lst1[i]
        lst1[i] = lst1[sm]
        lst1[sm] = temp
        temp = lst2[i]
        lst2[i] = lst2[sm]
        lst2[sm] = temp
        i += 1
    for k in range(len(lst2)):
        print(lst2[k], lst1[k])


#***Impending fines at the end of log***
        
def impendingfines(fread,reslist,n):
    #fread is log
    #reslist is restrictedlist
    #n is the current day
    studentlist = []
    fread.seek(0)
    li = fread.readline()
    while li != "":
        li = li.rstrip('\n')
        a = li.split('#')
        if len(a) > 1 and a[0] != 'A':
            if a[2] not in studentlist:
                studentlist.append(a[2])
        li = fread.readline()    
        
    for student in studentlist:
        #day borrowed, book, due date
        duedates = []

        #book, day returned
        returndates = []

        #books currently being borrowed
        outbooks = []
        
        fine = 0
        paid = 0
        fread.seek(0)
        #Check for only one student
        li = fread.readline()
        while li != "":
            li = li.rstrip("\n")
            a = li.split("#")
            if len(a)>1:
                if int(a[1]) <= n:
                    if a[2] == student:
                        if a[0] == "B":
                            day = int(a[1])
                            name = a[2]
                            book = a[3]
                            outbooks.append(book)
                            due = day+int(a[4])
                            duedates.append([day,book,due])
                        elif a[0] == "R":
                            day = int(a[1])
                            name = a[2]
                            book = a[3]
                            outbooks.remove(book)
                            returndates.append([book,day])
                        elif a[0] == "P":
                            paid += int(a[3])
            li = fread.readline()
        #Determining pending fines based off of late returns
        diff = 0
        fine = 0
        overduebook = ''
            
        for r in returndates:
            diff = 0
            #check every book returned
            for b in duedates:
                if r[0] == b[1]:
                    diff = r[1]-b[2]
                    if diff > 0:
                        overduebook = r[0]
        if diff > 0:
            if overduebook in reslist:
                fine = 5*diff
            else:
                fine = 1*diff
        fine = fine - paid
        print("On day", currentday,student,"has impending fines of",fine,"dollars.")
        duedates.clear()
        returndates.clear()
        outbooks.clear()

#***main***

#Storing last line of librarylog (the last day) as a variable.
log = open('librarylog-3.txt','r')
with log as f:
    lines = f.read().splitlines()
    last_line = int(lines[-1])
lastday = last_line
print("*Note*: When answering number 1, adjust the current day. Otherwise, enter \"End\"")
currentday = input("Enter the current date, or \"End\" for the last day: ")

if currentday == "End":
    currentday = lastday
else:
    currentday = int(currentday)

print('The day is',currentday,end='\n')

booklist = open('booklist-2.txt','r')
log = open('librarylog-3.txt','r')

#mainlist is used in essentially every funtion. Create it first.
mainlist = booklistMaker(booklist,currentday)
titles = mainlist[0]
addlist = makeaddlist(log,mainlist,lastday)
checklog(log,mainlist,currentday)
brlist = brlistcreation(log,mainlist,currentday)
borrowlist = brlist[0]
returnlist = brlist[1]
restrictedlist = restrictedbooks(mainlist)


print("Welcome to the library!\n")

print("What would you like to do?\n")

print("1- Check if a student can borrow a book")
print("2- Most popular books")
print("3- Borrow ratio for each book")
print("4- Sorted list of borrow ratios")
print("5- Check for impending fines")



req = int(input())
if req == 1:
    borrowcheck(log,restrictedlist,titles,currentday)
elif req == 2:
    borrowedbooks(log,mainlist,addlist,currentday,1)
elif req == 3:
    sumlist = borrowedbooks(log,mainlist,addlist,currentday,0)
    borrowRATIO(sumlist)
elif req == 4:
    ratiolist = borrowedbooks(log,mainlist,addlist,currentday,0)
    ratiosort(ratiolist)
elif req == 5:
    impendingfines(log,restrictedlist,currentday)

booklist.close()
log.close()










