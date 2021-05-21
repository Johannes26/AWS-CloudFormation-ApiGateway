import json
import calendar
import time


gmt = time.gmtime()
ts = calendar.timegm(gmt)

functionPermition="arn:aws:lambda:us-east-1:537846341098:function:lambda:mig"

with open("prueba.json") as f:
    data = f.read()
d = json.loads(data)

for x in range(15):
    apiDeployment="ApiGatewayDeployment"+ str(ts) + "v" + str(x)
    
    d["Resources"][apiDeployment]={
             "Type": "AWS::ApiGateway::Deployment",
             "DeletionPolicy": "Retain",
             "DependsOn": [
                "ApiGatewayMethod",
                "ConfigLambdaPermission"
             ],
             "Properties": {
                "Description": "Lambda API Deployment",
                "RestApiId": {
                   "Ref": "ApiGatewayRestApi"
                }
             }
        }
    d["Resources"]["ApiGatewayStage"+str(x)]["DependsOn"]= apiDeployment
    d["Resources"]["ApiGatewayStage"+str(x)]["Properties"]["DeploymentId"] = {
"Ref":apiDeployment}

d["Resources"]["ConfigLambdaPermission"]["Properties"]["FunctionName"]=functionPermition
d["Resources"]["ApiGatewayMethod"]["Properties"]["Integration"]["Uri"]["Fn::Sub"]="arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/"+functionPermition+"/invocations"
d["Description"]="AWS API Gateway with a migrations Lambda Integration"
d["Resources"]["ApiGatewayRestApi"]["Description"]="A Migration Lambda Integration in API Gateway"
    
with open("prueba.json", "w") as f:
    f.write(json.dumps(d))
