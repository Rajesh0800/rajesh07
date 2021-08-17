import mysql.connector
mydb = mysql.connector.connect(host="localhost",user="root",password="Janakiraman123!@#",database="hotel_booking")
mycursor=mydb.cursor()
def validate_login(username,password):
    mycursor.execute("select * from customer_details where customer_name like %s",(username,))
    data=mycursor.fetchall()
    name=data[0][1]
    passw=data[0][2] 
    if name==username and passw==password:
        return 1  
def validate_ownerdetails(owner_name,password):
    mycursor.execute("select * from owner_details where owner_name like %s",(owner_name,))
    data=mycursor.fetchall()
    name=data[0][1]
    passw=data[0][2] 
    if name==owner_name and passw==password:
        return 1    
def booking(username):
    mycursor.execute("select * from hotel_details;")
    data=mycursor.fetchall()
    print('choose the hotel :',data)
    option=int(input('ENTER YOUR OPTION:'))
    for i in range(1,len(data)):
        if option==i:
            selectedhotel=data[i-1]
            print('selected hotel_id :',selectedhotel[0],end=" ")
            print(' hotel_name :',selectedhotel[1],end=" ")
            print(' available tables:',selectedhotel[2],end=" ")
            print(' ratings :',selectedhotel[3],end=" ")
            print('cost per table:',selectedhotel[6])
            a=selectedhotel[1]
            c=selectedhotel[2]
            cost=selectedhotel[6] 
            location=selectedhotel[5]
            rating=selectedhotel[3]
            nooftable=int(input('ENTER TABLE REQUIRED :'))
            if nooftable<=c:
                d=c-nooftable
                mycursor.execute('update hotel_details set available_tables=%s where hotel_name=%s',(d,a))
                mydb.commit()
            else:
                print('No tables available for you')
            totalcost=nooftable*cost
            print('TOTAL COST:',totalcost)
            comment=str(input('ENTER YOUR COMMENTS:'))
            mycursor.execute("insert into booking_details(username,hotel_name,totalcost,rating,comment,location) values (%s,%s,%s,%s,%s,%s)",(username,a,totalcost,rating,comment,location,))
            mydb.commit() 
            return 1     
        else:
            print("Invalid option")
            return 0
def payment(username):
    accountHolderName = str(input('Enter your account holder name'))
    accountNumber = int(input('Enter your account number'))
    month = int(input('Enter your account valid month'))
    year = int(input('Enter your account valid year'))
    ccv = int(input('Enter your account valid ccv'))
    mycursor.execute=("insert into order_details(username,account_holder_name,account_no,month,year,ccv) values(%s,%s,%s,%s,%s,%s)",(username,accountHolderName, accountNumber, month, year, ccv,))
    mydb.commit()  
def display_customerdetails(username):
    mycursor.execute("select * from customer_details where customer_name like %s",(username,))
    data=mycursor.fetchall()
    print("customer_Id :%s"%data[0][0])
    print("Name:%s"%data[0][1])
    for row in range(len(data)):
        print("Password :%s"%data[row][2])
        print("Mail :%s"%data[row][4])
        print("Phone :%s"%data[row][3])
        print()
    return 1  
def display_all():
    mycursor.execute("select * from customer_details")
    data=mycursor.fetchall() 
    for row in range(len(data)):
        print("User_Id :%s"%data[row][0])
        print("Name:%s"%data[row][1])
        print("Password :%s"%data[row][2])
        print("Mail :%s"%data[row][4])
        print("Phone :%s"%data[row][3])
        print()
    return 1    
def display_booking():
    mycursor.execute("select * from booking_details")
    data=mycursor.fetchall() 
    if data:
        for row in range(len(data)):
            print("book_id:%s"%data[row][0],end="       ")
            print("username :%s"%data[row][1],end="        ")
            print("hotelname:%s"%data[row][2],end="    ")
            print("totalcost:%s"%data[row][3],end="   ")
            print("location:%s"%data[row][6])
            print()
    else:
        print("No Records found!")

destination=input("Are you a user or hotel_owner or newuser?"+'\n'+" Type your destination :") 
destination=destination.lower()
if destination=="user": 
    username=input("Enter your name :")
    password=input("Enter your password :")
    if validate_login(username,password):   
         if booking(username):
                payment(username)
                print("Order Success")
    else:
        print('customer not valid')
if destination=="newuser":
    username=input("Enter your name :")
    password=input("Enter your password :")
    mail=input("Enter your mail :")
    phone=input("Enter your Phone number :")
    address=input("Enter your address :")
    mycursor.execute("insert into customer_details(customer_id,customer_name,password,phone_number,email) values(null,%s,%s,%s,%s)",(username,password,phone,mail))
    mydb.commit()
    print("Registration success !!")
if destination=="hotel_owner":
    owner_name=str(input('ENTER YOUR NAME :'))
    password=str(input('ENTER THE PASSWORD :'))
    if validate_ownerdetails(owner_name,password):
        while(1):
            print("1.Display the particular customer_details"+'\n'+"2.Display all the records"+'\n'+"3.Display booking_details")
            print("Enter your option :")
            option=int(input())
            if option==1:
                username=input("Enter the username: ")
                display_customerdetails(username)
            elif option==2:
                display_all() 
            elif option==3: 
                display_booking()
            elif option==0:
                break
            else:
                print("Invalid option Please choose correct option!") 
    else:
        print("not a admin")