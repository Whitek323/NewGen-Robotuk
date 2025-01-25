import json

# Step 1: Read the JSON file
with open('data.json', 'r') as file:
    data = json.load(file)

# Step 2: Loop through the data
for item in data:
    # Step 3: Print each item
    print(item)
