# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import polklibrary.migrations.export


class PolklibraryMigrationsExportLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=polklibrary.migrations.export)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'polklibrary.migrations.export:default')


POLKLIBRARY_MIGRATIONS_EXPORT_FIXTURE = PolklibraryMigrationsExportLayer()


POLKLIBRARY_MIGRATIONS_EXPORT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(POLKLIBRARY_MIGRATIONS_EXPORT_FIXTURE,),
    name='PolklibraryMigrationsExportLayer:IntegrationTesting'
)


POLKLIBRARY_MIGRATIONS_EXPORT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(POLKLIBRARY_MIGRATIONS_EXPORT_FIXTURE,),
    name='PolklibraryMigrationsExportLayer:FunctionalTesting'
)


POLKLIBRARY_MIGRATIONS_EXPORT_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        POLKLIBRARY_MIGRATIONS_EXPORT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='PolklibraryMigrationsExportLayer:AcceptanceTesting'
)
