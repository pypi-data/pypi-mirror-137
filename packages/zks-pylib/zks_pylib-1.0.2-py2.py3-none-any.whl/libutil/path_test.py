#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging #logging
import logging.handlers
import os

#lib도, 이렇게 접근하도록 한다.
from libutil.logger import *

class PathTest:

    def __init__(self):

        LOG().debug("test")

        pass