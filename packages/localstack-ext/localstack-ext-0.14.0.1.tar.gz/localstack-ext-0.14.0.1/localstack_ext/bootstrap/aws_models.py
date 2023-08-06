from localstack.utils.aws import aws_models
CiAub=super
CiAum=None
CiAuB=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  CiAub(LambdaLayer,self).__init__(arn)
  self.cwd=CiAum
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.CiAuB.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,CiAuB,env=CiAum):
  CiAub(RDSDatabase,self).__init__(CiAuB,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,CiAuB,env=CiAum):
  CiAub(RDSCluster,self).__init__(CiAuB,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,CiAuB,env=CiAum):
  CiAub(AppSyncAPI,self).__init__(CiAuB,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,CiAuB,env=CiAum):
  CiAub(AmplifyApp,self).__init__(CiAuB,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,CiAuB,env=CiAum):
  CiAub(ElastiCacheCluster,self).__init__(CiAuB,env=env)
class TransferServer(BaseComponent):
 def __init__(self,CiAuB,env=CiAum):
  CiAub(TransferServer,self).__init__(CiAuB,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,CiAuB,env=CiAum):
  CiAub(CloudFrontDistribution,self).__init__(CiAuB,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,CiAuB,env=CiAum):
  CiAub(CodeCommitRepository,self).__init__(CiAuB,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
