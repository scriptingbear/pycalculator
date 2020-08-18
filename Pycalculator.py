import math
import os
import re

class Menu(object):
    '''Menu generator class that displays a
           custom menu of the form # - text, where
           # is the index of text in a list and
           processes user selection'''
    
    #Method to clear the screen
    clear = lambda: os.system('cls')

    #Square root symbok
    SQUARE_ROOT = chr(0x221A)

    #Class constructor
    def __init__(self):
            #Initialize instance variables
            self.menu_items =['Welcome to Pycalculator 1.0!', \
                              'Add', \
                              'Subtract', \
                              'Multiply', \
                              'Divide', \
                              'Square Root', \
                              'Logarithm', \
                              'Sine', \
                              'Cosine', \
                              'Tangent', \
                              'Settings']
            self.title = self.menu_items[0]

            #Add a line of underscores beneath the
            #title text
            self.title += "\n" + '-' * len(self.title) + "\n"
            #Initialize instance variable to hold user
            #menu selection
            self.option = ""
            self.default_decimals = 2


    #Method to display menu
    #and prompt user to select an option
    def ShowMenu(self):
            Menu.clear()
            print(self.title)
            item_count = len(self.menu_items)
            for i in range(1,item_count):
                option = str(i) + " - " + self.menu_items[i]
                print(option)

            #Prompt user to make selection
            print("\n")
            while True:
                self.option = input("Please select an option number or leave blank to quit: ")
                if self.option == '':
                    print('Pycalculator says "Peace out!')
                    return
                elif not self.option.isnumeric():
                    print("Please enter a number between 1 and " + str(item_count - 1))
                else:
                    self.option = int(self.option)
                    if 1 <= self.option < item_count - 1:
                        print("You selected " + self.menu_items[self.option] + "!\n")
                        #Invoke instance method with "self." prefix
                        self.GetInput()
                    elif self.option == item_count -1:
                        self.Settings()
                    else:
                        print(f"{self.option} is not a valid selection.")


    #Method to display prompt user for values
    #and validate them
    #UPDATE 08/18/20: Refactor to handle operations requiring only
    #one operand. Also split off validation code into separate
    #method and let it support variable number of arguments
    def GetInput(self):
        #Construct dynamic prompt that varies with the
        #the selected operation
        operations = {1: ("+", "Enter two numbers separated by at least one space: "), \
                      2: ("-", "Enter two numbers separated by at least one space: "), \
                      3: ("*", "Enter two numbers separated by at least one space: "), \
                      4: ("/", "Enter two numbers separated by at least one space: "), \
                      5: ("sqr", "Enter one number >= 0: "), \
                      6: ("log", "Enter one number >= 0: "), \
                      7: ("sin", "Enter number of degrees: "), \
                      8: ("cos", "Enter number of degrees: "), \
                      9: ("tan", "Enter number of degrees: ")}
        
        operation, prompt = operations[self.option]
       
        input_string = input(prompt)
        input_string = input_string.lower()
        if input_string == "":
            print("No input.")
            return

        #Get values from user using a list comprehension.
        #UPDATE 08/18/20: Instead of splitting input string on
        #operator, parse for numeric values. We already know what
        #operation to perform. Problem arises from subtraction
        #where the operator "-" is also prefixed to a number to
        #indicate a value less than zero.
        #Resulting list will consist of one or more tuples.
        #First element of each tuple will be contain an operand, including
        #its optional negative sign
        value_list = re.findall(f"(\-?[\d]+(\.[\d]+)?)", input_string)

        #Input is invalid if no numbers detected
        if len(value_list) == 0:
            print("Invalid input.")
            return

        #Ensure correct number of values supplied
        num_values = 2 if self.option <= 4 else 1
        temp = []
        for value_tuple in value_list:
            temp.append(value_tuple[0])
            
        if len(temp) != num_values:
            print("Too few or two many inputs entered.")
            return
        else:
            value_list = temp
            
        if (operation == "/") and (float(value_list[1]) == 0.0):
            print("Denominator must be non zero.")
            return

        if not self.Validate(value_list):
            return
        else:
            #Convert inputs to int or float
            try:
                value_list = list(map((lambda value: float(value) if "." in value else int(value)), value_list))
            except:
                print("Error in converting values.")
                return

            self.Calculate(value_list, operation)

    #Method to perform selected mathematical
    #operation
    def Calculate(self, value_list, operation):
        #Perform operation and display result
        if len(value_list) == 2:
            num1, num2 = value_list[0], value_list[1]
            if operation == "+":
                result = num1 + num2
            elif operation == "-":
                result = num1 - num2
            elif operation == "*":
                result = num1 * num2
            elif operation == "/":
                result = num1/num2
        elif len(value_list) == 1:
            num = value_list[0]
            if operation == "sqr":
                if num < 0:
                    print("Invalid input.")
                    return
                else:
                    result = math.sqrt(num)
            elif operation == "log":
                if num < 0:
                    print("Invalid input.")
                    return
                else:
                    result = math.log(num, 10)
            elif operation == "sin":
                result = math.sin(math.radians(num))
            elif operation == "cos":
                result = math.cos(math.radians(num))
            elif operation == "tan":
                #Tan() is undefined at 90 and 270 etc
                #Python will return a very large number
                #Assume bad if tan(x) > 600000
                result = math.tan(math.radians(num))
                if result > 600000:
                    print("Invalid input.")
                    return


        #Display result of calculation. Using nested {} in
        #f-string interpolation to evaluate
        # application's default decimal setting
        print("Answer: ",end="")
        if '.' in str(result):
            print(f"{result:,.{self.default_decimals}f}")
        else:
            print(f"{result:,d}")
                
        
    #Method for configuring application settings
    def Settings(self):
        try:
            test = int(input("Enter default number of decimals [0-4]: "))
        except ValueError:
            print("Invalid default decimals setting.")
            return

        if 0 <= test <= 4:
            self.default_decimals = test
            print("Default decimals is " + str(test) + ".")
        else:
            print("Default decimals setting must be between 0 to 4")
            
                
            
    #Method to validate variable number of numeric inputs
    def Validate(self, value_list):
        isValid = True
        for value in value_list:
            #Validate inputs, which must be strings consisting
            #only of digits and a single decimal, with an option
            #negative sign
            if (not re.match(f"^[\d\.-]+$", value)):
                print(f"Invalid input: {value}.")
                isValid = False

            if "-" in value:
                if not value.startswith("-"):
                    print(f"Invalid input: {value}.")
                    isValid = False
                elif value.count("-") > 1:
                    print(f"Invalid input: {value}.")
                    isValid = False
                    
            if (value.count('.') > 1):
                print(f"Too many decimal points in expression: {value}.")
                isValid = False

        return isValid

            

            
            
    
