# Get input from user as a string to preserve leading zeros
num = input("Enter a number: ")

# Make it cyclic by appending the first two digits at the end
cyclic_num = num + num[:2]

triplets = []
seen = set()

# Generate triplets until the first one repeats
for i in range(len(num)):
    triplet = cyclic_num[i:i+3]
    if triplet in seen:
        break  # Stop when a triplet repeats
    triplets.append(triplet)
    seen.add(triplet)

# Display the triplets
print("Sequential triplets (cyclic) until repetition:")
print(triplets)