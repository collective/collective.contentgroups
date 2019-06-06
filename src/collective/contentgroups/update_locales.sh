#!/bin/bash
# Run this script to update the translations.
i18ndude rebuild-pot --pot locales/collective.contentgroups.pot --create collective.contentgroups .
i18ndude sync --pot locales/collective.contentgroups.pot $(find . -name "collective.contentgroups.po")
