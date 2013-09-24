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
   Resource  plone/app/robotframework/keywords.robot

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

       ${uuid} =  Create content
       ...  type=Folder  id=gallery  title=Gallery
       Create content  type=Image  container=${uuid}
       ...  id=image-1  title=Image 1  description=The first image
       Create content  type=Image  container=${uuid}
       ...  id=image-2  title=Image 2  description=The second image
       Create content  type=Image  container=${uuid}
       ...  id=image-3  title=Image 3  description=The third image
       Create content  type=Image  container=${uuid}
       ...  id=image-4  title=Image 4  description=The fourth image
       Create content  type=Image  container=${uuid}
       ...  id=image-5  title=Image 5  description=The fifth image
       Create content  type=Image  container=${uuid}
       ...  id=image-6  title=Image 6  description=The sixth image
       Create content  type=Image  container=${uuid}
       ...  id=image-7  title=Image 7  description=The seventh image
       Create content  type=Image  container=${uuid}
       ...  id=image-8  title=Image 8  description=The eighth image
       Create content  type=Image  container=${uuid}
       ...  id=image-9  title=Image 9  description=The ninth image

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

`collective.listingviews`_ is a real gem, if only you knew how to use it.

.. _collective.listingviews: http://pypi.python.org/pypi/collective.listingviews

Next I'll demonstrate it by creating a simple image listing view with image
previews and their dimensions. The resulting listing view is simple, but
can be enhanced with CSS later:

.. figure:: collective-listingviews-image-listing.png
   :align: center

So, let's begin.

Once we have managed to `install the add-on with buildout`__ and restart our
site, we should be able to activate the add-on through *Add-ons*-panel in
*Site Setup*:

__ https://plone.org/documentation/kb/add-ons/installing

.. figure:: collective-listingviews-activated.png
   :align: center

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

Activating *collective.listingviews* adds two new configuration panels into
*Site Setup*:

.. figure:: collective-listingviews-configlets-01.png
   :align: center

.. code:: robotframework
   :class: hidden

   *** Test Cases ***

   Show Listing Views Configlets
       Go to  ${PLONE_URL}/plone_control_panel

       Page should contain element
       ...  xpath=//a[contains(@href, 'listingviewfields')]

       Assign id to element
       ...  xpath=//a[contains(@href, 'listingviewfields')]/ancestor::ul[@class='configlets']/parent::div/parent::div
       ...  addons-configlets

       Page should contain element  addons-configlets

       Assign id to element
       ...  xpath=//div[@id='addons-configlets']/preceding-sibling::h2[1]
       ...  addons-configlets-h2

       Assign id to element
       ...  xpath=//a[contains(@href, 'listingviewfields')]/ancestor::li[1]
       ...  addons-configlets-listingviewfields

       Assign id to element
       ...  xpath=//a[contains(@href, 'listingviews')]/ancestor::li[1]
       ...  addons-configlets-listingviews

       Highlight  addons-configlets

       Capture and crop page screenshot
       ...  collective-listingviews-configlets-01.png
       ...  content

       Remove highlighting  addons-configlets

       Highlight  addons-configlets-listingviewfields

       Capture and crop page screenshot
       ...  collective-listingviews-configlets-02.png
       ...  addons-configlets  addons-configlets-h2

       Remove highlighting  addons-configlets-listingviewfields

       Highlight  addons-configlets-listingviews

       Capture and crop page screenshot
       ...  collective-listingviews-configlets-03.png
       ...  addons-configlets  addons-configlets-h2

Visiting the first one (*Listing Custom Fields*) allows us to expose custom
properties from custom content types or define new ways to display existing
properties from the default content types.

.. figure:: collective-listingviews-configlets-02.png
   :align: center

Let's start by clicking *Add* to add a new custom field display definition:

.. figure:: collective-listingviews-custom-field-01.png
   :align: center

.. code:: robotframework
   :class: hidden

   *** Test Cases ***

   Show how to add a new custom field
       Go to  ${PLONE_URL}/@@listingviewfields_controlpanel

       Highlight  form-widgets-fields-buttons-add

       Capture and crop page screenshot
       ...  collective-listingviews-custom-field-01.png
       ...  content

       Click button  form-widgets-fields-buttons-add

Then let's fill the fields properly for displaying dimensions from an
image and finish the definition by clicking *Save*.

.. figure:: collective-listingviews-custom-field-02.png
   :align: center

.. code:: robotframework
   :class: hidden

   *** Test Cases ***

   Show how to fill details for a new custom field
       Page should contain element  form-widgets-fields-0-widgets-id

       Input text  form-widgets-fields-0-widgets-id  dimensions
       Input text  form-widgets-fields-0-widgets-name  Dimensions
       Input text  form-widgets-fields-0-widgets-tal_statement
       ...  python:'%s x %s' % item.getObject().getSize()

       Highlight  form-buttons-save

       Capture and crop page screenshot
       ...  collective-listingviews-custom-field-02.png
       ...  content

       Click button  form-buttons-save

