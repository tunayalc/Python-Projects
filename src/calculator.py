import sys

# Function to perform basic calculator operations
def calculate(variable1, operator, variable2):
    if operator == '+':
        return variable1 + variable2
    elif operator == '-':
        return variable1 - variable2
    elif operator == '*':
        return variable1 * variable2
    elif operator == '/':
        if variable2 != 0:  # Check for division by zero
            return variable1 / variable2
        else:
            return "Division by zero error"
    else:
        return "Invalid operator"

# Main function to get inputs from command line and perform the calculation
def main():
    if len(sys.argv) != 4:  # Expect 3 arguments from the command line
        print("Usage: calculator.py <number1> <operator> <number2>")
        sys.exit(1)

    try:
        number1 = float(sys.argv[1])  # Get the first number
        operator = sys.argv[2]        # Get the operator (+, -, *, /)
        number2 = float(sys.argv[3])  # Get the second number
    except ValueError:
        print("Invalid number")
        sys.exit(1)

    result = calculate(number1, operator, number2)
    print(result)

if __name__ == "__main__":
    main()
