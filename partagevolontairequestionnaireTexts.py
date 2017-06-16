# -*- coding: utf-8 -*-
"""
This module contains the texts of the part (server and remote)
"""

import os
import configuration.configparam as params
import gettext
import logging

logger = logging.getLogger("le2m")
try:
    localedir = os.path.join(params.getp("PARTSDIR"), "partagevolontairequestionnaire",
                             "locale")
    trans_PVQ = gettext.translation(
      "partagevolontairequestionnaire", localedir, languages=[params.getp("LANG")]).ugettext
except (AttributeError, IOError):
    logger.critical(u"Translation file not found")
    trans_PVQ = lambda x: x  # if there is an error, no translation


def get_text_explanation():
    return trans_PVQ(u"Merci de répondre aux questions ci-dessous. "
                     u"Le traitement des réponses sera totalement anonyme.")

