
import random
import string

print("===== RANDOM PASSWORD GENERATOR =====")

while True:
    try:
        length = int(input("\nEnter password length (minimum 8): "))

        if length < 8:
            print("Error: Password length must be at least 8.")
            continue

        break
    except ValueError:
        print("Error: Please enter a valid number.")

print("\nChoose character types:")
print("1. Uppercase letters")
print("2. Lowercase letters")
print("3. Numbers")
print("4. Symbols")

while True:
    choice = input("Enter choices (e.g. 1 2 3): ").split()

    if (len(set(choice)) < 2 or
            any(c not in ["1", "2", "3", "4"] for c in choice)):
        print("Select at least 2 valid character types.")
    else:
        break

characters = ""
password = []

if "1" in choice:
    characters += string.ascii_uppercase
    password.append(random.choice(string.ascii_uppercase))

if "2" in choice:
    characters += string.ascii_lowercase
    password.append(random.choice(string.ascii_lowercase))

if "3" in choice:
    characters += string.digits
    password.append(random.choice(string.digits))

if "4" in choice:
    characters += string.punctuation
    password.append(random.choice(string.punctuation))

if length < len(password):
    print("Password length is too short for selected types.")
else:
    password += random.choices(
        characters, k=length - len(password)
    )
    random.shuffle(password)

    while True:
        print("\nGenerated Password:", "".join(password))

        again = input("Generate another password? (yes/no): ").lower()

        if again != "yes":
            print("Thank you for using Password Generator!")
            break

        password = []

        for c in choice:
            if c == "1":
                password.append(random.choice(string.ascii_uppercase))
            elif c == "2":
                password.append(random.choice(string.ascii_lowercase))
            elif c == "3":
                password.append(random.choice(string.digits))
            elif c == "4":
                password.append(random.choice(string.punctuation))

        password += random.choices(
            characters, k=length - len(password)
        )
        random.shuffle(password)