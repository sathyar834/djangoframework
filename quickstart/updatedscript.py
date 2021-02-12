from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
import json
from .models import *
from .serializers import *
import boto3
import time
from botocore.exceptions import ClientError
import re
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
  return HttpResponse('Root Id is '+rootId, status = 200)

@api_view(['POST'])
def create_organizational_units(request):
  logger.info('Create Organizational Units')

  serializer = createOUSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
    list_of_ParentId = serializer.data.get("ParentId")
    list_of_OUNames = serializer.data.get("OUname")
  else:
    return HttpResponse("The input is not serialized")

  try:
    Create_OU_response = client.create_organizational_unit(
    ParentId= list_of_ParentId,
    Name=list_of_OUNames
    )
  except ClientError as e:
    logger.exception('Client Error!! %s',e)
    raise e
  logger.info('Organizational Units Created Succesfully')
  return HttpResponse('Organizational Units Created Succesfully')

@api_view(['GET'])
def list_organizational_units(request):
  logger.info('Listing the Organizational Units for the Respective Parent')

  serializer = listOUSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
    OU_parentId_list = serializer.data.get("ParentIdlistou")
  else:
    return HttpResponse("The input is not serialized", status = 200)

  OUnames_list = []
  OUId_list = []

  try:
    list_OU_response = client.list_organizational_units_for_parent(
      ParentId=OU_parentId_list,
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

  return HttpResponse(OU_json)

@api_view(['GET'])
def list_accounts(request):
  logger.info('Listing all the Accounts')
  listresponse = client.list_accounts(
  )

  listmoreresponse = client.list_accounts(
    NextToken=listresponse["NextToken"]
  )

  AccountName = listresponse['Accounts']
  AccountNamemore = listmoreresponse['Accounts']

  Namelist =[]
  Idslist =[]
  for y in AccountName:
    for x in y.keys():
      for a in y.keys():
        Names = y["Name"]
        Namelist.append(Names)
        Ids = y["Id"]
        Idslist.append(Ids)
        break
      break

  Namelistmore =[]
  Idslistmore =[]
  for y in AccountNamemore:
    for x in y.keys():
      for a in y.keys():
        Names = y["Name"]
        Namelistmore.append(Names)
        Ids = y["Id"]
        Idslistmore.append(Ids)
        break
      break

  res = {Namelist[i]: Idslist[i] for i in range(len(Namelist))}

  resmore = {Namelistmore[i]: Idslistmore[i] for i in range(len(Namelistmore))}

  finaldict = dict(list(res.items()) + list(resmore.items()))
  accounts_json = json.dumps(finaldict, indent=4)
  logger.info('List of Accounts : %s',accounts_json)
  return HttpResponse('List of Accounts ' +accounts_json)

@api_view(['GET'])
def list_existing_email(request):
  logger.info('Listing all the existing Emails from AWS Account')

  listresponse = client.list_accounts(
  )

  listmoreresponse = client.list_accounts(
    NextToken=listresponse["NextToken"]
  )

  AccountEmail = listresponse['Accounts']
  AccountEmailmore = listmoreresponse['Accounts']

  Emaillist =[]
  for y in AccountEmail:
    for x in y.keys():
      for a in y.keys():
        Email = y["Email"]
        Emaillist.append(Email)
        break
      break

  Emaillistmore =[]
  for y in AccountEmailmore:
    for x in y.keys():
      for a in y.keys():
        Email = y["Email"]
        Emaillistmore.append(Email)
        break
      break

  final_email_list = Emaillist + Emaillistmore
  email_json = json.dumps(final_email_list, indent=4)
  logger.info('List of Emails : %s',email_json)
  return HttpResponse('The Available emails are ' +email_json)

@api_view(['POST'])
def create_account(request):
  logger.info('Creating an account')

  serializer = createaccountSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
    list_of_Emails = serializer.data.get("Email")
    list_of_Names = serializer.data.get("Name")
  else:
    return HttpResponse("The input is not serialized")

  listresponse = client.list_accounts(
  )

  listmoreresponse = client.list_accounts(
    NextToken=listresponse["NextToken"]
  )

  AccountEmail = listresponse['Accounts']
  AccountEmailmore = listmoreresponse['Accounts']

  Emaillist =[]
  for y in AccountEmail:
    for x in y.keys():
      for a in y.keys():
        Email = y["Email"]
        Emaillist.append(Email)
        break
      break

  Emaillistmore =[]
  for y in AccountEmailmore:
    for x in y.keys():
      for a in y.keys():
        Email = y["Email"]
        Emaillistmore.append(Email)
        break
      break

  Existing_emails = Emaillist + Emaillistmore

  for awsmail in Existing_emails:
    mailstatus = bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", list_of_Emails))
    if mailstatus == True:
      if list_of_Emails == awsmail:
        status = "Invalid email"
        logger.exception('The email already exist!')
        return HttpResponse("The email already exist!")
      else:
        status = "Valid email"
    else:
      logger.exception('The email format is Invalid!')
      return HttpResponse("The email format is Invalid!")
  try:
    if status == "Valid email":
      cresponse = client.create_account(
        Email= list_of_Emails,
        AccountName= list_of_Names,
        IamUserAccessToBilling='ALLOW'
      )
  except ClientError as e:
    logger.exception('Client Error!! %s',e)
    raise e
  logger.info('Account created successfully')
  return HttpResponse("Account created successfully")

@api_view(['POST'])
def move_account(request):
  logger.info('Moving Account from Source Parent to Destination Parent')

  serializer = moveaccountSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
    AccountId = serializer.data.get("AccountId")
    SourceId = serializer.data.get("SourceId")
    DestinationId = serializer.data.get("DestinationId")
  else:
    return("The input is not serialized")

  try:
    Moveresponse = client.move_account(
      AccountId= AccountId,
      SourceParentId= SourceId,
      DestinationParentId= DestinationId
    )
    logger.info('The Account %s moved to %s Successfully',AccountId,DestinationId)
  except ClientError as e:
    logger.exception('Client Error!! %s',e)
    raise e
  return HttpResponse('The Account ' +AccountId+ ' moved to ' +DestinationId+ ' Successfully')

@api_view(['POST'])
def create_scp_policy(request):
  logger.info('Create SCP policy')

  serializer = createscpSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
    Document_name = serializer.data.get("Documentname")
    SCP_Description = serializer.data.get("SCPDescription")
    SCP_Name = serializer.data.get("SCPName")
    logger.info(Document_name)
  else:
    return HttpResponse("The input is not serialized")
  logger.info('Create SCP policy serialized')
  if Document_name == "scp_policy":
    with open('./quickstart/scppolicy/scp_policy.json') as f:
      data = json.load(f)
      data1 = json.dumps(data, indent=4)
  elif Document_name == "duplicatepolicy":
    with open('./quickstart/scppolicy/duplicatepolicy.json') as f:
      data = json.load(f)
      data1 = json.dumps(data, indent=4)
  else:
    logger.exception('Invalid Document Name')
    return HttpResponse("Invalid Document Name")
  try:
    create_scp_response = client.create_policy(
    Content= str(data1),
    Description= SCP_Description,
    Name= SCP_Name,
    Type='SERVICE_CONTROL_POLICY',
    )
    logger.info('SCP Policy created Successfully')
    return HttpResponse("SCP Policy created Successfully")
  except ClientError as e:
    logger.exception('Client Error!! %s',e)
    raise e

@api_view(['GET'])
def list_scp_policy(request):
  logger.info('Listing all the SCP policies of the AWS account')
  list_scp_response = client.list_policies(
    Filter='SERVICE_CONTROL_POLICY',
  )
  listscpstatus = list_scp_response["Policies"]

  scpNamelist =[]
  scpIdslist =[]
  for y in listscpstatus:
    for x in y.keys():
      for a in y.keys():
        Names = y["Name"]
        scpNamelist.append(Names)
        Ids = y["Id"]
        scpIdslist.append(Ids)
        break
      break
  scpdict = {scpNamelist[i]: scpIdslist[i] for i in range(len(scpNamelist))}
  scp_json = json.dumps(scpdict, indent=4)
  logger.info('SCP Policies: %s',scp_json)
  return HttpResponse(scp_json)

@api_view(['POST'])
def attach_scp_policy(request):
  logger.info('Attaching SCP policy')

  serializer = attachscpSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
    SCP_PolicyId = serializer.data.get("SCPPolicyId")
    SCP_TargetId = serializer.data.get("AccountId")
  else:
    return HttpResponse("The input is not serialized")
  try:
    attachresponse = client.attach_policy(
      PolicyId= SCP_PolicyId,
      TargetId= SCP_TargetId
    )
    logger.info("Policy attached Successfully")
  except ClientError as e:
    logger.exception('Client Error!! %s',e)
    raise e
  return HttpResponse("Policy attached Successfully")


