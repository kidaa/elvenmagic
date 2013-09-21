Creating custom views with collective.listingviews
==================================================

.. author:: Asko Soukka
.. categories:: Plone
.. tags:: collective, listingviews
.. comments::

.. code:: robotframework
   :class: hidden

   *** Settings ***

   Resource  plone/app/robotframework/server.robot

   Library  Selenium2Screenshots

   Suite Setup  Setup Plone site with Cover
   Suite Teardown  Run keywords  Teardown Plone site  Close all browsers

   *** Keywords ***

   Setup Plone site with Cover
       Setup Plone site  elvenmagic.ELVENMAGIC_ROBOT_TESTING
       Import library  Remote  ${PLONE_URL}/RobotRemote
       Import library  elvenmagic.Zope2ServerConfiguration

       Configure package  collective.listingviews

       Enable autologin as  Manager
       Set autologin username  Dwarven Artisan

       Set window size  640  768

   Pause
       Import library  Dialogs
       Pause execution

`collective.listingviews`_ is a real gem, if you only know how to use it.

.. _collective.listingviews: http://pypi.python.org/pypi/collective.listingviews

.. image:: collective-listingviews-activated.png

.. code:: robotframework
   :class: hidden

   *** Test Cases ***

   Open Plone
       Go to  ${PLONE_URL}

       Capture page screenshot  collective-listingviews-activated.png
