from os.path import dirname, join

from sila2.framework import Feature

AuthorizationProviderServiceFeature = Feature(
    open(join(dirname(__file__), "AuthorizationProviderService.sila.xml")).read()
)
