import json
from . models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('Cart:', cart)

        
        
    items = []
    order = {'get_cart_total':0, 'get_cart_items':0}
    cartItems = order['get_cart_items']
    for x in cart:
        try:
            cartItems += cart[x]["quantity"]
            product = Product.objects.get(id=x)
            total = (product.price * cart[x]["quantity"])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[x]['quantity']
            item ={
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,
                    },
                'quantity':cart[x]['quantity'],
                'get_total':total

                }
            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    return {'cartItems':cartItems, 'order':order, 'items':items}
    
def cartData(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            Customer.objects.get(user = user)
        except Exception as error:
            print(error)

            customer = Customer.create(user, user.username, user.email) 
            customer.save()
        customer = Customer.objects.get(user = user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return{'cartItems':cartItems, 'order':order, 'items':items}

def guestOrder(request, data):
    print('User is Not logged in... ')
    print('COOkIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']
        
    cookieData = cookieCart(request)
    items = cookieData['items']
    """writing to database for guest"""
    customer, created = Customer.objects.get_or_create(
        email = email,
    )
        
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer = customer,
        complete = False,
    )
        
    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    return customer, order
