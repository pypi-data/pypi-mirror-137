from datetime import datetime
yxKAU=str
yxKAi=int
yxKAq=super
yxKAI=False
yxKAT=isinstance
yxKAc=hash
yxKAD=bool
yxKAJ=True
yxKAL=list
yxKAt=map
yxKAB=None
from enum import Enum
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
from localstack_ext.bootstrap.state_utils import API_STATES_DIR,DYNAMODB_DIR,KINESIS_DIR
class CPVCSObj:
 def __init__(self,hash_ref:yxKAU):
  self.hash_ref:yxKAU=hash_ref
class Serialization(Enum):
 MAIN=API_STATES_DIR
 DDB=DYNAMODB_DIR
 KINESIS=KINESIS_DIR
 serializer_root_lookup={yxKAU(MAIN):API_STATES_DIR,yxKAU(DDB):DYNAMODB_DIR,yxKAU(KINESIS):KINESIS_DIR}
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:yxKAU,rel_path:yxKAU,file_name:yxKAU,size:yxKAi,service:yxKAU,region:yxKAU,serialization:Serialization):
  yxKAq(StateFileRef,self).__init__(hash_ref)
  self.rel_path:yxKAU=rel_path
  self.file_name:yxKAU=file_name
  self.size:yxKAi=size
  self.service:yxKAU=service
  self.region:yxKAU=region
  self.serialization:Serialization=serialization
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,hash_ref=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path,serialization=self.serialization)
 def __eq__(self,other):
  if not other:
   return yxKAI
  if not yxKAT(other,StateFileRef):
   return yxKAI
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return yxKAc((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other)->yxKAD:
  if not other:
   return yxKAI
  if not yxKAT(other,StateFileRef):
   return yxKAI
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others)->yxKAD:
  for other in others:
   if self.congruent(other):
    return yxKAJ
  return yxKAI
 def metadata(self)->yxKAU:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:yxKAU,state_files:Set[StateFileRef],parent_ptr:yxKAU):
  yxKAq(CPVCSNode,self).__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:yxKAU=parent_ptr
 def state_files_info(self)->yxKAU:
  return "\n".join(yxKAL(yxKAt(lambda state_file:yxKAU(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:yxKAU,head_ptr:yxKAU,message:yxKAU,timestamp:yxKAU=yxKAU(datetime.now().timestamp()),delta_log_ptr:yxKAU=yxKAB):
  self.tail_ptr:yxKAU=tail_ptr
  self.head_ptr:yxKAU=head_ptr
  self.message:yxKAU=message
  self.timestamp:yxKAU=timestamp
  self.delta_log_ptr:yxKAU=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:yxKAU,to_node:yxKAU)->yxKAU:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:yxKAU,state_files:Set[StateFileRef],parent_ptr:yxKAU,creator:yxKAU,rid:yxKAU,revision_number:yxKAi,assoc_commit:Commit=yxKAB):
  yxKAq(Revision,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator:yxKAU=creator
  self.rid:yxKAU=rid
  self.revision_number:yxKAi=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(yxKAt(lambda state_file:yxKAU(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:yxKAU,state_files:Set[StateFileRef],parent_ptr:yxKAU,creator:yxKAU,comment:yxKAU,active_revision_ptr:yxKAU,outgoing_revision_ptrs:Set[yxKAU],incoming_revision_ptr:yxKAU,version_number:yxKAi):
  yxKAq(Version,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(yxKAt(lambda stat_file:yxKAU(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
