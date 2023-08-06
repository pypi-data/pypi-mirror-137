import abc
eJwuq=str
eJwuH=None
eJwuF=staticmethod
eJwuB=set
eJwux=list
eJwub=map
eJwuv=int
eJwum=open
import logging
import os
from typing import Dict,Optional,Set
from localstack_ext.bootstrap.cpvcs.models import(Commit,CPVCSNode,CPVCSObj,Revision,StateFileRef,Version)
from localstack_ext.bootstrap.cpvcs.utils.common import config_context
LOG=logging.getLogger(__name__)
class CPVCSSerializer(abc.ABC):
 def __init__(self):
  pass
 @abc.abstractmethod
 def store_obj(self,cpvcs_obj:CPVCSObj)->eJwuq:
  pass
 @abc.abstractmethod
 def retrieve_obj(self,key:eJwuq,remote_path:eJwuq=eJwuH)->Optional[CPVCSObj]:
  pass
 @eJwuF
 def _deserialize_state_files(state_files_str:eJwuq)->Set[StateFileRef]:
  if not state_files_str:
   return eJwuB()
  state_files_attrs=state_files_str.split(";")
  state_files:Set[StateFileRef]=eJwuB()
  for state_file_attrs in state_files_attrs:
   instance_attrs=eJwux(eJwub(lambda x:x.split(":")[1],state_file_attrs.split(",")))
   state_files.add(StateFileRef(size=eJwuv(instance_attrs[0]),service=instance_attrs[1],region=instance_attrs[2],hash_ref=instance_attrs[3],file_name=instance_attrs[4],rel_path=instance_attrs[5],serialization=instance_attrs[6]))
  return state_files
class VersionSerializerTxt(CPVCSSerializer):
 def store_obj(self,cpvcs_obj:CPVCSNode)->eJwuq:
  with eJwum(os.path.join(config_context.get_ver_obj_store_path(),cpvcs_obj.hash_ref),"w")as fp:
   fp.write(eJwuq(cpvcs_obj))
  return cpvcs_obj.hash_ref
 def retrieve_obj(self,key:eJwuq,remote_path:eJwuq=eJwuH)->Optional[Version]:
  if remote_path:
   file_path=os.path.join(remote_path,key)
  else:
   file_path=os.path.join(config_context.get_ver_obj_store_path(),key)
  if not os.path.isfile(file_path):
   LOG.debug(f"No Version Obj file found in path {file_path}")
   return
  with eJwum(os.path.join(config_context.get_ver_obj_store_path(),key),"r")as fp:
   lines=eJwux(eJwub(lambda line:line.rstrip(),fp.readlines()))
   version_attrs=eJwux(eJwub(lambda line:line.split("=")[1],lines))
   state_files=self._deserialize_state_files(version_attrs[8])
   return Version(parent_ptr=version_attrs[0],hash_ref=version_attrs[1],creator=version_attrs[2],comment=version_attrs[3],version_number=eJwuv(version_attrs[4]),active_revision_ptr=version_attrs[5],outgoing_revision_ptrs=eJwuB(version_attrs[6].split(";")),incoming_revision_ptr=version_attrs[7],state_files=state_files)
class RevisionSerializerTxt(CPVCSSerializer):
 def store_obj(self,cpvcs_obj:Revision)->eJwuq:
  with eJwum(os.path.join(config_context.get_rev_obj_store_path(),cpvcs_obj.hash_ref),"w")as fp:
   fp.write(eJwuq(cpvcs_obj))
  return cpvcs_obj.hash_ref
 def retrieve_obj(self,key:eJwuq,remote_path:eJwuq=eJwuH)->Optional[Revision]:
  file_path=os.path.join(config_context.get_rev_obj_store_path(),key)
  if not os.path.isfile(file_path):
   LOG.debug(f"No Revision Obj file found in path {file_path}")
   return
  def _deserialize_commit(commit_str:eJwuq)->Commit:
   if not commit_str or commit_str=="None":
    return
   commit_attrs=eJwux(eJwub(lambda commit_attr:commit_attr.split(":")[1],commit_str.split(",")))
   return Commit(tail_ptr=commit_attrs[0],head_ptr=commit_attrs[1],message=commit_attrs[2],timestamp=commit_attrs[3],delta_log_ptr=commit_attrs[4])
  with eJwum(os.path.join(config_context.get_rev_obj_store_path(),key))as fp:
   lines=eJwux(eJwub(lambda line:line.rstrip(),fp.readlines()))
   revision_attrs=eJwux(eJwub(lambda line:line.split("=")[1],lines))
   state_files=self._deserialize_state_files(revision_attrs[5])
   return Revision(parent_ptr=revision_attrs[0],hash_ref=revision_attrs[1],creator=revision_attrs[2],rid=revision_attrs[3],revision_number=eJwuv(revision_attrs[4]),state_files=state_files,assoc_commit=_deserialize_commit(revision_attrs[6]))
version_serializer=VersionSerializerTxt()
revision_serializer=RevisionSerializerTxt()
txt_serializers:Dict[eJwuq,CPVCSSerializer]={"version":version_serializer,"revision":revision_serializer}
# Created by pyminifier (https://github.com/liftoff/pyminifier)
