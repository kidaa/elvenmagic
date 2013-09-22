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

   Suite Setup  Setup Plone site with ListingViews
   Suite Teardown  Run keywords  Teardown Plone site  Close all browsers

   *** Keywords ***

   Setup Plone site with ListingViews
       ${CONFIGURE_PACKAGES} =  Create list
       ...  collective.listingviews
       ${APPLY_PROFILES} =  Create list
       ...  collective.listingviews:default
       Setup Plone site  elvenmagic.ELVENMAGIC_ROBOT_TESTING
       Import library  Remote  ${PLONE_URL}/RobotRemote

       Enable autologin as  Manager
       Set autologin username  Dwarven Artisan

       Set window size  640  768

   Highlight
       [Arguments]  ${locator}
       Update element style  ${locator}  outline  3px dotted red

   Pause
       Import library  Dialogs
       Pause execution

`collective.listingviews`_ is a real gem, if you only know how to use it.

.. _collective.listingviews: http://pypi.python.org/pypi/collective.listingviews

.. image:: collective-listingviews-activated.png

.. code:: robotframework
   :class: hidden

   *** Test Cases ***

   Show activated Listing Views
       Go to  ${PLONE_URL}/prefs_install_products_form

       Page should contain element
       ...  xpath=//*[@id='collective.listingviews']

       Assign id to element
       ...  xpath=//*[@id='collective.listingviews']/parent::*
       ...  addons-collective-listingviews

       Assign id to element
       ...  xpath=//*[@id='collective.listingviews']/ancestor::form
       ...  addons-enabled

       Highlight  addons-collective-listingviews

       Capture and crop page screenshot
       ...  collective-listingviews-activated.png
       ...  addons-enabled

.. image:: collective-listingviews-configlets.png

.. code:: robotframework
   :class: hidden

   *** Test Cases ***

   Show Listing Views Configlets
       Go to  ${PLONE_URL}/plone_control_panel

       Page should contain element
       ...  xpath=//a[contains(@href, 'listingviews')]

       Assign id to element
       ...  xpath=//a[contains(@href, 'listingviews')]/ancestor::ul[@class='configlets']/parent::div/parent::div
       ...  addons-configlets

       Page should contain element  addons-configlets

       Assign id to element
       ...  xpath=//div[@id='addons-configlets']/preceding-sibling::h2[1]
       ...  addons-configlets-h2

       Capture and crop page screenshot
       ...  collective-listingviews-configlets.png
       ...  addons-configlets  addons-configlets-h2
