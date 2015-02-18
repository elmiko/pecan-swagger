#!/bin/env python
import json
import pprint

from pecan_swagger import utils
import myapp

pp = pprint.PrettyPrinter(indent=2)
pp.pprint(utils.swagger_build('myapp', '1.0'))
