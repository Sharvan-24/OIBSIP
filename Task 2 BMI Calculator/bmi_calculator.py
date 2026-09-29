
print("===== BMI CALCULATOR =====")

weight = float(input("Enter your weight (kg): "))
height_feet = float(input("Enter your height (feet): "))

# Convert feet into meters
height = height_feet * 0.3048

# Calculate BMI
bmi = weight / (height ** 2)

print(f"\nYour BMI is: {bmi:.2f}")

if bmi < 18.5:
    print("Category: Underweight")
elif bmi < 25:
    print("Category: Normal weight")
elif bmi < 30:
    print("Category: Overweight")
else:
    print("Category: Obese")