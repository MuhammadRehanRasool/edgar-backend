from rest_framework import status
from . import models
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes

from django.shortcuts import redirect
# Stripe import
import stripe
import json

stripe.api_key = 'sk_test_51LvflpEzOnSWJxP5wAUZaz0GwCcFO4aawZd9G91v8wUSiDV2NYC2y7FiZpkMnsWLCxFJcPqpGz7vwfU9Z4OrC4R0009X88pIFs'


def getProductIdFromStripe(product_name):
    product_search = stripe.Product.search(
        query="name:'"+product_name+"' ",
    )
    product_id = None
    if len(product_search["data"]) != 0:
        product_id = product_search["data"][0]["id"]
    else:
        product_id = stripe.Product.create(name=product_name).id
    return product_id


def getPriceIdFromStripe(original_amount, product_id):
    price_search = stripe.Price.search(
        query="product:'"+product_id+"' ",
    )
    price_id = None
    for temp in price_search:
        if int(original_amount) == int(temp["unit_amount"]):
            price_id = temp["id"]
    if price_id is None:
        price_id = stripe.Price.create(
            unit_amount=original_amount,
            currency="usd",
            product=product_id,
        ).id
    return price_id


@api_view(['GET', 'POST'])
@permission_classes([])
def testing(request):
    if request.method == "GET":
        # price_id = getPriceIdFromStripe(70, "prod_Mf890XCCTDw51d")
        # print(price_id)
        query = models.Topic.objects.all()
        print(query.values_list())
        return JsonResponse({'message': ""}, status=status.HTTP_200_OK)
    if request.method == "POST":
        coming_data = JSONParser().parse(request)
        amount = int(coming_data['amount'])*100
        product_name = coming_data['product']
        try:
            product_id = getProductIdFromStripe(product_name)
            pr_price = getPriceIdFromStripe(amount, product_id)
            # print("Amount", amount)
            # print("product_name", product_name)
            # print("product_id", product_id)
            # print("pr_price", pr_price)
            # print("\n\n\khatam tata")
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': pr_price,
                        'quantity': 1,
                    },

                ],
                mode='payment',
                # success_url='localhost:3000/' + \
                # '?success=true&session_id={CHECKOUT_SESSION_ID}',
                # cancel_url='localhost:3000/' + '?canceled=true',
                success_url='https://github.com/',
                cancel_url='https://github.com10lk236o566t',
            )
        except Exception as e:
            return JsonResponse({'Error':  str(e)}, status=500)
        print(checkout_session.url)
        # return redirect(checkout_session.url)
        return JsonResponse({'message': checkout_session.url}, status=status.HTTP_200_OK)
