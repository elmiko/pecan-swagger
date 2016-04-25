import unittest

from pecan_swagger import utils


class TestUtils(unittest.TestCase):
    def test_swagger_build(self):
        from .resources import example_app

        expected = {
            "swagger": "2.0",
            "info": {
                "version": "1.0",
                "title": "example_app"
                },
            "paths": {
                "/api": {
                    "GET": {}
                    },
                "/messages": {
                    "GET": {},
                    "POST": {}
                    },
                "/profile": {
                    "GET": {},
                    "POST": {}
                    },
                "/profile/image": {
                    "GET": {},
                    "POST": {}
                    },
                "/profile/stats": {
                    "GET": {}
                    }
                }
            }

        actual = utils.swagger_build('example_app', '1.0')
        self.assertDictEqual(expected, actual)
