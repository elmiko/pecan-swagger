#!/bin/env python
from pecan_swagger import utils
import myapp

print(utils.swagger_build('myapp', '1.0'))
