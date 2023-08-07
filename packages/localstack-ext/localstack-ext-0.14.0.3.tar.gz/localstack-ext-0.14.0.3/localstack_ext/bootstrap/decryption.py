import inspect
aqHmW=bytes
aqHmu=None
aqHmn=isinstance
aqHmD=list
aqHmz=getattr
aqHmt=open
aqHmb=property
aqHmh=Exception
aqHmV=setattr
aqHmy=True
import os.path
import sys
import traceback
from importlib.abc import MetaPathFinder,SourceLoader
from importlib.util import spec_from_file_location
import pyaes
class DecryptionHandler:
 decryption_key:aqHmW
 def __init__(self,decryption_key:aqHmW):
  self.decryption_key=decryption_key
 def decrypt(self,content)->aqHmW:
  cipher=pyaes.AESModeOfOperationCBC(self.decryption_key,iv="\0"*16)
  decrypter=pyaes.Decrypter(cipher)
  decrypted=decrypter.feed(content)
  decrypted+=decrypter.feed()
  decrypted=decrypted.partition(b"\0")[0]
  return decrypted
class EncryptedFileFinder(MetaPathFinder):
 decryption_handler:DecryptionHandler
 def __init__(self,decryption_handler:DecryptionHandler):
  self.decryption_handler=decryption_handler
 def find_spec(self,fullname,path,target=aqHmu):
  if path and not aqHmn(path,aqHmD):
   path=aqHmD(aqHmz(path,"_path",[]))
  if not path:
   return aqHmu
  name=fullname.split(".")[-1]
  file_path=os.path.join(path[0],name+".py")
  enc=file_path+".enc"
  if not os.path.isfile(enc):
   return aqHmu
  if os.path.isfile(file_path):
   return aqHmu
  return spec_from_file_location(fullname,enc,loader=DecryptingLoader(enc,self.decryption_handler))
class DecryptingLoader(SourceLoader):
 decryption_handler:DecryptionHandler
 def __init__(self,encrypted_file,decryption_handler:DecryptionHandler):
  self.encrypted_file=encrypted_file
  self.decryption_handler=decryption_handler
 def get_filename(self,fullname):
  return self.encrypted_file
 def get_data(self,filename):
  with aqHmt(filename,"rb")as f:
   data=f.read()
  data=self.decryption_handler.decrypt(data)
  return data
def init_source_decryption(decryption_handler:DecryptionHandler):
 sys.meta_path.insert(0,EncryptedFileFinder(decryption_handler))
 patch_traceback_lines()
 patch_inspect_findsource()
def patch_traceback_lines():
 if aqHmz(traceback.FrameSummary,"_ls_patch_applied",aqHmu):
  return
 @aqHmb
 def line(self):
  try:
   return line_orig.fget(self)
  except aqHmh:
   self._line=""
   return self._line
 line_orig=traceback.FrameSummary.line
 aqHmV(traceback.FrameSummary,"line",line)
 traceback.FrameSummary._ls_patch_applied=aqHmy
def patch_inspect_findsource():
 if aqHmz(inspect,"_ls_patch_applied",aqHmu):
  return
 def findsource(*args,**kwargs):
  try:
   return findsource_orig(*args,**kwargs)
  except aqHmh:
   return[],0
 findsource_orig=inspect.findsource
 inspect.findsource=findsource
 inspect._ls_patch_applied=aqHmy
# Created by pyminifier (https://github.com/liftoff/pyminifier)
