from datetime import datetime
UBoFw=str
UBoFs=int
UBoFd=super
UBoFN=False
UBoFH=isinstance
UBoFl=hash
UBoFA=bool
UBoFq=True
UBoFj=list
UBoFx=map
UBoFP=None
from enum import Enum
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
from localstack_ext.bootstrap.state_utils import API_STATES_DIR,DYNAMODB_DIR,KINESIS_DIR
class CPVCSObj:
 def __init__(self,hash_ref:UBoFw):
  self.hash_ref:UBoFw=hash_ref
class Serialization(Enum):
 MAIN=API_STATES_DIR
 DDB=DYNAMODB_DIR
 KINESIS=KINESIS_DIR
 serializer_root_lookup={UBoFw(MAIN):API_STATES_DIR,UBoFw(DDB):DYNAMODB_DIR,UBoFw(KINESIS):KINESIS_DIR}
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:UBoFw,rel_path:UBoFw,file_name:UBoFw,size:UBoFs,service:UBoFw,region:UBoFw,serialization:Serialization):
  UBoFd(StateFileRef,self).__init__(hash_ref)
  self.rel_path:UBoFw=rel_path
  self.file_name:UBoFw=file_name
  self.size:UBoFs=size
  self.service:UBoFw=service
  self.region:UBoFw=region
  self.serialization:Serialization=serialization
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,hash_ref=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path,serialization=self.serialization)
 def __eq__(self,other):
  if not other:
   return UBoFN
  if not UBoFH(other,StateFileRef):
   return UBoFN
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return UBoFl((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other)->UBoFA:
  if not other:
   return UBoFN
  if not UBoFH(other,StateFileRef):
   return UBoFN
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others)->UBoFA:
  for other in others:
   if self.congruent(other):
    return UBoFq
  return UBoFN
 def metadata(self)->UBoFw:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:UBoFw,state_files:Set[StateFileRef],parent_ptr:UBoFw):
  UBoFd(CPVCSNode,self).__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:UBoFw=parent_ptr
 def state_files_info(self)->UBoFw:
  return "\n".join(UBoFj(UBoFx(lambda state_file:UBoFw(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:UBoFw,head_ptr:UBoFw,message:UBoFw,timestamp:UBoFw=UBoFw(datetime.now().timestamp()),delta_log_ptr:UBoFw=UBoFP):
  self.tail_ptr:UBoFw=tail_ptr
  self.head_ptr:UBoFw=head_ptr
  self.message:UBoFw=message
  self.timestamp:UBoFw=timestamp
  self.delta_log_ptr:UBoFw=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:UBoFw,to_node:UBoFw)->UBoFw:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:UBoFw,state_files:Set[StateFileRef],parent_ptr:UBoFw,creator:UBoFw,rid:UBoFw,revision_number:UBoFs,assoc_commit:Commit=UBoFP):
  UBoFd(Revision,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator:UBoFw=creator
  self.rid:UBoFw=rid
  self.revision_number:UBoFs=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(UBoFx(lambda state_file:UBoFw(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:UBoFw,state_files:Set[StateFileRef],parent_ptr:UBoFw,creator:UBoFw,comment:UBoFw,active_revision_ptr:UBoFw,outgoing_revision_ptrs:Set[UBoFw],incoming_revision_ptr:UBoFw,version_number:UBoFs):
  UBoFd(Version,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(UBoFx(lambda stat_file:UBoFw(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
