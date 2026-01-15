def check_even_or_odd(user_input):
    
    number = int(user_input)
    if number % 2 == 0:
        print("That is an even number.")
    else:
        print("That is an odd number.")
    
def get_valid_number():
    
    while True:
        user_input = input("Enter a integer number:")
        try:
            number = int(user_input)
            return number
        except  ValueError:
            print("Invalid input. Please enter a valid integer.")

def greet(name):
    return "Hello, " + name + "! Nice to meet you."

     
greeting = greet("Alice")
print(greeting)  # Outputs: Hello, Alice!
print("please enter your number, and I will tell you if it is even or odd.")
number = get_valid_number()
check_even_or_odd(number)