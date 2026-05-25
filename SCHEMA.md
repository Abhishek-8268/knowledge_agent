# Database Schema

This project uses a local SQLite database with an E-commerce domain to test text-to-SQL capabilities. 

## Tables & Relationships

1. **`customers`**
   - `customer_id` (INTEGER, Primary Key): Unique identifier.
   - `name` (TEXT): Customer's full name.
   - `city` (TEXT): Customer's location.

2. **`products`**
   - `product_id` (INTEGER, Primary Key): Unique identifier.
   - `name` (TEXT): Product name.
   - `category` (TEXT): Broad grouping (e.g., Apparel, Food, Tech).
   - `price` (REAL): Cost per unit.

3. **`orders`**
   - `order_id` (INTEGER, Primary Key): Unique identifier.
   - `customer_id` (INTEGER, Foreign Key): Links to `customers`.
   - `product_id` (INTEGER, Foreign Key): Links to `products`.
   - `order_date` (TEXT): YYYY-MM-DD format.
   - `quantity` (INTEGER): Number of items purchased.

## Design Rationale
This 3-table normalized structure ensures data integrity. By separating customers and products from the orders table, we avoid duplicating static information (like a customer's city or a product's price) every time a new transaction occurs. This fulfills the requirement for at least 3 related tables while remaining straightforward for the LLM to write SQL against.