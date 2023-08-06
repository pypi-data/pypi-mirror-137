from pspring import ConfigurationProvider, Configuration
import logging,json
import yaml
import os
import boto3
from datetime import datetime
from threading import Thread

logger = logging.getLogger(__name__)
config = Configuration.getConfig(__name__)

class S3ConfigProvider(ConfigurationProvider):
    def __init__(self,**kargs):
        self.bucketId = kargs.get("bucketId") or config.getProperty("bucketId")
        self.objectKey = kargs.get("objectKey") or config.getProperty("objectKey")
        self.region = kargs.get("region") or config.getProperty("region")
        self.subscriptions = []
        self.config={}
        self.refresh()
        self.lastUpdated = int(datetime.now().timestamp())
        self.timeout = config.getProperty("timeout") or config.getProperty("PSPRING_AWS_S3_CONFIG_TIMEOUT") or config.getProperty("PSPRING_CONFIG_TIMEOUT")

    def checkForRefresh(self):
        lastUpdatedSeconds = int(datetime.now().timestamp()) - self.lastUpdated
        if(self.timeout != None and lastUpdatedSeconds > int(self.timeout)):
            logger.info({
                "event": "trace",
                "message": "Auto refreshing S3 config.",
                "data": {
                    "bucketId": self.bucketId,
                    "objectKey": self.objectKey,
                    "region": self.region,
                    "refreshTimeout": self.timeout
                }
            })
            self.lastUpdated = int(datetime.now().timestamp())
            Thread(target=self.refresh).start()

    def getProperty(self,propertyName):
        self.checkForRefresh()
        # Check for json based keys
        config = self.config
        propertyNames = propertyName.split(".")
        for propertyNameItem in propertyNames:
            if config != None:
                config = config.get(propertyNameItem)

        if config != None:
            return config

        # return default way of property access
        return self.config.get(propertyName)

    def refresh(self):
        client = boto3.client("s3",region_name=self.region)
        file = client.get_object(Bucket=self.bucketId,Key=self.objectKey)
        filecontent = file.get("Body").read().decode("utf-8")
        try:
            extn = os.path.splitext(self.objectKey)[1]

            if extn and extn == '.json':
                self.config = json.loads(str(filecontent))
                logger.info({
                    "event": "trace",
                    "message": "Loaded S3 JSON config.",
                    "data": {
                        "bucketId": self.bucketId,
                        "objectKey": self.objectKey,
                        "region": self.region,
                        "config": self.config
                    }
                })

            elif extn and extn in ['.yml', '.yaml']:
                self.config = yaml.safe_load(filecontent)

                logger.info({
                    "event": "trace",
                    "message": "Loaded S3 YAML config.",
                    "data": {
                        "bucketId": self.bucketId,
                        "objectKey": self.objectKey,
                        "region": self.region,
                        "config": self.config
                    }
                })
            else:
                logger.error({
                    "event": "error",
                    "message": f'File type {extn} not supported.',
                    "data": {
                        "bucketId": self.bucketId,
                        "objectKey": self.objectKey,
                        "region": self.region
                    }
                })
                raise Exception('File type {} not supported.'.format(extn))

            self.publish()
        except Exception as er:
            logger.warning({
                "event": "warning",
                "message": f"Received content from s3 was not json {er}",
                "data": {
                    "bucketId": self.bucketId,
                    "objectKey": self.objectKey,
                    "region": self.region
                }
            })

        logger.info({
            "event": "trace",
            "message": "Refreshed S3 config.",
            "data": {
                "bucketId": self.bucketId,
                "objectKey": self.objectKey,
                "region": self.region
            }
        })

    def subscribe(self,callback):
        self.subscriptions.append(callback)

    def publish(self):
        for subscription in self.subscriptions:
            subscription()