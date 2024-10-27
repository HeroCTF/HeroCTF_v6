import pandas as pd
pd.options.mode.chained_assignment = None 

# Load file
FILENAME = "orders.csv"
orders_df = pd.read_csv(FILENAME)

# Filter out transactions before 2023-01-01
orders_df['date'] = pd.to_datetime(orders_df['date'])
filtered_orders = orders_df[orders_df['date'] < '2023-01-01']

# Calculate price after discount
filtered_orders['effective_price'] = filtered_orders['price'] * (1 - filtered_orders['discount'] / 100)
filtered_orders['effective_price'] = filtered_orders['effective_price']

# Initialize balances
initial_balance = 10000
unique_ids = set(filtered_orders['buyer_id']).union(set(filtered_orders['seller_id']))
balances = {uid: initial_balance for uid in unique_ids}

# Update balances based on transactions
for index, row in filtered_orders.iterrows():
    buyer_id = row['buyer_id']
    seller_id = row['seller_id']
    effective_price = row['effective_price']

    balances[buyer_id] -= effective_price
    balances[seller_id] += effective_price

# Calculate total spared through discounts
total_discount = int((filtered_orders['price'] - filtered_orders['effective_price']).sum())

# Count negative balances
negative_balances_count = sum(1 for balance in balances.values() if balance < 0)

# Person with the highest balance
wealthiest_person = max(balances, key=balances.get)
highest_balance = balances[wealthiest_person]

print(f"Hero{{{wealthiest_person}_{total_discount}_{negative_balances_count}}}")