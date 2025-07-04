# Datalake

This directory contains sample data in JSON format, organized for easy ingestion into the PostgreSQL database. It simulates a real-world data lake for testing and demonstration purposes.

## Structure
- `inventory/`: Product and inventory items (`item_*.json`)
- `orders/`: Order records (`order_*.json`)
- `users/`: User profiles (`user_*.json`)

## Usage
These files are used by the data population scripts to seed the database with realistic data. You can modify or extend them to fit your own scenarios.

## Example
```json
   1   │ {
   2   │     "user_id": 1,
   3   │     "order_date": "2024-11-14T13:54:34.899730",
   4   │     "status": "cancelled",
   5   │     "total": 354.96,
   6   │     "items": [
   7   │         {
   8   │             "product_name": "Step",
   9   │             "requested_quantity": 1,
  10   │             "unit_price": 19.11
  11   │         },
  12   │         {
  13   │             "product_name": "Consumer",
  14   │             "requested_quantity": 5,
  15   │             "unit_price": 67.17
  16   │         }
  17   │     ]
  18   │ }
```

---

*No scripts in this directory. Data only.*
