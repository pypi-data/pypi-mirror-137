from os.path import dirname, join

from sila2.framework import Feature

AuthenticationServiceFeature = Feature(open(join(dirname(__file__), "AuthenticationService.sila.xml")).read())
