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
            "produces": [],
            "consumes": [],
            "paths": {
                "/api": {
                    "get": {}
                    },
                "/messages": {
                    "get": {},
                    "post": {}
                    },
                "/profile": {
                    "get": {},
                    "post": {}
                    },
                "/profile/image": {
                    "get": {},
                    "post": {}
                    },
                "/profile/stats": {
                    "get": {}
                    }
                }
            }

        actual = utils.swagger_build('example_app', '1.0')
        self.assertDictEqual(expected, actual)

    def test_swagger_build_wsme(self):
        from .resources import example_wsme_app

        expected = \
            {
              "consumes": [],
              "info": {
                "title": "example_wsme_app",
                "version": "1.0"
              },
              "paths": {
                "/api": {
                  "get": {}
                },
                "/messages": {
                  "get": {},
                  "post": {}
                },
                "/profile": {
                  "get": {},
                  "post": {}
                },
                "/profile/image": {
                  "get": {},
                  "post": {}
                },
                "/profile/stats": {
                  "get": {}
                },
                "/wsmemessages": {
                  "get": {
                    "description": "",
                    "parameters": [],
                    "responses": {
                      200: {
                        "description": "",
                        "schema": {
                          "items": {
                            "items": {
                              "properties": {
                                "id": {
                                  "maxLength": 255,
                                  "minLength": 1,
                                  "type": "string"
                                },
                                "message": {
                                  "maxLength": 255,
                                  "minLength": 1,
                                  "type": "string"
                                },
                                "message_from": {
                                  "enum": [
                                    '1.OSOMATSU',
                                    '2.KARAMATSU',
                                    '3.CHOROMATSU',
                                    '4.ICHIMATSU',
                                    '5.JUSHIMATSU',
                                    '6.TODOMATSU'
                                  ],
                                  "type": "string"
                                },
                                "message_size": {
                                  "minimum": 1,
                                  "type": "integer"
                                }
                              }
                            },
                            "type": "object"
                          },
                          "type": "array"
                        }
                      }
                    }
                  },
                  "post": {
                    "description": "",
                    "parameters": [
                      {
                        "in": "query",
                        "name": "message",
                        "required": True,
                        "type": "string"
                      }
                    ],
                    "responses": {
                      201: {
                        "description": "",
                        "schema": {
                          "items": {
                            "properties": {
                              "id": {
                                "maxLength": 255,
                                "minLength": 1,
                                "type": "string"
                              },
                              "message": {
                                "maxLength": 255,
                                "minLength": 1,
                                "type": "string"
                              },
                              "message_from": {
                                "enum": [
                                    '1.OSOMATSU',
                                    '2.KARAMATSU',
                                    '3.CHOROMATSU',
                                    '4.ICHIMATSU',
                                    '5.JUSHIMATSU',
                                    '6.TODOMATSU'
                                ],
                                "type": "string"
                              },
                              "message_size": {
                                "minimum": 1,
                                "type": "integer"
                              }
                            }
                          },
                          "type": "object"
                        }
                      }
                    }
                  }
                },
                "/wsmemessages/<specifier>": {
                  "delete": {
                    "description": "",
                    "parameters": [
                      {
                        "in": "query",
                        "name": "id",
                        "required": True,
                        "type": "string"
                      }
                    ],
                    "responses": {
                      204: {
                        "description": ""
                      }
                    }
                  },
                  "get": {
                    "description": "",
                    "parameters": [
                      {
                        "in": "query",
                        "name": "id",
                        "required": True,
                        "type": "string"
                      }
                    ],
                    "responses": {
                      200: {
                        "description": "",
                        "schema": {
                          "items": {
                            "properties": {
                              "id": {
                                "maxLength": 255,
                                "minLength": 1,
                                "type": "string"
                              },
                              "message": {
                                "maxLength": 255,
                                "minLength": 1,
                                "type": "string"
                              },
                              "message_from": {
                                "enum": [
                                    '1.OSOMATSU',
                                    '2.KARAMATSU',
                                    '3.CHOROMATSU',
                                    '4.ICHIMATSU',
                                    '5.JUSHIMATSU',
                                    '6.TODOMATSU'
                                ],
                                "type": "string"
                              },
                              "message_size": {
                                "minimum": 1,
                                "type": "integer"
                              }
                            }
                          },
                          "type": "object"
                        }
                      }
                    }
                  }
                },
                "/wsmemessages/detail": {
                  "get": {
                    "description": "",
                    "parameters": [
                      {
                        "in": "query",
                        "name": "id",
                        "required": True,
                        "type": "string"
                      }
                    ],
                    "responses": {
                      200: {
                        "description": "",
                        "schema": {
                          "items": {
                            "properties": {
                              "id": {
                                "maxLength": 255,
                                "minLength": 1,
                                "type": "string"
                              },
                              "message": {
                                "maxLength": 255,
                                "minLength": 1,
                                "type": "string"
                              },
                              "message_from": {
                                "enum": [
                                    '1.OSOMATSU',
                                    '2.KARAMATSU',
                                    '3.CHOROMATSU',
                                    '4.ICHIMATSU',
                                    '5.JUSHIMATSU',
                                    '6.TODOMATSU'
                                ],
                                "type": "string"
                              },
                              "message_size": {
                                "minimum": 1,
                                "type": "integer"
                              }
                            }
                          },
                          "type": "object"
                        }
                      }
                    }
                  }
                }
              },
              "produces": [],
              "swagger": "2.0"
            }

        actual = utils.swagger_build('example_wsme_app', '1.0')

        import codecs, json
        fout = codecs.open('example_wsme_app.json', 'w', 'utf_8')
        json.dump(actual, fout, sort_keys=True, indent=2)

        self.maxDiff = None
        self.assertDictEqual(expected, actual)
