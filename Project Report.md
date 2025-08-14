Project Report: Restaurant Billing ERP System

1. Introduction
The Restaurant Billing ERP System is a comprehensive desktop application designed to manage restaurant orders, billing, and reporting in an efficient and user-friendly way. It uses a graphical user interface (GUI) to simplify the process of order entry, cart management, checkout, and bill generation in both CSV and PDF formats. The system also integrates with a database to store orders and items for historical reference and analysis.

2. Objectives
The main objectives of the project are:
• Provide a modern GUI for billing.
• Maintain a database of orders.
• Auto-calculate totals with GST and discounts.
• Generate bills in PDF and CSV formats.
• Enable easy navigation with a sidebar menu.

3. Technologies Used
Programming Language: Python 3.x
Libraries and Frameworks:
• Tkinter – GUI creation
• ttkbootstrap – Modern ERP-style styling
• Pandas – CSV file handling
• SQLite3 – Local database storage
• datetime – Date and time management
• FPDF – PDF bill generation
Database: SQLite (restaurant.db) with tables 'orders' and 'order_items'

4. System Features
• ERP-style interface with header and sidebar.
• Live clock display in the header.
• Theme switching between light and dark modes.
• Add to Cart functionality with item and quantity selection.
• Cart management: remove items or clear cart.
• Order type and payment method selection.
• Automatic GST and discount calculations.
• Bill generation in PDF and CSV formats.
• Orders stored in local database.

5. Workflow
1. Start application and initialize database.
2. Load menu from CSV file.
3. User selects items and adds to cart.
4. Set order type, payment method, and discount.
5. Checkout: save order to database.
6. Generate bill in PDF and CSV formats.
7. Display success message.

6. Outputs
• GUI interface with main page and profile page.
• CSV file output for each bill.
• PDF file output for printable bills.

7. Advantages
• Easy to use, even for non-technical staff.
• Works offline with local database.
• Professional printable bills.
• Modular design for easy expansion.
• Quick order processing.

8. Future Enhancements
• Implement trending menu and order history pages.
• Add sales reports with charts.
• Multi-user login with role-based permissions.
• Integrate barcode scanner for item entry.
• Create mobile/tablet version.

9. Conclusion
The Restaurant Billing ERP System successfully modernizes the billing process in restaurants, offering a fast, accurate, and professional solution. With its modular design, it is scalable for future enhancements, making it suitable for small to medium-sized restaurants.
