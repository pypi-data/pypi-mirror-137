import json
import logging
import os
import time
import unittest

import boto3
from moto import mock_secretsmanager

logging.basicConfig(level=logging.INFO)

from pspringaws.secretsmngrconfigprovider import SecretsMgrConfigProvider

os.environ["PSPRING_CONFIG_TIMEOUT"] = "2"


@mock_secretsmanager
class TestSecretsMgrConfigProvider(unittest.TestCase):

    def setUp(self) -> None:
        self.client = boto3.client('secretsmanager')
        self.client.create_secret(
            Name='TestSecrets',
            SecretString='{"defaultKey": "defaultValue"}'
        )

    def update_secrets(self, key_values: dict):
        self.client.put_secret_value(
            SecretId='TestSecrets',
            SecretString=json.dumps(key_values)
        )

    def test_config(self):
        """Test secrets manager config success"""
        self.update_secrets({"testKey": "testValue"})

        conf = SecretsMgrConfigProvider(secretId="TestSecrets", region="us-east-1")
        value = conf.getProperty("testKey")

        self.assertEqual(value, "testValue")

    def test_background_config_refresh_after_timeout(self):
        """ Test secrets manager config refreshed in background and latest value pulled"""
        # update config
        self.update_secrets({"testKey": "testValue"})

        conf = SecretsMgrConfigProvider(secretId="TestSecrets", region="us-east-1")

        # check old value
        self.assertEqual(conf.getProperty("testKey"), "testValue")

        # update new config
        self.update_secrets({"testKey": "testValueNew"})

        # Wait till timeout
        time.sleep(3)
        conf.getProperty("testKey")
        # Wait till refresh thread completes
        time.sleep(1)
        # fetch new config
        value_2 = conf.getProperty("testKey")
        # validate
        self.assertEqual(value_2, "testValueNew")
