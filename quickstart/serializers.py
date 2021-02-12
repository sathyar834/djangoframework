from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *


class createOUSerializer(serializers.ModelSerializer):
  class Meta:
    model = createOU
    # fields = ('Enter the Id of the parent where the OU has to be created','Enter the list of names on which the OU has to be created')
    fields = ('OUname','ParentId')

class listrootSerializer(serializers.ModelSerializer):
  class Meta:
    model = listroot
    fields = ('rootId')

class listOUSerializer(serializers.ModelSerializer):
  class Meta:
    model = listOU
    # fields = ('Enter the Id of the parent OU whose child OUs you want to list',)
    fields = ('ParentIdlistou',)

class createaccountSerializer(serializers.ModelSerializer):
  class Meta:
    model = createaccount
    fields = ('Email','Name')

class moveaccountSerializer(serializers.ModelSerializer):
  class Meta:
    model = moveaccount
    fields = ('AccountId','SourceId','DestinationId')

class createscpSerializer(serializers.ModelSerializer):
  class Meta:
    model = createscp
    fields = ('SCPDescription','SCPName','Documentname')

class attachscpSerializer(serializers.ModelSerializer):
  class Meta:
    model = attachscp
    fields = ('SCPPolicyId','AccountId')