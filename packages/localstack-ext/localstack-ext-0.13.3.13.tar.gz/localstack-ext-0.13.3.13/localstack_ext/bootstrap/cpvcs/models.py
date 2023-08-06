from datetime import datetime
YKAHL=str
YKAHl=int
YKAHy=super
YKAHg=False
YKAHz=isinstance
YKAHU=hash
YKAHn=bool
YKAHE=True
YKAHs=list
YKAHi=map
YKAHr=None
from enum import Enum
from typing import Set
from localstack_ext.bootstrap.cpvcs.constants import(COMMIT_TXT_LAYOUT,REV_TXT_LAYOUT,STATE_TXT_LAYOUT,STATE_TXT_METADATA,VER_TXT_LAYOUT)
from localstack_ext.bootstrap.state_utils import API_STATES_DIR,DYNAMODB_DIR,KINESIS_DIR
class CPVCSObj:
 def __init__(self,hash_ref:YKAHL):
  self.hash_ref:YKAHL=hash_ref
class Serialization(Enum):
 MAIN=API_STATES_DIR
 DDB=DYNAMODB_DIR
 KINESIS=KINESIS_DIR
 serializer_root_lookup={YKAHL(MAIN):API_STATES_DIR,YKAHL(DDB):DYNAMODB_DIR,YKAHL(KINESIS):KINESIS_DIR}
class StateFileRef(CPVCSObj):
 txt_layout=STATE_TXT_LAYOUT
 metadata_layout=STATE_TXT_METADATA
 def __init__(self,hash_ref:YKAHL,rel_path:YKAHL,file_name:YKAHL,size:YKAHl,service:YKAHL,region:YKAHL,serialization:Serialization):
  YKAHy(StateFileRef,self).__init__(hash_ref)
  self.rel_path:YKAHL=rel_path
  self.file_name:YKAHL=file_name
  self.size:YKAHl=size
  self.service:YKAHL=service
  self.region:YKAHL=region
  self.serialization:Serialization=serialization
 def __str__(self):
  return self.txt_layout.format(size=self.size,service=self.service,region=self.region,hash_ref=self.hash_ref,file_name=self.file_name,rel_path=self.rel_path,serialization=self.serialization)
 def __eq__(self,other):
  if not other:
   return YKAHg
  if not YKAHz(other,StateFileRef):
   return YKAHg
  return(self.hash_ref==other.hash_ref and self.region==other.region and self.service==self.service and self.file_name==other.file_name and self.size==other.size)
 def __hash__(self):
  return YKAHU((self.hash_ref,self.region,self.service,self.file_name,self.size))
 def congruent(self,other)->YKAHn:
  if not other:
   return YKAHg
  if not YKAHz(other,StateFileRef):
   return YKAHg
  return(self.region==other.region and self.service==other.service and self.file_name==other.file_name and self.rel_path==other.rel_path)
 def any_congruence(self,others)->YKAHn:
  for other in others:
   if self.congruent(other):
    return YKAHE
  return YKAHg
 def metadata(self)->YKAHL:
  return self.metadata_layout.format(size=self.size,service=self.service,region=self.region)
class CPVCSNode(CPVCSObj):
 def __init__(self,hash_ref:YKAHL,state_files:Set[StateFileRef],parent_ptr:YKAHL):
  YKAHy(CPVCSNode,self).__init__(hash_ref)
  self.state_files:Set[StateFileRef]=state_files
  self.parent_ptr:YKAHL=parent_ptr
 def state_files_info(self)->YKAHL:
  return "\n".join(YKAHs(YKAHi(lambda state_file:YKAHL(state_file),self.state_files)))
class Commit:
 txt_layout=COMMIT_TXT_LAYOUT
 def __init__(self,tail_ptr:YKAHL,head_ptr:YKAHL,message:YKAHL,timestamp:YKAHL=YKAHL(datetime.now().timestamp()),delta_log_ptr:YKAHL=YKAHr):
  self.tail_ptr:YKAHL=tail_ptr
  self.head_ptr:YKAHL=head_ptr
  self.message:YKAHL=message
  self.timestamp:YKAHL=timestamp
  self.delta_log_ptr:YKAHL=delta_log_ptr
 def __str__(self):
  return self.txt_layout.format(tail_ptr=self.tail_ptr,head_ptr=self.head_ptr,message=self.message,timestamp=self.timestamp,log_hash=self.delta_log_ptr)
 def info_str(self,from_node:YKAHL,to_node:YKAHL)->YKAHL:
  return f"from: {from_node}, to: {to_node}, message: {self.message}, time: {datetime.fromtimestamp(float(self.timestamp))}"
class Revision(CPVCSNode):
 txt_layout=REV_TXT_LAYOUT
 def __init__(self,hash_ref:YKAHL,state_files:Set[StateFileRef],parent_ptr:YKAHL,creator:YKAHL,rid:YKAHL,revision_number:YKAHl,assoc_commit:Commit=YKAHr):
  YKAHy(Revision,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator:YKAHL=creator
  self.rid:YKAHL=rid
  self.revision_number:YKAHl=revision_number
  self.assoc_commit=assoc_commit
 def __str__(self):
  return self.txt_layout.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,rid=self.rid,rev_no=self.revision_number,state_files=";".join(YKAHi(lambda state_file:YKAHL(state_file),self.state_files))if self.state_files else "",assoc_commit=self.assoc_commit)
class Version(CPVCSNode):
 txt_layout=VER_TXT_LAYOUT
 def __init__(self,hash_ref:YKAHL,state_files:Set[StateFileRef],parent_ptr:YKAHL,creator:YKAHL,comment:YKAHL,active_revision_ptr:YKAHL,outgoing_revision_ptrs:Set[YKAHL],incoming_revision_ptr:YKAHL,version_number:YKAHl):
  YKAHy(Version,self).__init__(hash_ref,state_files,parent_ptr)
  self.creator=creator
  self.comment=comment
  self.active_revision_ptr=active_revision_ptr
  self.outgoing_revision_ptrs=outgoing_revision_ptrs
  self.incoming_revision_ptr=incoming_revision_ptr
  self.version_number=version_number
 def __str__(self):
  return VER_TXT_LAYOUT.format(hash_ref=self.hash_ref,parent=self.parent_ptr,creator=self.creator,comment=self.comment,version_number=self.version_number,active_revision=self.active_revision_ptr,outgoing_revisions=";".join(self.outgoing_revision_ptrs),incoming_revision=self.incoming_revision_ptr,state_files=";".join(YKAHi(lambda stat_file:YKAHL(stat_file),self.state_files))if self.state_files else "")
 def info_str(self):
  return f"{self.version_number}, {self.creator}, {self.comment}"
# Created by pyminifier (https://github.com/liftoff/pyminifier)
