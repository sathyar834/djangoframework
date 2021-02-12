from django.db import models


# Create your models here.
class createOU(models.Model):
  ParentId = models.CharField(max_length=30)
  OUname =  models.CharField(max_length=30)

class listroot(models.Model):
  rootId = models.CharField(max_length=30)

class listOU(models.Model):
  ParentIdlistou = models.TextField(max_length=30)

class createaccount(models.Model):
  Email = models.CharField(max_length=30)
  Name = models.CharField(max_length=30)

class moveaccount(models.Model):
  AccountId = models.CharField(max_length=30)
  DestinationId = models.CharField(max_length=30)
  SourceId = models.CharField(max_length=30)

class createscp(models.Model):
  SCPDescription = models.CharField(max_length=30)
  SCPName = models.CharField(max_length=30)
  Documentname = models.CharField(max_length=30)

class attachscp(models.Model):
  SCPPolicyId = models.CharField(max_length=30)
  AccountId = models.CharField(max_length=30)
