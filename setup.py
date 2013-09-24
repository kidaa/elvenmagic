from setuptools import setup, find_packages

setup(
    name='elvenmagic',
    version='1.0.0',
    description='',
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Programming Language :: Python',
    ],
    keywords='',
    author='Asko Soukka',
    author_email='asko.soukka@iki.fi',
    url='https://github.com/datakurre/elvenmagic/',
    license='GPL',
    py_modules=[
        'elvenmagic'
    ],
    packages=find_packages("src", exclude=["ez_setup"]),
    package_dir={"": "src"},
    zip_safe=False,
    install_requires=[
        'setuptools',
        'plone.api',
        'plone.app.robotframework',
        'sphinxcontrib-robotframework[docs]',

        # Reviewed products:
        'collective.listingviews',
        'plone.app.workflowmanager',
    ]
)
