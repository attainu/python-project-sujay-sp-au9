import time
import sys
from collections import defaultdict
import threading
from playsound import playsound


class Swiggy:
    def __init__(self, input):
        self.PROCESSING_POWER = 3
        self.restaurants = [['Davangere benne dosa', 5000, 3, True], ['ITC gardenia', 5000, 3, True], [
            'Empire restaurant', 5000, 3, True], ['Shanti sagar', 5000, 3, True], ['Burma burma', 5000, 3, True]]
        self.items = defaultdict(list, {
            'Davangere benne dosa': [
                ['Butter masala dosa', 5, 30], ['Open masala dosa', 6, 40], ['Onion dosa', 4, 50], ['Rava dosa', 6, 50], ['Neer dosa', 5, 40]],
            'ITC gardenia': [
                ['Avocado uramaki', 15, 200], ['Ebi tempura roll', 14, 210], ['Banoffee truffle', 17, 210], ['Golden fried broccoli', 12, 190], ['Tawa meen', 27, 270]],
            'Empire restaurant': [
                ['Chicken tandoori', 18, 140], ['Parota', 7, 20], ['Butter chicken', 17, 120], ['Butter scotch milkshake', 10, 120], ['Shaadi-ki-biriyani', 25, 570]],
            'Shanti sagar': [
                ['Veg palao', 12, 80], ['Veg biriyani', 12, 80], ['Schezwan fried rice', 14, 100], ['Palak paneer', 13, 90], ['Veg noodles', 12, 80]],
            'Burma burma': [
                ['Burmese pepper soup', 19, 290], ['Chicken ramen', 20, 370], ['Pumpkin and basil soup', 20, 290], ['Eggplant tofu mash', 19, 210], ['Sticky rice', 12, 190]]
        })
        self.ordersTaken = dict()
        f = open(input)
        lines = f.readlines()
        self.Lines = [line.strip() for line in lines]
        self.inputIndex = 0
        self.fileInput = True
        f.close()

    def inputFile(self, text=""):
        if not self.fileInput:
            return input(text)
        print(text)
        self.inputIndex += 1
        time.sleep(0.5)
        temp = self.Lines[self.inputIndex-1]
        print(temp)
        return temp

    def onboard(self):
        name = self.inputFile("Restaurant name: ")
        check = True
        for i in self.restaurants:
            if name == i[0]:
                print("Restaurant name already exists. Sorry")
                check = False
                break
        if(check):
            # Restaurant has to deposit amount of 5000
            self.restaurants.append([name, 5000, self.PROCESSING_POWER, True])
            self.addItem(name)

    def addItem(self, name):
        numberOfItems = self.inputFile(
            "Enter number of items available for order/delivery: ")
        if(numberOfItems.isdigit()):
            numberOfItems = int(numberOfItems)
            for _ in range(numberOfItems):
                tempItemList = []
                itemName = self.inputFile("Enter name of item: ")
                index = 0
                check = True
                for i in self.items[name]:
                    if(i[0] == itemName):
                        check = False
                        break
                    index += 1
                if(check):
                    itemPrepareTime = self.inputFile(
                        f'Enter preparation time required for {itemName} in minutes: ')
                    if(itemPrepareTime.isdigit()):
                        itemPrepareTime = int(itemPrepareTime)
                        itemCost = self.inputFile(
                            f'Enter cost of {itemName}: ')
                        if(itemCost.isdigit()):
                            itemCost = int(itemCost)
                            tempItemList.append(
                                [itemName, itemPrepareTime, itemCost])
                        else:
                            print("Wrong entry. Try again")
                    else:
                        print("Wrong entry(only digits 0-9 allowed)")
                    self.items[name] += tempItemList
                else:
                    updatePrice = self.inputFile("Update price. Y/N?: ")
                    if updatePrice in 'Yy':
                        updatedPrice = self.inputFile(
                            f"Enter new price for {self.items[name][index][0]}: ")
                        if(updatedPrice.isdigit()):
                            self.items[name][index][2] = int(updatedPrice)
                        else:
                            print("Wrong entry. Try again")
                    else:
                        print("Name already exists. Try again")

        else:
            print("Wrong entry(only digits 0-9 allowed)")

    def deleteItem(self, name):
        print("Enter name of item to be deleted")
        itemToDelete = self.inputFile()
        itemToDelete = itemToDelete.lower()
        for i in range(len(self.items[name])):
            if(self.items[name][i][0].lower() == itemToDelete):
                self.items[name] = self.items[name][:i] + \
                    self.items[name][i+1:]
                print(f"{itemToDelete} removed.")
                break

    def updateMenu(self):
        print("Available restaurants:")
        for i in range(len(self.restaurants)):
            print(i+1, ".", self.restaurants[i][0])
        print("Enter choice of restaurant as number representing choice:")
        choiceOfRestaurant = self.inputFile()
        if(choiceOfRestaurant.isdigit()):
            choiceOfRestaurant = int(choiceOfRestaurant)-1
            if(choiceOfRestaurant > len(self.restaurants)):
                print("Wrong entry. Try again")
            else:
                temp = self.restaurants[choiceOfRestaurant][0]
                print(f'Available items from {temp}:')
                for i in range(len(self.items[temp])):
                    print(i+1, ".", self.items[temp][i][0])
                print(
                    "Enter 1 of the following options(Enter choice as number that represents choice):")
                print("1. Add item/Edit price of existing item")
                print("2. Delete/Remove item")
                choice = self.inputFile()
                if(choice.isdigit()):
                    choice = int(choice)
                    if(choice > 2 or choice < 0):
                        print("Wrong entry. Try again")
                    else:
                        if(choice == 1):
                            self.addItem(
                                self.restaurants[choiceOfRestaurant][0])
                        else:
                            self.deleteItem(
                                self.restaurants[choiceOfRestaurant][0])
                else:
                    print("Wrong entry. Try again")

    def order(self, orderNumber):
        totalPrepareTime = []
        totalCost = 0
        print("Available restaurants:")
        for i in range(len(self.restaurants)):
            if(self.restaurants[i][1] == 0 or self.restaurants[i][2] == 0 or len(self.items[self.restaurants[i][0]]) == 0):
                self.restaurants[i][3] = False
                print(i+1, ".", self.restaurants[i]
                      [0], "-currently unavailable")
            else:
                print(i+1, ".", self.restaurants[i][0])
        print("Enter choice of restaurant as number representing choice:")
        choiceOfRestaurant = self.inputFile()
        if(choiceOfRestaurant.isdigit()):
            choiceOfRestaurant = int(choiceOfRestaurant)-1
            if(self.restaurants[choiceOfRestaurant][3] == False or choiceOfRestaurant > len(self.restaurants)):
                print("Wrong entry. Try again")
            else:
                temp = self.restaurants[choiceOfRestaurant][0]
                print(f'Available items from {temp}:')
                for i in range(len(self.items[temp])):
                    print(i+1, ".", self.items[temp][i][0])
                print(
                    "Enter choice of item as number representing choice(Multiples choices are to be separated by commas):")
                currentProcessingPower = self.restaurants[choiceOfRestaurant][2]
                print(
                    f"Note: {temp}'s current processing power is {currentProcessingPower}")
                choice = self.inputFile().strip()
                choice = choice.split(",")
                if(len(choice) > currentProcessingPower):
                    print(
                        f'Unable to process more than {currentProcessingPower} orders')
                else:
                    for i in range(len(choice)):
                        item = choice[i].strip()
                        if(item.isdigit()):
                            item = int(item)-1
                            if(item >= len(temp)):
                                print("Wrong entry. Skipping item")
                            else:
                                self.restaurants[choiceOfRestaurant][2] -= 1
                                totalPrepareTime.append(
                                    self.items[temp][item][1])
                                totalCost += self.items[temp][item][2]
                        else:
                            print("Wrong entry. Skipping item")
                    if(len(totalPrepareTime) != 0):
                        thread = threading.Thread(target=self.prepareDispatch, args=[totalPrepareTime, [
                            orderNumber, choiceOfRestaurant-1], totalCost])
                        self.ordersTaken[orderNumber] = thread
                        thread.start()

        else:
            print("Wrong entry. Retry")

    def prepareDispatch(self, totalPrepareTime, orderNumber, totalCost):
        print(
            f'Order {orderNumber[0]} will be dispatched in approximately {sum(totalPrepareTime)} minutes')
        for prepareTime in totalPrepareTime:
            time.sleep(prepareTime)
            self.restaurants[orderNumber[1]][2] += 1
        f = open(f'Order{orderNumber[0]}.txt', "w+")
        f.write(f'Order {orderNumber[0]} dispatched. Please pay {totalCost}')
        f.close()
        playsound("F:\Github\python-project-sujay-sp-au9\juntos.mp3")
        del self.ordersTaken[orderNumber[0]]


if __name__ == "__main__":
    orderNumber = 1
    system = Swiggy("input.txt")
    print("File input? y or n")
    fileInput = input()
    if fileInput in 'Nn':
        system.fileInput = False
    while(True):
        if(len(system.restaurants) == 0):
            print("Onboard atleast 1 restaurant to continue: ")
            system.onboard()
        else:
            print(
                "Choose 1 of the following options(Enter choice as number that represents choice):")
            print("1. Onboard restaurant")
            print("2. Order")
            print("3. Update menu")
            print("4. Close API")
            choice = system.inputFile()
            if(choice.isdigit()):
                choice = int(choice)
                if(choice == 4):
                    print("Checking for existing orders..")
                    while (len(system.ordersTaken) > 0):
                        time.sleep(30)
                    sys.exit("Good day.")
                elif(choice == 1):
                    system.onboard()
                elif(choice == 2):
                    system.order(orderNumber)
                    time.sleep(0.1)
                    orderNumber += 1
                elif(choice == 3):
                    system.updateMenu()
                else:
                    print("Wrong choice. Retry")

            else:
                print("Wrong entry. Retry")
