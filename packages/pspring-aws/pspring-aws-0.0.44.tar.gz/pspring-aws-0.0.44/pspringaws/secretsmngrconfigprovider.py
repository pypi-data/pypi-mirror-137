from pspring import ConfigurationProvider, Configuration
from .secretsmngr import SecretsManager
import logging,json
from datetime import datetime
from threading import Thread

logger = logging.getLogger(__name__)
config = Configuration.getConfig(__name__)

class SecretsMgrConfigProvider(ConfigurationProvider):
    def __init__(self,**kargs):
        self.secretId = kargs.get("secretId") or config.getProperty("secretId")
        region = kargs.get("region") or config.getProperty("region")
        self.subscriptions = []
        self.mgr = SecretsManager(secretId=self.secretId,region=region)
        self.refresh()
        self.lastUpdated = int(datetime.now().timestamp())
        self.timeout = kargs.get("timeout") or config.getProperty("PSPRING_AWS_SM_CONFIG_TIMEOUT") or config.getProperty("PSPRING_CONFIG_TIMEOUT")

    def getProperty(self,propertyName):
        self.checkForRefresh()
        return self.secretValue.get(propertyName)

    def checkForRefresh(self):
        lastUpdatedSeconds = int(datetime.now().timestamp()) - self.lastUpdated
        if(self.timeout != None and lastUpdatedSeconds > int(self.timeout)):
            logger.info({
                "event": "trace",
                "message": "Auto refreshing SecretsManager config.",
                "data": {
                    "secretId": self.secretId,
                    "refreshTimeout": self.timeout
                }
            })
            self.lastUpdated = int(datetime.now().timestamp())
            Thread(target=self.refresh).start()

    def refresh(self):
        self.secretValue = self.mgr.getRefreshedSecretValue()
        self.publish()

        logger.info({
            "event": "trace",
            "message": "Refreshed SecretsManager config.",
            "data": {
                "secretId": self.secretId
            }
        })

    def subscribe(self,callback):
        self.subscriptions.append(callback)

    def publish(self):
        for subscription in self.subscriptions:
            subscription()