import json


with open("prueba.json") as f:
    data = f.read()
d = json.loads(data)
for x in range(15):
    d["Resources"]["ApiGatewayStage"+str(x)]={'Type': 'AWS::ApiGateway::Stage',
                           'Properties': {'DeploymentId': {'Ref': 'ApiGatewayDeployment'},
                                          'Description': 'Lambda API Stage v'+str(x), 'RestApiId': {'Ref': 'ApiGatewayRestApi'}, 'StageName': 'v'+str(x)}}
with open("prueba.json", "w") as f:
    f.write(json.dumps(d))
