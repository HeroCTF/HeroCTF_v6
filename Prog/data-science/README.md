# Data Science

### Category

Prog

### Description

Here is a database of sells on a online marketplace. Your job as a data analyst is to answer the following questions :
1. If at 2019-12-31 (at the beginning) every person has 10000$, who has the most money by 2023-01-01 (transaction of that day **excluded**)?
2. By 2023-01-01 (transaction of that day **excluded**) how much money was spared through discounts?
3. By 2023-01-01 (transaction of that day **excluded**) how many people have a negative balance?

Here are some information about the database fields:
| Field name | Data type  | Constraints             |
|------------|------------|-------------------------|
| order_id   | integer    | 1 < order_id < 1 000 000  |
| buyer_id   | integer    | 1 < buyer_id < 1 000 000  |
| seller_id  | integer    | 1 < seller_id < 1 000 000 |
| price      | integer    | 1 < price < 1 000       |
| discount % | integer    | 0 < discount < 100      |
| date       | date       | yyyy-mm-dd              |

Additionally, you should know that Buyers and Sellers are reprensted by a unique ID and are correlated. Buyer 163564 is the same person as Seller 163564.

Prices should be **floored** to the nearest integer, but only at the final stage of the calculation.

e.g. If there are two discounts bringing prices down from 10 and 5 to 8.64 and 4.32 respectively, the amount of money spared is `10 + 5 - 8.64 - 4.32 = 2.04 ~= 2`. As you can see, the only rounding operation was done on the very last value, used in the flag.

The flag is Hero{response1_response2_reponse3}.

e.g. Hero{163564_21673_78}

Format : **Hero{flag}**<br>
Author : **Log_s**

### Files

- [orders.csv](orders.csv)

### Write Up

This is a rather easy problem to solve, the trick is going about it methodically. Here is a step by step guide to solve this problem:
1. Parse the input file
2. Filter out the time period of interest
3. Calculate the price after discount for each transaction
4. Initialize the balance of each person to 10000
5. Update the balance of each person after each transaction
6. Calculate the 3 end values we need

Here is a python script that does just that:

```python
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
```

### Flag

Hero{732669_188098001_3468}