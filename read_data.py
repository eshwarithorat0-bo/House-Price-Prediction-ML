import csv

print("HOUSE PRICE DATASET")
print("-" * 40)

with open("house_data.csv", "r", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        print(
            "Area:", row["Area"], "sq.ft |",
            "Bedrooms:", row["Bedrooms"], "|",
            "Price: ₹", row["Price"]
        )
        