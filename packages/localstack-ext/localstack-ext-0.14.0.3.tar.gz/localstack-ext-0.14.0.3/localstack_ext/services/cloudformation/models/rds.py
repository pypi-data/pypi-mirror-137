from typing import Dict
OlJyW=staticmethod
OlJyQ=None
OlJyB=str
OlJyi=super
OlJyA=int
from localstack.services.cloudformation.service_models import GenericBaseModel
from localstack.utils.aws import aws_stack
from localstack.utils.common import short_uid
class RDSDBSubnetGroup(GenericBaseModel):
 @OlJyW
 def cloudformation_type():
  return "AWS::RDS::DBSubnetGroup"
 def get_physical_resource_id(self,attribute=OlJyQ,**kwargs):
  return self.props.get("DBSubnetGroupName")
 def fetch_state(self,stack_name,resources):
  client=aws_stack.connect_to_service("rds")
  group_name=self.resolve_refs_recursively(stack_name,self.props.get("DBSubnetGroupName"),resources)
  group=client.describe_db_subnet_groups()["DBSubnetGroups"]
  match=[i for i in group if i["DBSubnetGroupName"]==group_name]
  return(match or[OlJyQ])[0]
 @OlJyW
 def get_deploy_templates():
  return{"create":{"function":"create_db_subnet_group"},"delete":{"function":"delete_db_subnet_group","parameters":{"DBSubnetGroupName":"DBSubnetGroupName"}}}
class RDSDBCluster(GenericBaseModel):
 @OlJyW
 def cloudformation_type():
  return "AWS::RDS::DBCluster"
 @OlJyW
 def add_defaults(resource:Dict,stack_name:OlJyB):
  props=resource["Properties"]
  if not props.get("DBClusterIdentifier"):
   props["DBClusterIdentifier"]=f"dbc-{short_uid()}"
 def get_physical_resource_id(self,attribute=OlJyQ,**kwargs):
  return self.props.get("DBClusterIdentifier")
 def fetch_state(self,stack_name,resources):
  client=aws_stack.connect_to_service("rds")
  clusters=client.describe_db_clusters().get("DBClusters",[])
  cluster_id=self.resolve_refs_recursively(stack_name,self.props.get("DBClusterIdentifier"),resources)
  match=[c for c in clusters if c["DBClusterIdentifier"]==cluster_id]
  return(match or[OlJyQ])[0]
 def get_cfn_attribute(self,attribute):
  if attribute=="Endpoint.Address":
   return "localhost"
  props=self.props
  if attribute=="Endpoint.Port":
   return props.get("Port")or props.get("Endpoint",{}).get("Port")
  return OlJyi(RDSDBCluster,self).get_cfn_attribute(attribute)
 @OlJyW
 def get_deploy_templates():
  attrs=["AvailabilityZones","BackupRetentionPeriod","CharacterSetName","DatabaseName","DBClusterIdentifier","DBClusterParameterGroupName","VpcSecurityGroupIds","DBSubnetGroupName","Engine","EngineVersion","Port","MasterUsername","MasterUserPassword","OptionGroupName","PreferredBackupWindow","PreferredMaintenanceWindow","ReplicationSourceIdentifier","Tags","StorageEncrypted","KmsKeyId","PreSignedUrl","EnableIAMDatabaseAuthentication","BacktrackWindow","EnableCloudwatchLogsExports","EngineMode","ScalingConfiguration","DeletionProtection","GlobalClusterIdentifier","EnableHttpEndpoint","CopyTagsToSnapshot","Domain","DomainIAMRoleName","EnableGlobalWriteForwarding","SourceRegion"]
  def _params(params,**kwargs):
   params={k:v for k,v in params.items()if k in attrs}
   scaling_config=params.get("ScalingConfiguration")
   if scaling_config:
    if "MinCapacity" in scaling_config:
     scaling_config["MinCapacity"]=OlJyA(scaling_config["MinCapacity"])
    if "MaxCapacity" in scaling_config:
     scaling_config["MaxCapacity"]=OlJyA(scaling_config["MaxCapacity"])
   return params
  result={"create":{"function":"create_db_cluster","parameters":_params,"types":{"BackupRetentionPeriod":OlJyA,"Port":OlJyA}},"delete":{"function":"delete_db_cluster","parameters":["DBClusterIdentifier"]}}
  return result
