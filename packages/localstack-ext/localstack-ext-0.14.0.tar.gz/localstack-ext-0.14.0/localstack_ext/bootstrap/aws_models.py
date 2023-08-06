from localstack.utils.aws import aws_models
vKEmi=super
vKEmG=None
vKEmo=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  vKEmi(LambdaLayer,self).__init__(arn)
  self.cwd=vKEmG
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.vKEmo.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,vKEmo,env=vKEmG):
  vKEmi(RDSDatabase,self).__init__(vKEmo,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,vKEmo,env=vKEmG):
  vKEmi(RDSCluster,self).__init__(vKEmo,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,vKEmo,env=vKEmG):
  vKEmi(AppSyncAPI,self).__init__(vKEmo,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,vKEmo,env=vKEmG):
  vKEmi(AmplifyApp,self).__init__(vKEmo,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,vKEmo,env=vKEmG):
  vKEmi(ElastiCacheCluster,self).__init__(vKEmo,env=env)
class TransferServer(BaseComponent):
 def __init__(self,vKEmo,env=vKEmG):
  vKEmi(TransferServer,self).__init__(vKEmo,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,vKEmo,env=vKEmG):
  vKEmi(CloudFrontDistribution,self).__init__(vKEmo,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,vKEmo,env=vKEmG):
  vKEmi(CodeCommitRepository,self).__init__(vKEmo,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
