import random
import datetime, dateutil.parser

# Constants
NB_ORDERS = 200_000
MAX_ORDER_ID = 999_999

NB_USERS = 10_000
MAX_USER_ID = 999_999

MAX_PRICE = 10_000

MAX_DISCOUNT = 99

START_DATE = "2020-01-01"
END_DATE = "2023-12-31"

FILENAME = "orders.csv"

# Util functions
def generate_order_metadata(discount):
    return {
        "price": random.randint(1, MAX_PRICE),
        "discount": random.randint(1, MAX_DISCOUNT) if discount else 0,
        "date": datetime.datetime.strftime(
            random_date(START_DATE, END_DATE), "%Y-%m-%d"
        ),
    }

def random_date(start, end):
    start = dateutil.parser.parse(start)
    end = dateutil.parser.parse(end)
    return start + datetime.timedelta(
        seconds=random.randint(0, int((end - start).total_seconds()))
    )

def generate_unique_integers(number_of_values, min_value, max_value):
    assert(number_of_values <= (max_value - min_value + 1))
    return random.sample(range(min_value, max_value + 1), number_of_values)

# Generate unique integers for user and order ids
user_ids = generate_unique_integers(NB_USERS, 1, MAX_USER_ID)
print(f"[*] Generated {len(user_ids)} unique user ids")
order_ids = generate_unique_integers(NB_ORDERS, 1, MAX_ORDER_ID)
print(f"[*] Generated {len(order_ids)} unique order ids")

# Generate orders
orders = []
for order_id in order_ids:
    buyer = random.choice(user_ids)
    seller = buyer
    while seller == buyer:
        seller = random.choice(user_ids)
    discount = random.choice([True, False])
    metadata = generate_order_metadata(discount)
    orders.append(
        {
            "order_id": order_id,
            "buyer_id": buyer,
            "seller_id": seller,
            "price": metadata["price"],
            "discount": metadata["discount"],
            "date": metadata["date"],
        }
    )
print(f"[*] Generated {len(orders)} orders")

# Convert to CSV
import csv

with open(FILENAME, "w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["order_id", "buyer_id", "seller_id", "price", "discount", "date"],
    )
    writer.writeheader()
    for order in orders:
        writer.writerow(order)
print(f"[*] Saved orders to {FILENAME}")