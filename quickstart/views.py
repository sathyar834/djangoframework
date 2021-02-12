from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
import json
from .models import createOU
from .serializers import *
import boto3
import logging
from botocore.exceptions import ClientError
import requests


logger = logging.getLogger('django')

client = boto3.client('organizations')

@api_view(['POST'])
def create_orgunit(request):
  # event = request.data
  # print(event)
  # return JsonResponse("your data is: "+event+"kg", safe=False)
    serializer = createOUSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      x = serializer.data.get("name")
      y = serializer.data.get("ParentId")

      # Create_OU_response = client.create_organizational_unit(
      #   ParentId= y,
      #   Name=x
      # )
      logger.info('%s is your ou name',x)
      # print(x)
      logger.info('hello satya123')
      # return JsonResponse(x, safe=False)
      return HttpResponse(x+ ' is your ou name',status=200)

@api_view(['GET'])
def list_organizational_units(request):
  logger.info('Listing the Organizational Units for the Respective Parent')

  # serializer = listOUSerializer(data=request.data)
  # if serializer.is_valid():
  #   serializer.save()
  stream = BytesIO(request.body)
  data = JSONParser().parse(stream)
  serializer = listOUSerializer(data=data)
  print(serializer.is_valid())
  OU_parentId_list = serializer.data.get("ParentId")
  # else:
  #   return HttpResponse("The input is not serialized", status = 200)
  # print(serializer)
  # OU_parentId_list = serializer.data.get("ParentId")

  # OU_parentId_list = request.data['ParentId']
  print(OU_parentId_list)
  OUnames_list = []
  OUId_list = []
  for x in OU_parentId_list:
    try:
      list_OU_response = client.list_organizational_units_for_parent(
        ParentId=x,
      )
      NameofOU = list_OU_response["OrganizationalUnits"]
      for y in NameofOU:
        for x in y.keys():
          for a in y.keys():
            Names = y["Name"]
            OUnames_list.append(Names)
            Ids = y["Id"]
            OUId_list.append(Ids)
            break
          break
    except ClientError as e:
      logger.exception('Client Error!! %s',e)
      raise e

  OUdict = {OUnames_list[i]: OUId_list[i] for i in range(len(OUnames_list))}
  OU_json = json.dumps(OUdict, indent=4)

  logger.info('The Organizational Units for the Respective Parent are : %s',OU_json)
  # return JsonResponse('Organizational units '+OU_parentId_list, safe=False)
  return HttpResponse('Organizational units '+OU_parentId_list, status =200)