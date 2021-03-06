#!/bin/sh
PRODUCTNAME='collective.rcse'
I18NDOMAIN=$PRODUCTNAME

# Synchronise the .pot with the templates.
../../../../bin/i18ndude rebuild-pot --exclude resources --pot locales/${PRODUCTNAME}.pot --create ${I18NDOMAIN} .

# Synchronise the resulting .pot with the .po files
../../../../bin/i18ndude sync --pot locales/${PRODUCTNAME}.pot locales/*/LC_MESSAGES/${PRODUCTNAME}.po
