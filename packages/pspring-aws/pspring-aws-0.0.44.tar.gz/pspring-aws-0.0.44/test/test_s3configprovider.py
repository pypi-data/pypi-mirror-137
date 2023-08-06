import json
import logging
import os
import time
import unittest

import boto3
from moto import mock_s3

logging.basicConfig(level=logging.INFO)

from pspringaws.s3configprovider import S3ConfigProvider

os.environ["PSPRING_CONFIG_TIMEOUT"] = "2"


@mock_s3
class TestS3ConfigProvider(unittest.TestCase):
    """
    Test S3ConfigProvider
    """
    def setUp(self) -> None:
        self.client = boto3.client('s3')
        self.client.create_bucket(Bucket='testbucket')

    def update_config(self, data: dict):
        """Update dict config to bucket"""
        self.client.put_object(
            Body=json.dumps(data),
            Bucket='testbucket',
            Key='config.json'
        )

    def test_config(self):
        """Test s3 config success"""
        self.update_config({"testKey": "testValue"})

        conf = S3ConfigProvider(bucketId="testbucket", objectKey="config.json")
        value = conf.getProperty("testKey")

        self.assertEqual(value, "testValue")

    def test_background_config_refresh_after_timeout(self):
        """ Test s3 config refreshed in background and latest value pulled"""
        # update config
        self.update_config({"testKey": "testValue"})

        conf = S3ConfigProvider(bucketId="testbucket", objectKey="config.json")

        # check old value
        self.assertEqual(conf.getProperty("testKey"), "testValue")

        # update new config
        self.update_config({"testKey": "testValueNew"})

        # Wait till timeout
        time.sleep(3)
        conf.getProperty("testKey")
        # Wait till refresh thread completes
        time.sleep(1)
        # fetch new config
        value_2 = conf.getProperty("testKey")
        # validate
        self.assertEqual(value_2, "testValueNew")
