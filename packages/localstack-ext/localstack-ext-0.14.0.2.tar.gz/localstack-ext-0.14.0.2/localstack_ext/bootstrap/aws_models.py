from localstack.utils.aws import aws_models
VLAnO=super
VLAnR=None
VLAng=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  VLAnO(LambdaLayer,self).__init__(arn)
  self.cwd=VLAnR
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.VLAng.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,VLAng,env=VLAnR):
  VLAnO(RDSDatabase,self).__init__(VLAng,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,VLAng,env=VLAnR):
  VLAnO(RDSCluster,self).__init__(VLAng,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,VLAng,env=VLAnR):
  VLAnO(AppSyncAPI,self).__init__(VLAng,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,VLAng,env=VLAnR):
  VLAnO(AmplifyApp,self).__init__(VLAng,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,VLAng,env=VLAnR):
  VLAnO(ElastiCacheCluster,self).__init__(VLAng,env=env)
class TransferServer(BaseComponent):
 def __init__(self,VLAng,env=VLAnR):
  VLAnO(TransferServer,self).__init__(VLAng,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,VLAng,env=VLAnR):
  VLAnO(CloudFrontDistribution,self).__init__(VLAng,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,VLAng,env=VLAnR):
  VLAnO(CodeCommitRepository,self).__init__(VLAng,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
