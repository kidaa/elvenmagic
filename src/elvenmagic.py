# -*- coding: utf-8 -*-
from App.Common import aq_base

from zope.component.hooks import (
    getSiteManager
)

from plone.app.robotframework import (
    AutoLogin,
    RemoteLibraryLayer
)

from zope.configuration import xmlconfig
from plone.app.robotframework.remote import RemoteLibrary
from plone.app.testing import (
    PLONE_FIXTURE,
    ploneSite
)
from plone.app.testing.layers import FunctionalTesting
from Products.MailHost.interfaces import IMailHost

from plone.testing import (
    Layer,
    z2
)


class MockMailHostLayer(Layer):
    """Layer for setting up a MockMailHost to store all sent messages as
    strings into a list at portal.MailHost.messages

    """
    defaultBases = (PLONE_FIXTURE,)

    def setUp(self):
        # Note: CMFPlone can be imported safely only when a certain
        # zope.testing-set environment variable is in place.
        from Products.CMFPlone.tests.utils import MockMailHost
        with ploneSite() as portal:
            portal._original_MailHost = portal.MailHost
            portal.MailHost = mailhost = MockMailHost('MailHost')
            sm = getSiteManager(context=portal)
            sm.unregisterUtility(provided=IMailHost)
            sm.registerUtility(mailhost, provided=IMailHost)

    def tearDown(self):
        with ploneSite() as portal:
            portal.MailHost = portal._original_MailHost
            sm = getSiteManager(context=portal)
            sm.unregisterUtility(provided=IMailHost)
            sm.registerUtility(aq_base(portal._original_MailHost),
                               provided=IMailHost)

MOCK_MAILHOST_FIXTURE = MockMailHostLayer()


class Zope2ServerConfiguration(object):
    """Additional configuration keywords for Zope2-instances started using
    plone.app.robotframework.Zope2Server-library

    **Warning** This works only when being called within the same process
    with Zope2Server-library based Zope2-server.
    """

    def configure_package(self, name,
                          meta=False, configure=True, overrides=False,
                          install=False):
        """Configure named package into the last known configurationContext
        """
        import sys
        __import__(name)
        package = sys.modules[name]

        from robot.libraries.BuiltIn import BuiltIn
        server = BuiltIn().get_library_instance(
            "plone.app.robotframework.Zope2Server")
        configurationContext = server.zope_layer["configurationContext"]

        if meta:
            xmlconfig.file('meta.zcml', package,
                           context=configurationContext)

        if configure:
            xmlconfig.file('configure.zcml', package,
                           context=configurationContext)

        if overrides:
            xmlconfig.includeOverrides(
                configurationContext,
                'overrides.zcml',
                package=package)

        if install:
            import Zope2.App.startup
            z2.installProduct(Zope2.App.startup.app(), package)


class CustomRemoteKeywords(RemoteLibrary):
    """Useful remote keywords, which are run inside a normal ZPublisher-request
    environment with all the related Plone-magic in place

    """
    def get_the_last_sent_email(self):
        """Return the last sent email from MockMailHost sent messages storage
        """
        return self.MailHost.messages[-1] if self.MailHost.messages else u""


ELVENMAGIC_REMOTE_LIBRARY_FIXTURE = RemoteLibraryLayer(
    bases=(PLONE_FIXTURE,),
    libraries=(AutoLogin, CustomRemoteKeywords),
    name="ElvenMagic:RobotRemote"
)

ELVENMAGIC_ROBOT_TESTING = FunctionalTesting(
    bases=(MOCK_MAILHOST_FIXTURE,
           ELVENMAGIC_REMOTE_LIBRARY_FIXTURE,
           z2.ZSERVER_FIXTURE),
    name="AutoLogin:Robot"
)
