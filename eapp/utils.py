def count_carts(cart):
    total_quantity = 0
    total_price = 0
    if cart:
        for item in cart.values():
            total_quantity += item['quantity']
            total_price += item['quantity'] * item['price']
    return{
        'total_quantity': total_quantity,
        'total_price': total_price
    }