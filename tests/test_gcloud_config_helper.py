#!/usr/bin/env python

"""Tests for `gcloud_config_helper` package."""

import unittest

from gcloud_config_helper import GCloudCredentials
from datetime import datetime, timedelta
from copy import deepcopy


class MyGCloudCredentials(GCloudCredentials):
    def __init__(self, test_config: dict):
        self.test_config = test_config
        super(MyGCloudCredentials, self).__init__()

    def load(self):
        self.config = self.test_config


class TestGcloud_config_helper(unittest.TestCase):
    """Tests for `gcloud_config_helper` package."""

    def setUp(self):
        self.creds = MyGCloudCredentials(
            {
                "configuration": {
                    "active_configuration": "binx.io",
                    "properties": {
                        "core": {
                            "account": "mvanholsteijn@binx.io",
                            "disable_usage_reporting": "True",
                            "project": "sample-project",
                        }
                    },
                },
                "credential": {
                    "access_token": "secret-access-token",
                    "id_token": "secret-id-token",
                    "token_expiry": "2021-04-23T19:26:52Z",
                },
            }
        )

    def testCorrectName(self):
        self.assertEqual(self.creds.name, "binx.io")

    def testCorrectToken(self):
        self.assertEqual(self.creds.token, "secret-access-token")

    def testRefresh(self):
        c = MyGCloudCredentials(deepcopy(self.creds.config))
        self.assertEqual(c.token, c.access_token)
        self.assertEqual(c.expiry, c.token_expiry)
        self.assertTrue(c.expired)

        new_expiry = datetime.utcnow() + timedelta(hours=1)
        c.config["credential"]["token_expiry"] = f"{new_expiry.isoformat()}+00:00"
        c.config["credential"]["access_token"] = "new-secret"

        self.assertNotEqual(c.token, c.access_token)
        self.assertNotEqual(c.expiry, c.token_expiry)
        self.assertTrue(c.expired)
        c.refresh(None)

        self.assertEqual(c.token, c.access_token)
        self.assertEqual(c.expiry, c.token_expiry)
        self.assertFalse(c.expired)

    def testCorrectExpiry(self):
        self.assertEqual(
            self.creds.token_expiry, datetime.fromisoformat("2021-04-23T19:26:52")
        )
        self.assertTrue(self.creds.expired)

    def testCorrectProject(self):
        self.assertEqual(self.creds.project, "sample-project")

    def testCorrectConfigurationProperties(self):
        self.assertDictEqual(
            self.creds.properties,
            {
                "core": {
                    "account": "mvanholsteijn@binx.io",
                    "disable_usage_reporting": "True",
                    "project": "sample-project",
                }
            },
        )

    def testCorrectCredential(self):
        self.assertDictEqual(
            self.creds.credential,
            {
                "access_token": "secret-access-token",
                "id_token": "secret-id-token",
                "token_expiry": "2021-04-23T19:26:52Z",
            },
        )
