import tkinter as tk
from tkinter import messagebox
import pandas as pd
import sqlite3
import datetime
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from fpdf import FPDF
from utils.calculator import calculate_total
import os


def init_db():
    conn = sqlite3.connect('db/restaurant.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total REAL,
            gst REAL,
            discount REAL,
            payment_method TEXT,
            order_type TEXT,
            date TEXT
        );
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            item TEXT,
            quantity INTEGER,
            price REAL,
            FOREIGN KEY(order_id) REFERENCES orders(id)
        );
    ''')
    conn.commit()
    conn.close()


class BillingERP:
    def __init__(self, root):
        self.root = root
        self.cart = []
        self.discount = tk.DoubleVar(value=0.0)
        self.selected_order_type = tk.StringVar(value="Dine-In")
        self.selected_payment = tk.StringVar(value="Cash")
        self.total_amount_var = tk.StringVar(value="Total: ₹0.00")
        self.theme = "morph"

        self.style = ttk.Style(theme=self.theme)
        self.root.title("RESTAURANT BILLING ERP")
        self.root.state('zoomed')

        self.setup_layout()
        self.build_header()
        self.build_sidebar()

        self.content_frame = ttk.Frame(self.main_frame, padding=10)
        self.content_frame.pack(fill="both", expand=True)

        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)

        self.show_main_page()
        self.update_time()

    def setup_layout(self):
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.header_frame = ttk.Frame(self.root, bootstyle="dark")
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.sidebar_frame = ttk.Frame(self.root, width=200, bootstyle="info")
        self.sidebar_frame.grid(row=1, column=0, sticky="ns")

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(row=1, column=1, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

    def build_header(self):
        self.title_label = ttk.Label(
            self.header_frame,
            text="🍽️  Restaurant Billing ERP",
            font=("Segoe UI", 22, "bold"),
            bootstyle="inverse-light"
        )
        self.title_label.pack(side="left", padx=20, pady=10)

        self.clock_label = ttk.Label(
            self.header_frame,
            font=("Segoe UI", 12),
            bootstyle="inverse-light"
        )
        self.clock_label.pack(side="right", padx=20)

        self.theme_button = ttk.Button(
            self.header_frame,
            text="🌓 Toggle Theme",
            command=self.toggle_theme,
            bootstyle="secondary"
        )
        self.theme_button.pack(side="right", padx=10)

    def build_sidebar(self):
        ttk.Label(self.sidebar_frame, text="Menu", font=("Segoe UI", 14, "bold"),
                  bootstyle="inverse-info").pack(pady=10)
        ttk.Button(self.sidebar_frame, text="My Profile", bootstyle="secondary-outline", width=20,
                   command=self.show_profile).pack(pady=5)
        ttk.Button(self.sidebar_frame, text="View Menu", bootstyle="secondary-outline", width=20,
                   command=self.show_main_page).pack(pady=5)
        ttk.Button(self.sidebar_frame, text="Trending Menu", bootstyle="secondary-outline", width=20).pack(pady=5)
        ttk.Button(self.sidebar_frame, text="Order History", bootstyle="secondary-outline", width=20).pack(pady=5)
        ttk.Button(self.sidebar_frame, text="Clear Cart", bootstyle="danger", width=20,
                   command=self.clear_cart).pack(pady=5)
        ttk.Button(self.sidebar_frame, text="Exit", bootstyle="secondary-outline", width=20,
                   command=self.root.quit).pack(pady=5)

        # PAGE SWITCHING
    
    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_main_page(self):
        self.clear_content_frame()
        menu_data = pd.read_csv('data/menu.csv')

        # ITEM ENTRY
        
        card = ttk.Frame(self.content_frame, padding=20, bootstyle="info")
        card.grid(row=0, column=0, pady=10, sticky="ew")

        ttk.Label(card, text="Add Item to Cart", font=("Segoe UI", 14, "bold"),
                  foreground="black").grid(row=0, column=0, columnspan=2, pady=10)

        ttk.Label(card, text="Item:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.item_combo = ttk.Combobox(card, values=list(menu_data['item']), width=30)
        self.item_combo.grid(row=1, column=1, pady=5)

        ttk.Label(card, text="Quantity:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.quantity_spinbox = ttk.Spinbox(card, from_=1, to=50, width=30)
        self.quantity_spinbox.grid(row=2, column=1, pady=5)

        ttk.Button(card, text="Add to Cart", bootstyle="success",
                   command=self.add_to_cart).grid(row=3, column=0, columnspan=2, pady=10)

        # CART TREEVIEW
        
        cart_card = ttk.Frame(self.content_frame, padding=10, bootstyle="light")
        cart_card.grid(row=1, column=0, pady=10, sticky="nsew")  # expands now

        self.cart_tree = ttk.Treeview(cart_card, columns=("Item", "Qty", "Price"),
                                      show="headings", height=10, bootstyle="info")
        self.cart_tree.heading("Item", text="Item")
        self.cart_tree.heading("Qty", text="Quantity")
        self.cart_tree.heading("Price", text="Unit Price")
        self.cart_tree.pack(fill="both", expand=True)

        ttk.Button(cart_card, text="Remove Selected", bootstyle="danger-outline",
                   command=self.remove_selected).pack(pady=5)

        self.total_details_label = ttk.Label(cart_card, text="", font=("Segoe UI", 10, "bold"))
        self.total_details_label.pack(anchor="e", pady=(5, 0))

        # ORDER OPTIONS
        
        options_card = ttk.Frame(self.content_frame, padding=15, bootstyle="primary")
        options_card.grid(row=2, column=0, pady=10, sticky="ew")

        ttk.Label(options_card, text="Order Type").grid(row=0, column=0, padx=10)
        ttk.Combobox(options_card, textvariable=self.selected_order_type,
                     values=["Dine-In", "Takeaway"], width=15).grid(row=0, column=1)

        ttk.Label(options_card, text="Payment").grid(row=0, column=2, padx=10)
        ttk.Combobox(options_card, textvariable=self.selected_payment,
                     values=["Cash", "Card", "UPI"], width=15).grid(row=0, column=3)

        ttk.Label(options_card, text="Discount (%)").grid(row=0, column=4, padx=10)
        ttk.Entry(options_card, textvariable=self.discount, width=10).grid(row=0, column=5)

        ttk.Button(options_card, text="Checkout", command=self.checkout,
                   bootstyle="success").grid(row=0, column=6, padx=20)

        self.total_label = ttk.Label(self.content_frame, textvariable=self.total_amount_var,
                                     font=("Segoe UI", 16, "bold"))
        self.total_label.grid(row=3, column=0, pady=5, sticky="e")

    def show_profile(self):
        self.clear_content_frame()
        profile_card = ttk.Frame(self.content_frame, padding=30, bootstyle="light")
        profile_card.pack(expand=True, fill="both")

        ttk.Label(profile_card, text="My Profile", font=("Segoe UI", 22, "bold")).pack(pady=10)
        ttk.Label(profile_card, text="Name: Atharva Mandlik", font=("Segoe UI", 14)).pack(pady=5)
        ttk.Label(profile_card, text="Mobile: 1234567890", font=("Segoe UI", 14)).pack(pady=5)
        ttk.Label(profile_card, text="Email: atharva@example.com", font=("Segoe UI", 14)).pack(pady=5)

        ttk.Button(profile_card, text="← Back", bootstyle="secondary",
                   command=self.show_main_page).pack(pady=10)

        ttk.Button(profile_card, text="Delete Account", bootstyle="danger").pack(pady=15)

        # CORE FUNCTIONS
    
    def update_time(self):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.clock_label.configure(text=now)
        self.root.after(1000, self.update_time)

    def toggle_theme(self):
        self.theme = "cyborg" if self.theme == "morph" else "morph"
        self.style.theme_use(self.theme)

    def add_to_cart(self):
        item = self.item_combo.get()
        qty = self.quantity_spinbox.get()
        if not item or not qty.isdigit():
            messagebox.showerror("Input Error", "Please select an item and a valid quantity.")
            return
        try:
            menu_data = pd.read_csv('data/menu.csv')
            price = float(menu_data.loc[menu_data['item'] == item, 'price'].values[0])
        except Exception:
            messagebox.showerror("Data Error", "Price not found for selected item.")
            return
        self.cart.append({'item': item, 'quantity': int(qty), 'price': price})
        self.refresh_cart()

    def refresh_cart(self):
        self.cart_tree.delete(*self.cart_tree.get_children())
        total_qty = 0
        total_price = 0
        for i, entry in enumerate(self.cart):
            self.cart_tree.insert('', 'end', iid=i,
                                  values=(entry['item'], entry['quantity'], entry['price']))
            total_qty += entry['quantity']
            total_price += entry['quantity'] * entry['price']
        self.total_details_label.config(
            text=f"Total Qty: {total_qty}     Total Price: ₹{total_price:.2f}"
        )
        subtotal, gst, total = calculate_total(self.cart, gst_rate=5, discount=self.discount.get())
        self.total_amount_var.set(f"Total: ₹{total:.2f}")

    def remove_selected(self):
        selected = self.cart_tree.selection()
        if not selected:
            return
        for iid in selected:
            self.cart.pop(int(iid))
        self.refresh_cart()

    def clear_cart(self):
        self.cart.clear()
        self.refresh_cart()

    def checkout(self):
        if not self.cart:
            messagebox.showwarning("Empty Cart", "No items to checkout.")
            return

        subtotal, gst, total = calculate_total(self.cart, gst_rate=5, discount=self.discount.get())
        payment = self.selected_payment.get()
        order_type = self.selected_order_type.get()
        date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = sqlite3.connect('db/restaurant.db')
        c = conn.cursor()
        c.execute("INSERT INTO orders (total, gst, discount, payment_method, order_type, date) VALUES (?, ?, ?, ?, ?, ?)",
                  (total, gst, self.discount.get(), payment, order_type, date_time))
        order_id = c.lastrowid
        for item in self.cart:
            c.execute("INSERT INTO order_items (order_id, item, quantity, price) VALUES (?, ?, ?, ?)",
                      (order_id, item['item'], item['quantity'], item['price']))
        conn.commit()
        conn.close()

        df = pd.DataFrame(self.cart)
        df['total_price'] = df['price'] * df['quantity']
        df.to_csv(f"data/bill_{order_id}.csv", index=False)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Restaurant Bill", ln=True, align='C')
        pdf.cell(200, 10, txt=f"Order ID: {order_id} | Date: {date_time}", ln=True, align='C')
        pdf.ln(10)
        for item in self.cart:
            pdf.cell(200, 10, txt=f"{item['item']} x{item['quantity']} = ₹{item['price'] * item['quantity']}",
                     ln=True)
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Subtotal: ₹{subtotal}", ln=True)
        pdf.cell(200, 10, txt=f"GST (5%): ₹{gst}", ln=True)
        pdf.cell(200, 10, txt=f"Discount: ₹{self.discount.get()}", ln=True)
        pdf.cell(200, 10, txt=f"Total: ₹{total}", ln=True)
        pdf.output(f"data/bill_{order_id}.pdf")

        messagebox.showinfo("Success", f"Order #{order_id} completed! Bill saved.")
        self.cart.clear()
        self.refresh_cart()


def run_app():
    init_db()
    root = tk.Tk()
    BillingERP(root)
    root.mainloop()


if __name__ == "__main__":
    run_app()
