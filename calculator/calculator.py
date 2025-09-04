def calculate(expression):
    tokens = expression.split()
    
    # Handle multiplication and division first
    i = 1
    while i < len(tokens) - 1:
        if tokens[i] == '*':
            tokens[i-1] = float(tokens[i-1]) * float(tokens[i+1])
            del tokens[i:i+2]
        elif tokens[i] == '/':
            tokens[i-1] = float(tokens[i-1]) / float(tokens[i+1])
            del tokens[i:i+2]
        else:
            i += 2

    # Handle addition and subtraction
    i = 1
    while i < len(tokens) - 1:
        if tokens[i] == '+':
            tokens[i-1] = float(tokens[i-1]) + float(tokens[i+1])
            del tokens[i:i+2]
        elif tokens[i] == '-':
            tokens[i-1] = float(tokens[i-1]) - float(tokens[i+1])
            del tokens[i:i+2]
        else:
            i += 2
            
    return float(tokens[0])


result = calculate("3 + 7 * 2")
print("Result:", result)
