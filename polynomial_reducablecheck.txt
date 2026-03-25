from sympy import symbols, sympify, factor

# Define variable
x = symbols('x')

# Take polynomial input from user
poly_input = input("Enter a polynomial in variable x: ")

# Convert string to polynomial expression
poly = sympify(poly_input)

# Factor the polynomial
factored_poly = factor(poly)

print("\nOriginal Polynomial:", poly)
print("Factored Form:", factored_poly)

# Check reducibility
if poly == factored_poly:
    print("The polynomial is IRREDUCIBLE (over integers).")
else:
    print("The polynomial is REDUCIBLE (over integers).")
