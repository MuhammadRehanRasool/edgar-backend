from rest_framework import status
from . import models
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes

from django.shortcuts import redirect
# Stripe import
import stripe

stripe.api_key = 'sk_test_51LvflpEzOnSWJxP5wAUZaz0GwCcFO4aawZd9G91v8wUSiDV2NYC2y7FiZpkMnsWLCxFJcPqpGz7vwfU9Z4OrC4R0009X88pIFs'


@api_view(['GET', 'POST'])
@permission_classes([])
def testing(request):
    if request.method == "GET":
        res = stripe.Product.search(
            query="name:'Maths' ",
        )

        print(res)
        return JsonResponse({'message': res}, status=status.HTTP_200_OK)
    if request.method == "POST":
        coming_data = JSONParser().parse(request)
        amount = coming_data['amount']*100
        product_name = coming_data['product']
        try:
            product = stripe.Product.create(name=product_name)
            pr_price = stripe.Price.create(
                unit_amount=amount,
                currency="usd",
                product=product.id,
            )

            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price': pr_price.id,
                        'quantity': 1,
                    },

                ],
                mode='payment',
                # success_url='localhost:3000/' + \
                # '?success=true&session_id={CHECKOUT_SESSION_ID}',
                # cancel_url='localhost:3000/' + '?canceled=true',
                success_url='https://github.com/',
                cancel_url='https://github.com/abrar-11',
            )
        except Exception as e:
            return JsonResponse({'Error':  str(e)}, status=500)
        print(checkout_session.url)
        # return redirect(checkout_session.url)
        return JsonResponse({'message': checkout_session.url}, status=status.HTTP_200_OK)
