import getpass
VDfRq=object
VDfRm=staticmethod
VDfRW=False
VDfRX=Exception
VDfRz=None
VDfRI=input
VDfRF=list
import json
import logging
import os
import sys
from localstack.config import dirs
from localstack.constants import API_ENDPOINT
from localstack.utils.common import FileMappedDocument,call_safe,safe_requests,to_str
LOG=logging.getLogger(__name__)
AUTH_CACHE_FILE="auth.json"
class AuthProvider(VDfRq):
 @VDfRm
 def name():
  raise
 def get_or_create_token(self,username,password,headers):
  pass
 def get_user_for_token(self,token):
  pass
 @VDfRm
 def providers():
  return{c.name():c for c in AuthProvider.__subclasses__()}
 @VDfRm
 def get(provider,raise_error=VDfRW):
  provider_class=AuthProvider.providers().get(provider)
  if not provider_class:
   msg='Unable to find auth provider class "%s"'%provider
   LOG.warning(msg)
   if raise_error:
    raise VDfRX(msg)
   return VDfRz
  return provider_class()
class AuthProviderInternal(AuthProvider):
 @VDfRm
 def name():
  return "internal"
 def get_or_create_token(self,username,password,headers):
  data={"username":username,"password":password}
  response=safe_requests.post("%s/user/signin"%API_ENDPOINT,json.dumps(data),headers=headers)
  if response.status_code>=400:
   return
  try:
   result=json.loads(to_str(response.content or "{}"))
   return result["token"]
  except VDfRX:
   pass
 def read_credentials(self,username):
  print("Please provide your login credentials below")
  if not username:
   sys.stdout.write("Username: ")
   sys.stdout.flush()
   username=VDfRI()
  password=getpass.getpass()
  return username,password,{}
 def get_user_for_token(self,token):
  raise VDfRX("Not implemented")
def get_auth_cache()->FileMappedDocument:
 return FileMappedDocument(os.path.join(dirs.cache,AUTH_CACHE_FILE),mode=0o600)
def login(provider,username=VDfRz):
 auth_provider=AuthProvider.get(provider)
 if not auth_provider:
  providers=VDfRF(AuthProvider.providers().keys())
  raise VDfRX('Unknown provider "%s", should be one of %s'%(provider,providers))
 username,password,headers=auth_provider.read_credentials(username)
 print("Verifying credentials ... (this may take a few moments)")
 token=auth_provider.get_or_create_token(username,password,headers)
 if not token:
  raise VDfRX("Unable to verify login credentials - please try again")
 cache=get_auth_cache()
 cache.update({"provider":provider,"username":username,"token":token})
 call_safe(cache.save,exception_message="error saving authentication information")
def logout():
 cache=get_auth_cache()
 cache.clear()
 cache.save()
def json_loads(s):
 return json.loads(to_str(s))
# Created by pyminifier (https://github.com/liftoff/pyminifier)
