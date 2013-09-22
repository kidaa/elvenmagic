# -*- coding: utf-8 -*-
import sys

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
    ploneSite,
    PloneSandboxLayer)
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


class ElvenMagicLayer(PloneSandboxLayer):

    def setUpZope(self, app, configurationContext):
        from robot.libraries.BuiltIn import BuiltIn

        for name in BuiltIn().get_variable_value('${META_PACKAGES}', []):
            if not name in sys.modules:
                __import__(name)
            package = sys.modules[name]
            xmlconfig.file('meta.zcml', package,
                           context=configurationContext)

        for name in BuiltIn().get_variable_value('${CONFIGURE_PACKAGES}', []):
            if not name in sys.modules:
                __import__(name)
            package = sys.modules[name]
            xmlconfig.file('configure.zcml', package,
                           context=configurationContext)

        for name in BuiltIn().get_variable_value('${OVERRIDE_PACKAGES}', []):
            if not name in sys.modules:
                __import__(name)
            package = sys.modules[name]
            xmlconfig.includeOverrides(
                configurationContext, 'overrides.zcml', package=package)

        for name in BuiltIn().get_variable_value('${INSTALL_PACKAGES}', []):
            if not name in sys.modules:
                __import__(name)
            package = sys.modules[name]
            z2.installProduct(app, package)

    def setUpPloneSite(self, portal):
        from robot.libraries.BuiltIn import BuiltIn

        for name in BuiltIn().get_variable_value('${APPLY_PROFILES}', []):
            self.applyProfile(portal, name)

ELVENMAGIC_FIXTURE = ElvenMagicLayer()


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
           ELVENMAGIC_FIXTURE,
           z2.ZSERVER_FIXTURE),
    name="ElvenMagic:Robot"
)
