import copy
class commodity():
    def __init__(self,product_name,price):

        self.product_name = product_name
        self.price = price


class Order():
    def __init__(self,user_name,order_id,type):
        self.order_id =order_id
        self.user_name = user_name
        self.order_items = []
        self.total_price = 0
        self.type = type

    def add_order(self,item):
        self.order_items.append(item)

class Dine_order(Order):
    def __init__(self,user_name,order_id,type):
        super().__init__(user_name,order_id,type)
        self.date = input("Please enter the date of booking for dine in:")
        self.time = input("Please enter the time of booking for dine in:")
        self.persons = input("Please enter the number of persons:")
    def get_total(self):
        for item in self.order_items:
            self.total_price += item.price
        service = self.total_price * 0.1
        self.total_price += service
        return f"Your total payble amount is :{self.total_price} inclusing AUD {service} for Service Charges"



class Pickup_order(Order):
    def __init__(self,user_name,order_id,type):
        super().__init__(user_name,order_id,type)
        self.date = input("Please enter the date of pickup:")
        self.time = input("Please enter the time of pickup:")
        self.person = input("Please enter the name of persons:")
    def get_total(self):
        for item in self.order_items:
            self.total_price += item.price
        return f"Your total payble amount is :{self.total_price}"
class Delevery_order(Order):
    def __init__(self, user_name,order_id,type,address,distance):
        super().__init__(user_name,order_id,type)

        self.address = address
        self.date = input("Please enter the date of delivery:")
        self.time = input("Please enter the time of delivery:")
        self.distance = distance
    def get_total(self):
        for item in self.order_items:
            self.total_price += item.price
        if self.distance <2 :
            service = 5
        elif self.distance <5:
            service = 10
        elif self.distance <10:
            service = 18
        else:
            raise ValueError("Distance is too long")
        self.total_price += service
        return f"Your total payble amount is :{self.total_price} and there will be an additional charges for Delivery"

class User():
    def __init__(self,name,mobile,password,dob,address=None):
        self.name=name
        self.mobile = mobile
        self.password = password
        self.dob = dob
        self.address = address
        self.orders = []
    def add_order(self,order):
        self.orders.insert(0,order)


class UserManage():
    def __init__(self):
        self.all_users = {}
    def add_user(self,user):
        self.all_users[user.mobile] = user
    def get_user(self,mobile):
        if mobile in self.all_users.keys():
            return self.all_users[mobile]
        else:
            return None


