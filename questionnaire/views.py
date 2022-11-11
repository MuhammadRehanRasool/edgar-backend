from statistics import mode
from rest_framework import status
from . import models, serializers
from django.shortcuts import redirect
from authentication.models import CustomUsers
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
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


@api_view(['POST'])
def makePayment(request):
    if request.method == "POST":
        coming_data = JSONParser().parse(request)
        amount = int(coming_data['amount'])*100
        product_name = coming_data['product']
        success_url = coming_data['success_url']
        cancel_url = coming_data['cancel_url']
        user = coming_data['user']
        type = coming_data['type']
        rd = coming_data['redirect']
        if amount == 0:
            addSubscriptionToDatabase(user, type)
            return JsonResponse({'type': "success", 'message': rd}, status=status.HTTP_200_OK)
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
                success_url=success_url,
                cancel_url=cancel_url
            )
        except Exception as e:
            return JsonResponse({'type': "error", 'message':  str(e)})
        return JsonResponse({'type': "success", 'message': checkout_session.url}, status=status.HTTP_200_OK)

# Test


@api_view(['GET', 'POST'])
def topics(request):
    if request.method == "GET":
        user = request.GET.get('user', None)
        if user is None:
            return JsonResponse([], status=status.HTTP_200_OK, safe=False)
        all_ids = models.StudentSubscription.objects.filter(user=int(user))
        fetch_ids = serializers.StudentSubscriptionSerializer(
            all_ids, many=True)
        toExclude = []
        for item in fetch_ids.data:
            toExclude.append(item["type"]["topic"])
        query = models.Topic.objects.all().exclude(pk__in=toExclude)
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
        query = models.Topic.objects.filter(pk=int(request.data["id"])).first()
        serializer = serializers.TopicSerializer(query)
        query_b = models.TopicSubscription.objects.filter(
            topic=int(request.data["id"]))
        serializer_b = serializers.TopicSubscriptionSerializer(
            query_b, many=True)
        return JsonResponse({
            **serializer.data,
            "questionsCount": models.Questions.objects.filter(topic=int(request.data["id"])).count(),
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


def addSubscriptionToDatabase(user, type):
    if user is not None and type is not None:
        query = models.StudentSubscription.objects.create(user=CustomUsers.objects.get(
            pk=int(user)), type=models.TopicSubscription.objects.get(pk=int(type)))


@api_view(['GET'])
@permission_classes([])
def subscriptions(request):
    if request.method == "GET":
        user = request.GET.get('user', None)
        type = request.GET.get('type', None)
        rd = request.GET.get('redirect', None)
        addSubscriptionToDatabase(user, type)
        return redirect(str(rd))


@api_view(['GET'])
@permission_classes([])
def mysubscriptions(request):
    if request.method == "GET":
        user = request.GET.get('user', None)
        all_ids = models.StudentSubscription.objects.filter(user=int(user))
        fetch_ids = serializers.StudentSubscriptionSerializer(
            all_ids, many=True)
        return JsonResponse(fetch_ids.data, status=status.HTTP_200_OK, safe=False)

# Subscriptions
