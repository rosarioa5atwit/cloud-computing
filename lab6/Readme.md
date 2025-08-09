This project is the back_End service for a the portion of the guitar shop database for lab 4. It has 10 routes with both Put and Get verbs.


INstructions 
Replace the information DeCONFIG in the driver.py file with your lab 4 database information. Then Run `python driver.py` to access a menu for direct database operations, including options to retrieve and update orders, products, and customers.Start the server with `python main.py`, which will be accessible at `http://localhost:8001`. Here are the available API routes. These routes include:
1.  /orders/{order_id}: This endpoint retrieves the details of a specific order using its unique identifier (order ID). It returns information such as the items included in the order, the customer details, order status, and timestamps. 
2. /products/code/{product_code}: This endpoint allows you to get information about a specific product by its unique product code. The response includes details like the product name, description, price, availability, and other relevant specifications. 
3. /customers/{customer_id}/orders : This retrieves a list of all orders placed by a specific customer identified by their unique customer ID. It helps in tracking customer activity and order history.
 4.  /orders/date/{date}: This endpoint retrieves orders that were placed on a specific date. It can be utilized for reporting and analytics purposes, allowing businesses to monitor daily sales and order trends.
 5.  /customers/update/{customer_id} : This endpoint updates information for a specific customer identified by their customer ID. The operation may involve interactive prompts to collect updated details such as name, email, address, and phone number from the user. 
6.  /categories/update/{category_id} : Similar to the customer update, this endpoint modifies the details of a particular product category. It may involve interactive prompts to gather new category names, descriptions, or attributes.
 7./orders/update/{order_id}: This endpoint enables the modification of an existing order identified by its order ID. Interactive prompts may be used to collect new details such as item quantities, customer notes, or order status. 
8. /products: This retrieves a list of products, potentially with optional filters for searching specific product attributes (like category, price range, availability, etc.). This is useful for displaying products in a retail interface. 
9. /customers: This retrieves a list of customers, again with potential filters for searching by attributes such as name, email, or registration date. This is useful for managing customer relationships and support. 10. 10.  /products/update/{product_id}: This endpoint allows for the updating of product information for a specific product identified by its ID. Interactive prompts may be used to gather new details, including changes to name, price, description, and stock levels.


Run `python test.py` to automatically test all endpoints or select an interactive menu for individual endpoint testing.

Screenshots are in the screenshot folder
