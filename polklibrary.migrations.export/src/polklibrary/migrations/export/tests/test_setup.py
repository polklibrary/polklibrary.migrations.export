# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from polklibrary.migrations.export.testing import POLKLIBRARY_MIGRATIONS_EXPORT_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that polklibrary.migrations.export is properly installed."""

    layer = POLKLIBRARY_MIGRATIONS_EXPORT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if polklibrary.migrations.export is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'polklibrary.migrations.export'))

    def test_browserlayer(self):
        """Test that IPolklibraryMigrationsExportLayer is registered."""
        from polklibrary.migrations.export.interfaces import (
            IPolklibraryMigrationsExportLayer)
        from plone.browserlayer import utils
        self.assertIn(IPolklibraryMigrationsExportLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = POLKLIBRARY_MIGRATIONS_EXPORT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['polklibrary.migrations.export'])

    def test_product_uninstalled(self):
        """Test if polklibrary.migrations.export is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'polklibrary.migrations.export'))

    def test_browserlayer_removed(self):
        """Test that IPolklibraryMigrationsExportLayer is removed."""
        from polklibrary.migrations.export.interfaces import IPolklibraryMigrationsExportLayer
        from plone.browserlayer import utils
        self.assertNotIn(IPolklibraryMigrationsExportLayer, utils.registered_layers())
