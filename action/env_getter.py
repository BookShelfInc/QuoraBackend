def getVariable(var):
    keys = {}
    keys = {'s3BucketPath': 'https://s3.amazonaws.com/quora-avatar-bucket/', 's3BucketName': 'quora-avatar-bucket', 'API_GATEWAY_IMAGE': 'https://xyhd3cbi24.execute-api.us-east-1.amazonaws.com/apiv1/avatar', 'RDS_HOST': 'quorainstancedb.cljzmclq5sf0.us-east-1.rds.amazonaws.com', 'RDS_NAME': 'quoraDB', 'RDS_PORT': '5432', 'RDS_PASSWORD': 'liverpool1892', 'RDS_USER': 'postgres'}
    with open('.env', 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.split('=')
            keys[line[0]] = line[1].replace('\n','')
    return (keys[var] if(var in keys.keys()) else None)