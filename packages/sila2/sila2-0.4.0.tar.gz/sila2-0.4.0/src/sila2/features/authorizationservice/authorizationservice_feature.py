from os.path import dirname, join

from sila2.framework import Feature

AuthorizationServiceFeature = Feature(open(join(dirname(__file__), "AuthorizationService.sila.xml")).read())
