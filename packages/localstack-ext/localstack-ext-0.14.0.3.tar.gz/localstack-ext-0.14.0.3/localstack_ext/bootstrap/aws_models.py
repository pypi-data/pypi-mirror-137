from localstack.utils.aws import aws_models
uirQK=super
uirQc=None
uirQa=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  uirQK(LambdaLayer,self).__init__(arn)
  self.cwd=uirQc
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.uirQa.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,uirQa,env=uirQc):
  uirQK(RDSDatabase,self).__init__(uirQa,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,uirQa,env=uirQc):
  uirQK(RDSCluster,self).__init__(uirQa,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,uirQa,env=uirQc):
  uirQK(AppSyncAPI,self).__init__(uirQa,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,uirQa,env=uirQc):
  uirQK(AmplifyApp,self).__init__(uirQa,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,uirQa,env=uirQc):
  uirQK(ElastiCacheCluster,self).__init__(uirQa,env=env)
class TransferServer(BaseComponent):
 def __init__(self,uirQa,env=uirQc):
  uirQK(TransferServer,self).__init__(uirQa,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,uirQa,env=uirQc):
  uirQK(CloudFrontDistribution,self).__init__(uirQa,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,uirQa,env=uirQc):
  uirQK(CodeCommitRepository,self).__init__(uirQa,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
