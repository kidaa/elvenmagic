Customize Plone workflows with plone.app.workflowmanager
========================================================

.. author:: Asko Soukka
.. categories:: Plone
.. tags:: workflowmanager
.. comments::

.. code:: robotframework
   :class: hidden

   *** Settings ***

   Resource  plone/app/robotframework/server.robot
   Resource  plone/app/robotframework/keywords.robot

   Library  Selenium2Screenshots

   Suite Setup  Setup Plone site with WorkflowManager
   Suite Teardown  Run keywords  Teardown Plone site  Close all browsers

   *** Keywords ***

   Setup Plone site with WorkflowManager
       ${CONFIGURE_PACKAGES} =  Create list
       ...  plone.app.workflowmanager
       ${APPLY_PROFILES} =  Create list
       ...  plone.app.workflowmanager:default
       Setup Plone site  elvenmagic.ELVENMAGIC_ROBOT_TESTING
       Import library  Remote  ${PLONE_URL}/RobotRemote

       Enable autologin as  Manager
       Set autologin username  Dwarven Artisan

       Set window size  640  768

   Highlight
       [Arguments]  ${locator}
       Update element style  ${locator}  outline  3px dotted red

   Remove highlighting
       [Arguments]  ${locator}
       Update element style  ${locator}  outline  none

   Pause
       Import library  Dialogs
       Pause execution

`plone.app.workflowmanager`_ really frees the

.. _plone.app.workflowmanager: http://pypi.python.org/pypi/plone.app.workflowmanager

Next I'll demonstrate it by creating a simple image listing view with image
previews and their dimensions. The resulting listing view is simple, but
can be enhanced with CSS later:

.. figure:: plone-app-workflowmanager-activated.png
   :align: center

.. code:: robotframework
   :class: hidden

   *** Test Cases ***

   Show activated Listing Views
       Go to  ${PLONE_URL}/prefs_install_products_form

       Pause

       Page should contain element
       ...  xpath=//*[@id='plone.app.workflowmanager']

       Assign id to element
       ...  xpath=//*[@id='plone.app.workflowmanager']/parent::*
       ...  addons-plone-app-workflowmanager

       Assign id to element
       ...  xpath=//*[@id='plone.app.workflowmanager']/ancestor::form
       ...  addons-enabled

       Highlight  addons-plone-app-workflowmanager

       Capture and crop page screenshot
       ...  plone-app-workflowmanager-activated.png
       ...  addons-enabled


