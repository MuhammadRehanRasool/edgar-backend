from rest_framework import serializers
from . import models
from authentication.models import CustomUsers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUsers
        fields = ['pk', 'username', 'email', 'name']


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subject
        fields = '__all__'


class NameOfSubscriptionTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SubscriptionTypes
        fields = ['title', 'expiryHours']


class TopicSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()
    subscription_types = NameOfSubscriptionTypesSerializer(many=True)

    class Meta:
        model = models.Topic
        fields = '__all__'


class TopicSubscriptionSerializer(serializers.ModelSerializer):
    subscription_types = NameOfSubscriptionTypesSerializer()

    class Meta:
        model = models.TopicSubscription
        fields = '__all__'


class StudentSubscriptionSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    type = TopicSubscriptionSerializer()

    class Meta:
        model = models.StudentSubscription
        fields = '__all__'


# class CountrySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Country
#         fields = '__all__'


# class AirlineSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AirlineCompany
#         fields = '__all__'


# class TicketSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Ticket
#         fields = '__all__'
