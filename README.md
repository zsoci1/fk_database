# About the project

This project was created for a small company that delivers personalized meals for a whole day (breakfast, lunch, snack, and dinner) with given meal sizes (S, M, L, XL) and allergenic options (gluten-free, lactose-free, without specific ingredients, etc.).
The deliveries happen from Sunday to Thursday, and the customers get their order the day before (the meals for Monday are delivered on Sunday).

The client wanted to automate the daily breakdown for each day, for the kitchen and for the delivery staff, while having control over customer information such as subscription, size, type, and number of meals. The ultimate goal for the client was two automated Excel sheets for each day, one containing information for the kitchen staff about the number of orders for a given type and size, and the allergens, and one for the delivery staff about the customers (name, address, phone number) and the meals for that day.

The language of the UI and the documentation of the codebase is Hungarian.

# Tech stack

For the database, SQLite was used since the client wanted to store all data locally on their computer.
A relational database was created with two tables, one that holds information about the customers and the other about the meals for a given date. 
UI - customtkinter
Writing Excel files - openpyxl


UI design and collaborator: @dop14

# Install

1. clone the repository
2. install requirements
3. run main.py