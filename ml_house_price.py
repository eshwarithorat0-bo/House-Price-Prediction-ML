import csv

def train_model(data):
    # Fit price = a*area + b*bedrooms + c
    n = len(data)
    if n < 3:
        raise ValueError("Dataset needs at least 3 rows.")

    # Simple multiple linear regression using gradient descent
    areas = [row[0] for row in data]
    bedrooms = [row[1] for row in data]
    prices = [row[2] for row in data]

    mean_area = sum(areas) / n
    mean_bedrooms = sum(bedrooms) / n
    mean_price = sum(prices) / n

    scale_area = max(max(areas) - min(areas), 1)
    scale_bedrooms = max(max(bedrooms) - min(bedrooms), 1)

    a = b = 0.0
    c = mean_price
    rate = 0.01

    for _ in range(20000):
        da = db = dc = 0.0

        for area, bed, price in data:
            x1 = (area - mean_area) / scale_area
            x2 = (bed - mean_bedrooms) / scale_bedrooms
            error = a*x1 + b*x2 + c - price
            da += error*x1
            db += error*x2
            dc += error

        a -= rate * 2 * da / n
        b -= rate * 2 * db / n
        c -= rate * 2 * dc / n

    return a, b, c, mean_area, mean_bedrooms, scale_area, scale_bedrooms

try:
    data = []

    with open("house_data.csv", "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            data.append((
                float(row["Area"]),
                float(row["Bedrooms"]),
                float(row["Price"])
            ))

    model = train_model(data)
    a, b, c, ma, mb, sa, sb = model

    print("=" * 40)
    print("HOUSE PRICE PREDICTION")
    print("Model trained using sample dataset")
    print("=" * 40)

    while True:
        area = float(input("Enter house area in sq.ft: "))
        bedrooms = float(input("Enter number of bedrooms: "))

        if area <= 0 or bedrooms <= 0:
            print("Enter positive values only.")
            continue

        price = a*((area-ma)/sa) + b*((bedrooms-mb)/sb) + c

        print("\n--- PREDICTION RESULT ---")
        print(f"Area: {area:,.0f} sq.ft")
        print(f"Bedrooms: {bedrooms:.0f}")
        print(f"Estimated Price: Rs. {price:,.2f}")

        again = input("\nPredict another house? (yes/no): ")
        if again.strip().lower() != "yes":
            break

except FileNotFoundError:
    print("Error: house_data.csv was not found in this folder.")
except (ValueError, KeyError) as error:
    print("Check the CSV column names and numeric values:", error)
    