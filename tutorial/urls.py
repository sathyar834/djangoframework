"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from quickstart import updatedscript
from quickstart import views


urlpatterns = [
  url(r'^createou/$', updatedscript.create_organizational_units, name='Create OU'),
  url(r'^listroot/$', updatedscript.list_roots, name='List Roots'),
  url(r'^listou/$', updatedscript.list_organizational_units, name='List OU'),
  url(r'^listaccounts/$', updatedscript.list_accounts, name='List Accounts'),
  url(r'^listexistingemails/$', updatedscript.list_existing_email, name='List Existing Emailss'),
  url(r'^createaccount/$', updatedscript.create_account, name='Create Account'),
  url(r'^moveaccount/$', updatedscript.move_account, name='Move Account'),
  url(r'^createscp/$', updatedscript.create_scp_policy, name='Create SCP'),
  url(r'^listscp/$', updatedscript.list_scp_policy, name='List SCP'),
  url(r'^attachscp/$', updatedscript.attach_scp_policy, name='Attach SCP'),
  url(r'^org/$', views.create_orgunit, name='ORG SCP'),
  url(r'^listouview/$', views.list_organizational_units, name='List OU'),
]