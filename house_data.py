# House Price Prediction - Sample Dataset

area = [500, 700, 900, 1100, 1300]
bedrooms = [1, 2, 2, 3, 3]
prices = [1500000, 2200000, 2800000, 3500000, 4200000]

print("HOUSE DATASET")
print("--------------------")

for i in range(len(area)):
    print("Area:", area[i], "sq.ft")
    print("Bedrooms:", bedrooms[i])
    print("Price: Rs.", prices[i])
    print("--------------------")
    