from os.path import dirname, join

from sila2.framework import Feature

LockControllerFeature = Feature(open(join(dirname(__file__), "LockController.sila.xml")).read())
