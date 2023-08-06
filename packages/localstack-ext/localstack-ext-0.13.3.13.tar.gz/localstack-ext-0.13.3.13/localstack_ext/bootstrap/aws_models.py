from localstack.utils.aws import aws_models
Teato=super
TeatK=None
Teatq=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  Teato(LambdaLayer,self).__init__(arn)
  self.cwd=TeatK
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.Teatq.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,Teatq,env=TeatK):
  Teato(RDSDatabase,self).__init__(Teatq,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,Teatq,env=TeatK):
  Teato(RDSCluster,self).__init__(Teatq,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,Teatq,env=TeatK):
  Teato(AppSyncAPI,self).__init__(Teatq,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,Teatq,env=TeatK):
  Teato(AmplifyApp,self).__init__(Teatq,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,Teatq,env=TeatK):
  Teato(ElastiCacheCluster,self).__init__(Teatq,env=env)
class TransferServer(BaseComponent):
 def __init__(self,Teatq,env=TeatK):
  Teato(TransferServer,self).__init__(Teatq,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,Teatq,env=TeatK):
  Teato(CloudFrontDistribution,self).__init__(Teatq,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,Teatq,env=TeatK):
  Teato(CodeCommitRepository,self).__init__(Teatq,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
