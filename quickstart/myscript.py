from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
import json
from .models import *
from .serializers import *
import boto3
import logging

logger = logging.getLogger('django')

client = boto3.client('organizations')

@api_view(['GET'])
def list_roots(request):
  global rootId
  logger.info('Listing the roots of the AWS account')

  rootId_response = client.list_roots(
  )
  rootId = rootId_response['Roots'][0]['Id']

  logger.info("RootId: %s",rootId)

  # serializer = listrootSerializer(rootId, many=True)
  return HttpResponse('Root Id is '+rootId, status = 200)




