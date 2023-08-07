import logging
cpTfY=bool
cpTfx=hasattr
cpTfa=set
cpTfD=True
cpTfj=False
cpTfu=isinstance
cpTfI=dict
cpTfe=getattr
cpTfP=None
cpTfN=str
cpTfh=Exception
cpTfQ=open
import os
from typing import Any,Callable,List,OrderedDict,Set,Tuple
import dill
from localstack.utils.common import ObjectIdHashComparator
API_STATES_DIR="api_states"
KINESIS_DIR="kinesis"
DYNAMODB_DIR="dynamodb"
LOG=logging.getLogger(__name__)
def check_already_visited(obj,visited:Set)->Tuple[cpTfY,Set]:
 if cpTfx(obj,"__dict__"):
  visited=visited or cpTfa()
  wrapper=ObjectIdHashComparator(obj)
  if wrapper in visited:
   return cpTfD,visited
  visited.add(wrapper)
 return cpTfj,visited
def get_object_dict(obj):
 if cpTfu(obj,cpTfI):
  return obj
 obj_dict=cpTfe(obj,"__dict__",cpTfP)
 return obj_dict
def is_composite_type(obj):
 return cpTfu(obj,(cpTfI,OrderedDict))or cpTfx(obj,"__dict__")
def api_states_traverse(api_states_path:cpTfN,side_effect:Callable[...,cpTfP],mutables:List[Any]):
 for dir_name,_,file_list in os.walk(api_states_path):
  for file_name in file_list:
   try:
    subdirs=os.path.normpath(dir_name).split(os.sep)
    region=subdirs[-1]
    service_name=subdirs[-2]
    side_effect(dir_name=dir_name,fname=file_name,region=region,service_name=service_name,mutables=mutables)
   except cpTfh as e:
    msg=(f"Failed to apply {side_effect.__name__} for {file_name} in dir {dir_name}: {e}")
    LOG.warning(msg)
    if LOG.isEnabledFor(logging.DEBUG):
     LOG.exception(msg)
    continue
def load_persisted_object(state_file):
 if not os.path.isfile(state_file):
  return
 import dill
 with cpTfQ(state_file,"rb")as f:
  try:
   content=f.read()
   result=dill.loads(content)
   return result
  except cpTfh as e:
   LOG.debug("Unable to read pickled persistence file %s: %s",state_file,e)
def persist_object(obj,state_file):
 with cpTfQ(state_file,"wb")as f:
  result=f.write(dill.dumps(obj))
  return result
# Created by pyminifier (https://github.com/liftoff/pyminifier)
