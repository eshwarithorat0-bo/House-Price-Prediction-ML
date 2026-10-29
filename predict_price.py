# HOUSE PRICE PREDICTION MINI PROJECT

areas = [500, 700, 900, 1100, 1300]
prices = [1500000, 2200000, 2800000, 3500000, 4200000]

price_per_sqft = sum(
    prices[i] / areas[i] for i in range(len(areas))
) / len(areas)

print("=" * 45)
print("       HOUSE PRICE PREDICTION")
print("=" * 45)

while True:
    print("\nEnter house details:")

    try:
        area = float(input("Enter house area in sq.ft: "))
        bedrooms = int(input("Enter number of bedrooms: "))

        if area <= 0 or bedrooms <= 0:
            print("Please enter positive numbers only.")
            continue

        predicted_price = area * price_per_sqft

        print("\n--- PREDICTION RESULT ---")
        print(f"House Area: {area:,.0f} sq.ft")
        print(f"Bedrooms: {bedrooms}")
        print(f"Estimated Price: ₹{predicted_price:,.2f}")

    except ValueError:
        print("Invalid input! Please enter numbers only.")
        continue

    again = input("\nPredict another house? (yes/no): ").strip().lower()

    if again != "yes":
        print("\nThank you for using House Price Prediction!")
        break