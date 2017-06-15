# -*- coding: utf-8 -*-
"""
This module contains the texts of the part (server and remote)
"""

from util.utiltools import get_pluriel
import partagevolontairequestionnaireParams as pms
from util.utili18n import le2mtrans
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


def get_histo_vars():
    return ["PVQ_period", "PVQ_decision",
            "PVQ_periodpayoff",
            "PVQ_cumulativepayoff"]


def get_histo_head():
    return [le2mtrans(u"Period"), le2mtrans(u"Decision"),
             le2mtrans(u"Period\npayoff"), le2mtrans(u"Cumulative\npayoff")]


def get_text_explanation():
    return trans_PVQ(u"Explanation text")


def get_text_label_decision():
    return trans_PVQ(u"Decision label")


def get_text_summary(period_content):
    txt = trans_PVQ(u"Summary text")
    return txt


