# File: utils/calculator.py

def calculate_total(cart, gst_rate=5, discount=0):
    """
    Calculates subtotal, GST, and total for the cart.

    Parameters:
        cart (list): List of items in the format:
                     [{'item': 'ItemName', 'quantity': int, 'price': float}, ...]
        gst_rate (float): GST percentage to apply.
        discount (float): Flat discount amount to subtract.

    Returns:
        tuple: (subtotal, gst, total) all rounded to 2 decimal places.
    """
    if not cart:
        return 0.0, 0.0, 0.0

    try:
        discount = max(0, float(discount))  # Ensure non-negative discount
    except ValueError:
        discount = 0.0

    subtotal = sum(item['price'] * item['quantity'] for item in cart)
    gst = (gst_rate / 100) * subtotal
    total = subtotal + gst - discount

    return round(subtotal, 2), round(gst, 2), round(total, 2)