Read more about using TAL-statements (TAL-expressions) from `Plone Developer
Manual`__.

__ http://developer.plone.org/functionality/expressions.html

Then let's repeat this by adding a one more field for displaying a thumbnail
preview of the image:

.. figure:: collective-listingviews-custom-field-03.png
   :align: center

.. code:: robotframework
   :class: hidden

   *** Test Cases ***

   Show how to add an another custom field
       Page should contain element  form-widgets-fields-buttons-add

       Click button  form-widgets-fields-buttons-add

       Page should contain element  form-widgets-fields-1-widgets-id

       Input text  form-widgets-fields-1-widgets-id  preview
       Input text  form-widgets-fields-1-widgets-name  Preview
       Input text  form-widgets-fields-1-widgets-tal_statement
       ...  python:item.getObject().tag(scale='thumb')

       Highlight  form-buttons-save

       Capture and crop page screenshot
       ...  collective-listingviews-custom-field-03.png
       ...  formfield-form-widgets-fields-1

       Click button  form-buttons-save

Once the required custom display fields are defined, we are ready for defining
a new listing view by opening *Listing View* -configlet from *Site Setup*:

.. figure:: collective-listingviews-configlets-03.png
   :align: center

Adding a new listing view is pretty straightforward:

.. figure:: collective-listingviews-add-view.png
   :align: center

.. code:: robotframework
   :class: hidden

   *** Test Cases ***

   Show how to add a new listing view
       Go to  ${PLONE_URL}/@@listingviews_controlpanel

       Page should contain element  crud-add-form-widgets-id

       Input text  crud-add-form-widgets-id  image_listing
       Input text  crud-add-form-widgets-name  Image Listing

       Add pointy note  crud-add-form-widgets-id
       ...  Give the view an unique id
       ...  position=right

       Add pointy note  crud-add-form-widgets-name
       ...  Give the view a menu label
       ...  position=right

       Select from list  crud-add-form-widgets-listing_fields-from  Title:tolink
       Click button
       ...  css=#formfield-crud-add-form-widgets-listing_fields button[name='from2toButton']
       Select from list  crud-add-form-widgets-listing_fields-from  :preview
       Click button
       ...  css=#formfield-crud-add-form-widgets-listing_fields button[name='from2toButton']
       Select from list  crud-add-form-widgets-listing_fields-from  :dimensions
       Click button
       ...  css=#formfield-crud-add-form-widgets-listing_fields button[name='from2toButton']

       Add pointy note
       ...  css=#formfield-crud-add-form-widgets-listing_fields table
       ...  Define properties to show for each of listed item
       ...  position=top

       Add pointy note
       ...  css=#formfield-crud-add-form-widgets-restricted_to_types table
       ...  Restrict types where the new view is available to be selected
       ...  position=bottom

       Highlight  crud-add-form-buttons-add

       Add pointy note  crud-add-form-buttons-add
       ...  Save the new listing view
       ...  position=right

       Capture and crop page screenshot
       ...  collective-listingviews-add-view.png
       ...  content

       Click button  crud-add-form-buttons-add

Finally, we can go to a folder with images, open its *Display*-menu and
select our brand new view to show the folder contents:

.. figure:: collective-listingviews-select-view.png
   :align: center

.. code:: robotframework
   :class: hidden

   *** Test Cases ***

   Show how to activate new listing view
       Go to  ${PLONE_URL}/gallery

       Open display menu

       Highlight  css=a[id$=image_listing]

       Add pointy note  plone-contentmenu-display
       ...  Click to open the display menu
       ...  position=bottom

       Add pointy note  css=a[id$=image_listing]
       ...  Click to select Image Listing -view
       ...  position=left

       Capture and crop page screenshot
       ...  collective-listingviews-select-view.png
       ...  edit-bar  css=#plone-contentmenu-display .actionMenuContent

       Click link
       ...  plone-contentmenu-display-collective.listingviews.image_listing

       Set window size  640  1024

       Capture viewport screenshot
       ...  collective-listingviews-image-listing.png

And enjoy our brand new view:

.. figure:: collective-listingviews-image-listing.png
   :align: center

Jus great, isn't it!

Disclaimer
----------

With great power comes great responsibility. It's extremely easy to create
views that break when they are trying to render unexpected content types. If
you want to play it safe, use custom listing views only with collections, which
allow you to limit the view see only selected content types.

.. This robotframework-directive will prevent images to be re-generated, but it
   won't know if the tests generating the images have changed...

.. robotframework::
   :creates: collective-listingviews-activated.png
             collective-listingviews-add-view.png
             collective-listingviews-configlets-01.png
             collective-listingviews-configlets-02.png
             collective-listingviews-configlets-03.png
             collective-listingviews-custom-field-01.png
             collective-listingviews-custom-field-02.png
             collective-listingviews-custom-field-03.png
             collective-listingviews-image-listing.png
             collective-listingviews-select-view.png

