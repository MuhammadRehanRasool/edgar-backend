from statistics import mode
from rest_framework import status
from . import models, serializers
from authentication.models import CustomUsers
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes

from django.shortcuts import redirect
# Stripe import
import stripe
import json

stripe.api_key = 'sk_test_51LyNIZJwTuApoB7Ms8joJ1fORtVdu9sohKVSy1KoZJALIWKCsv7sST3AVYfWpfoEis9gvsPK6JRlZLyFFQhjmKhG00VJdbjvll'


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


@api_view(['POST'])
def makePayment(request):
    if request.method == "POST":
        coming_data = JSONParser().parse(request)
        amount = int(coming_data['amount'])*100
        product_name = coming_data['product']
        success_url = coming_data['success_url']
        cancel_url = coming_data['cancel_url']
        redirect = coming_data['redirect']
        try:
            product_id = getProductIdFromStripe(product_name)
            pr_price = getPriceIdFromStripe(amount, product_id)
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': pr_price,
                        'quantity': 1,
                    },

                ],
                mode='payment',
                success_url=success_url+"&redirect="+redirect,
                cancel_url=cancel_url
            )
        except Exception as e:
            return JsonResponse({'type': "error", 'message':  str(e)})
        return JsonResponse({'type': "success", 'message': checkout_session.url}, status=status.HTTP_200_OK)

# Test


@api_view(['GET', 'POST'])
def topics(request):
    if request.method == "GET":
        query = models.Topic.objects.all()
        serializer = serializers.TopicSerializer(query, many=True)
        payload = []
        try:
            for item in serializer.data:
                query_b = models.TopicSubscription.objects.filter(
                    topic=item["id"])
                serializer_b = serializers.TopicSubscriptionSerializer(
                    query_b, many=True)
                payload.append({
                    **item,
                    "subscriptions": serializer_b.data})
        except Exception as e:
            print(e)
            return JsonResponse({'message': "Error!"}, status=status.HTTP_200_OK)
        return JsonResponse(payload, status=status.HTTP_200_OK, safe=False)
    if request.method == "POST":
        query = models.Topic.objects.filter(pk=request.data["id"]).first()
        serializer = serializers.TopicSerializer(query)
        query_b = models.TopicSubscription.objects.filter(
            topic=request.data["id"])
        serializer_b = serializers.TopicSubscriptionSerializer(
            query_b, many=True)
        return JsonResponse({
            **serializer.data,
            "questionsCount": 170,
            "subscriptions": serializer_b.data
        }, status=status.HTTP_200_OK)

# Topics


@api_view(['GET'])
def plans(request):
    if request.method == "GET":
        query = models.SubscriptionTypes.objects.all()
        serializer = serializers.NameOfSubscriptionTypesSerializer(
            query, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

# Plans


@api_view(['GET'])
@permission_classes([])
def subscriptions(request):
    if request.method == "GET":
        user = request.GET.get('user', None)
        type = request.GET.get('type', None)
        redirect = request.GET.get('redirect', None)
        print(redirect)
        if user is not None and type is not None:
            query = ""
            # query = models.StudentSubscription.objects.create(
            #     user=CustomUsers.objects.get(pk=user), type=models.TopicSubscription.objects.get(pk=type))
            if query:
                return JsonResponse({'type': "success", 'message':  "Done!"}, status=500)
        return JsonResponse({'type': "error", 'message':  "Invalid!"}, status=500)

# Subscriptions