class RDSDBParameterGroup(GenericBaseModel):
 @OlJyW
 def cloudformation_type():
  return "AWS::RDS::DBParameterGroup"
 def get_physical_resource_id(self,attribute=OlJyQ,**kwargs):
  return self.props.get("DBParameterGroupName")
 def fetch_state(self,stack_name,resources):
  client=aws_stack.connect_to_service("rds")
  props=self.props
  descr=self.resolve_refs_recursively(stack_name,props.get("Description"),resources)
  family=self.resolve_refs_recursively(stack_name,props.get("Family"),resources)
  groups=client.describe_db_parameter_groups()["DBParameterGroups"]
  match=[g for g in groups if g["Family"]==family and g["Description"]==descr]
  return(match or[OlJyQ])[0]
 @OlJyW
 def get_deploy_templates():
  return{"create":{"function":"create_db_parameter_group","parameters":{"DBParameterGroupName":"DBParameterGroupName","DBParameterGroupFamily":"Family","Description":"Description","Tags":"Tags"}},"delete":{"function":"delete_db_parameter_group","parameters":["DBParameterGroupName"]}}
class RDSDBInstance(GenericBaseModel):
 @OlJyW
 def cloudformation_type():
  return "AWS::RDS::DBInstance"
 @OlJyW
 def add_defaults(resource:Dict,stack_name:OlJyB):
  props=resource["Properties"]
  if not props.get("DBInstanceIdentifier"):
   props["DBInstanceIdentifier"]=f"db-{short_uid()}"
 def get_physical_resource_id(self,attribute=OlJyQ,**kwargs):
  return self.props.get("DBInstanceIdentifier")
 def get_cfn_attribute(self,attribute):
  if attribute=="Endpoint.Address":
   return "localhost"
  props=self.props
  if attribute=="Endpoint.Port":
   return props.get("Endpoint",{}).get("Port")or props.get("Port")
  return OlJyi(RDSDBInstance,self).get_cfn_attribute(attribute)
 def fetch_state(self,stack_name,resources):
  db_id=self.props.get("DBInstanceIdentifier")
  db_id=self.resolve_refs_recursively(stack_name,db_id,resources)
  client=aws_stack.connect_to_service("rds")
  instances=client.describe_db_instances()["DBInstances"]
  match=[i for i in instances if i["DBInstanceIdentifier"]==db_id]
  return(match or[OlJyQ])[0]
 @OlJyW
 def get_deploy_templates():
  attrs=["DBName","DBInstanceIdentifier","AllocatedStorage","DBInstanceClass","Engine","MasterUsername","MasterUserPassword","DBSecurityGroups","AvailabilityZone","DBSubnetGroupName","PreferredMaintenanceWindow","DBParameterGroupName","BackupRetentionPeriod","PreferredBackupWindow","Port","MultiAZ","EngineVersion","AutoMinorVersionUpgrade","LicenseModel","Iops","OptionGroupName","CharacterSetName","NcharCharacterSetName","PubliclyAccessible","Tags","DBClusterIdentifier","StorageType","TdeCredentialArn","TdeCredentialPassword","StorageEncrypted","KmsKeyId","Domain","CopyTagsToSnapshot","MonitoringInterval","MonitoringRoleArn","DomainIAMRoleName","PromotionTier","Timezone","EnableIAMDatabaseAuthentication","EnablePerformanceInsights","PerformanceInsightsKMSKeyId","PerformanceInsightsRetentionPeriod","EnableCloudwatchLogsExports","ProcessorFeatures","DeletionProtection","MaxAllocatedStorage","EnableCustomerOwnedIp"]
  return{"create":{"function":"create_db_instance","parameters":attrs+[{"VpcSecurityGroupIds":"VPCSecurityGroups"}],"types":{"AllocatedStorage":OlJyA,"Port":OlJyA}},"delete":{"function":"delete_db_instance","parameters":["DBInstanceIdentifier"]}}
# Created by pyminifier (https://github.com/liftoff/pyminifier)