class restaurant():
    def __init__(self):

        self.user_manage = UserManage()

        self.foods = {1:["Noodles",2],
                     2:["Sandwich",4],
                     3:["Dumpling",6],
                     4:["Muffins",8],
                     5:["Pasta",10],
                     6:["Pizza",20]
                     }
        self.drinks = {1:["Coffee",2],
                      2:["Colddrink",4],
                      3:["Shake",6],
        }

        self.now_user = None
        self.order_id = 1

    def show_main(self):
        print("Please Enter 1 for Signup")
        print("Please Enter 2 for Login")
        print("Please Enter 3 for Exit")
        select = int(input("input your select:"))
        return select
    def show_home(self):
        print("Please Enter 2.1 to Start Order")
        print("Please Enter 2.2 to Print Statistics")
        print("Please Enter 2.3 to Logout")
        select = input("input your select:")
        return select
    def show_start_order(self):
        print("Please Enter 1 for Dine in.")
        print("Please Enter 2 for Order Online.")
        print("Please Enter 3 to go to Login Page.")

        select = int(input("input your select:"))

        return select
    def show_menu(self,mode="Dine in"):

        temp_list = []

        for k,v in self.foods.items():
            print(f"Enter {k} for {v[0]}\tPrice AUD {v[1]}")
        print(f"Enter {k+1} Drinks Menu")
        select = int(input("input your select:"))

        if select in self.foods.keys():
            temp_list.append(self.foods[select])

        if select <= k + 1 :
            for k,v in self.drinks.items():
                print(f"Enter {k} for {v[0]}\tPrice AUD {v[1]}")
            print(f"Enter {k+1} for Checkout")
            select = int(input("input your select:"))
            if select in self.drinks.keys():
                temp_list.append(self.drinks[select])
            if select <= k + 1:
                select = input("Please Enter Y to proceed to CHeckout or\n Enter N to cancel the order")
                if select == "Y" or select == "y":

                    if mode == "Dine in":
                        order = Dine_order(user_name=self.now_user.name,type=mode,order_id=self.order_id)

                    elif mode == "delivery":


                        address = self.now_user.address
                        distance = self.now_user.distance

                        order = Delevery_order(user_name= self.now_user.name, address=address, distance=distance,type=mode,order_id=self.order_id)

                    elif mode == "pickup":
                        order = Pickup_order(user_name=self.now_user.name,type=mode,order_id=self.order_id)
                    else:
                        raise ValueError("mode is not correct")
                    for item in temp_list:
                        order.add_order(commodity(item[0],item[1]))
                    self.order_id += 1
                    self.now_user.add_order(order)
                    total_str = order.get_total()
                    print(total_str)


                    return True
                else:
                    return False
    def show_order_online(self):
        print("Enter 1 for Self Pickup")
        print("Enter 2 for Home Delivery")
        print("Enter 3 to go to Previous Meun")
        select = int(input("input your select:"))
        if select == 1:
            self.show_menu(mode="pickup")
        elif select == 2:

            if self.now_user.address == None:
                print("""You have not mentiond your address ,while signing up.\n
                      Please Enter Y if would like to enter your address.\n
                      Enter N if you would like to select other mode of order.""")
                address = input("input your address")

                distance = float(input("input your distance"))
                if distance > 10:
                    print("Sorry, your distance is too far away.")
                    return self.show_order_online()
                else:
                    self.now_user.distance =distance
                    self.now_user.address = address
            self.show_menu(mode="delivery")
        elif select == 3:
            return False

    def Signup(self):
        tempname = input("\nPlease enter your name:")
        if self.user_manage.get_user(tempname) != None:
            print("Your name have Signed up.")
            return False
        m = True  # validate mobile
        while m is True:
            tempmobile = input("\nPlease enter your mobile number:")
            if (len(tempmobile) == 10) and (tempmobile[0] == "0"):  # validate mobile
                m = False  # end the loop
            else:
                print("\nYou have entered the mobile in invalid format. \nPlease start again:")
        p = True  # validate pw
        while p is True:
            temppw = input("\nPlease enter your Password:")
            pos = temppw.find("@") + temppw.find("#") + temppw.find("$") + 2
            prepw = temppw[0:pos]
            postpw = temppw[pos + 1:]
            if postpw.isdigit() and prepw.isalpha() and pos > 0:
                p = False  # end the loop
            else:
                print("\nYou have entered the password in invalid format. \nPlease start again:")
        pc = True  # validate pw confirmation
        while pc is True:
            confirmpw = input("\nPlease confirm your password:")
            if confirmpw == temppw:  # validate re-enter pw
                pc = False
            else:
                print("\nYour passwords are not matching.\nPlease start again:")
        b = True  # validate dob
        while b is True:
            tempdob = input("\nPlease Enter your Date of Birth # DD/MM/YYYY (No Space):")
            if len(tempdob.split("/")) != 3 or int(tempdob.split("/")[0]) > 31 or int(
                    tempdob.split("/")[1]) > 12 or int(tempdob.split("/")[2]) < 1900:
                print("\nYou have entered the date of Birth in invalid format.\nPlease start again")
            elif 2022 - int(tempdob.split("/")[2]) < 18:  # validate age
                print("\nYou must be at least 18 years old. \nPlease start again.")
            else:
                b = False
                print("You have successfully signed up")
                self.user_manage.add_user(User(name=tempname, mobile=tempmobile, password=temppw, dob=tempdob))

    def Login(self):
        login = True
        while login is True:  # validate login
            inputuser = input("Please enter your Username (Mobile Number):")
            counterpw = 0
            while (counterpw < 3):
                inputpw = input("\nPlease enter your password: ")
                if self.user_manage.get_user(inputuser) is not None:

                    if inputpw == self.user_manage.get_user(inputuser).password:
                        print("You have Successfully Signed in.\nWelcome", inputpw)
                        login = False
                        break
                    else:
                        print("You have input wrong password.")
                        counterpw = counterpw + 1
                else:
                    print("Record not found for the Username")
                    return False
            while (counterpw >= 3):  # change password for 3 pw error
                print(
                    "You have used the maximum attempts of Login:\nPlease reset password by entering the below details:")
                checkm = input("\nPlease enter your Username (Mobile Number) to confirm:")
                if self.user_manage.get_user(inputuser).mobile == checkm:
                    checkdob = input("\nPlease enter your Date of Birth in DD/MM/YYYY format, to confirm:")
                    if checkdob == self.user_manage.get_user(inputuser).dob:  # check DOB
                        updatepw = input("\nPlease enter your new Password:")
                        if updatepw == self.user_manage.get_user(inputuser).password:
                            print("You cannot use the password used earlier.")
                        else:  # validate new pw
                            pos = updatepw.find("@") + updatepw.find("#") + updatepw.find("$") + 2
                            prepw = updatepw[0:pos]
                            postpw = updatepw[pos + 1:]
                            if postpw.isdigit() and prepw.isalpha() and pos > 0:
                                self.user_manage.get_user(inputuser).password = updatepw
                                print("Your Password has been reset successfully.")
                                counterpw = 0
                            else:
                                print("You have entered the password in invalid format. \nPlease start again:")
                    else:
                        print("You have entered incorrect Date of Birth.")
                else:
                    print("You have entered incorrect Username")
        if login is False:
            self.now_user = self.user_manage.get_user(inputuser)
            return True

    def Print_statistics(self):
        print("Please Enter the Option to Print the Statistics:")
        print("1 - All Dine in Orders.")
        print("2 - All Pick up Orders.")
        print("3 - All Deliveries")
        print("4 - All Orders (Descedingly)")
        print("5 - Total Amount Spent on All Orders.")
        print("6 - To go to Previous Menu.")
        select = int(input("Please Enter the Option: "))
        print("Order ID\t\tDate\t\tType of Order\t\tOrder Amount")
        if select == 1:
            for i in self.now_user.orders:
                if i.type == "Dine in":
                    print(f"{i.order_id}\t\t{i.date}\t\t{i.type}\t\t{len(i.order_items)}")
        elif select == 2:
            for i in self.now_user.orders:
                if i.type == "pickup":
                    print(f"{i.order_id}\t\t{i.date}\t\t{i.type}\t\t{len(i.order_items)}")
        elif select == 3:
            for i in self.now_user.orders:
                if i.type == "delivery":
                    print(f"{i.order_id}\t\t{i.date}\t\t{i.type}\t\t{len(i.order_items)}")
        elif select == 4:
            for user in self.user_manage.all_users:
                for i in user.orders:
                    print(f"{i.order_id}\t\t{i.date}\t\t{i.type}\t\t{len(i.order_items)}")
        elif select == 5:
            total = 0
            for i in self.now_user.orders:
                total += i.total_price
                print(f"Total Amount Spent on All Orders AUD: {total}")
        elif select == 6:
            return True



    def main(self):
        while True:
            select_main = self.show_main()

            if select_main == 1:
                self.Signup()
            elif select_main ==2:
                login = self.Login()
                while self.now_user:
                    select_home = self.show_home()
                    if select_home == "2.1":
                        while True:
                            select_start_order = self.show_start_order()
                            if select_start_order ==1:
                                show_menu = self.show_menu(mode="Dine in")
                                break
                            elif select_start_order == 2:
                                self.show_order_online()
                            elif select_start_order == 3:
                                break

                    elif select_home == "2.2":
                        self.Print_statistics()
                    elif select_home == "2.3":
                        self.now_user = None

            elif select_main == 3:
                break


        print()
if __name__ == '__main__':
    r = restaurant()
    # r.user_manage.add_user(User(name="XXX", mobile="0111111111", password="X@11", dob="11/11/1988"))
    r.main()