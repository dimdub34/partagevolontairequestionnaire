# -*- coding: utf-8 -*-

import logging
from collections import OrderedDict
from twisted.internet import defer
from util.utili18n import le2mtrans
import partagevolontairequestionnaireParams as pms
from PyQt4 import QtGui


logger = logging.getLogger("le2m.{}".format(__name__))


class Serveur(object):
    def __init__(self, le2mserv):
        self._le2mserv = le2mserv
        actions = OrderedDict()
        actions[u"Démarrer"] = lambda _: \
            self._demarrer()
        self._le2mserv.gestionnaire_graphique.add_topartmenu(
            u"Partage volontaire - Questionnaire pour tous", actions)

        # modification du questionnaire final
        self._le2mserv.gestionnaire_graphique.screen.action_finalquest.\
            triggered.disconnect()
        self._le2mserv.gestionnaire_graphique.screen.action_finalquest.\
            triggered.connect(lambda _: self.demarrer_questionnaire_final())

    @defer.inlineCallbacks
    def _demarrer(self):
        """
        Start the part
        :return:
        """
        # check conditions =====================================================
        if not self._le2mserv.gestionnaire_graphique.question(
                        le2mtrans(u"Start") + u" partagevolontairequestionnaire?"):
            return

        # init part ============================================================
        yield (self._le2mserv.gestionnaire_experience.init_part(
            "partagevolontairequestionnaire", "PartiePVQ",
            "RemotePVQ", pms))
        self._tous = self._le2mserv.gestionnaire_joueurs.get_players(
            'partagevolontairequestionnaire')

        # set parameters on remotes
        yield (self._le2mserv.gestionnaire_experience.run_step(
            le2mtrans(u"Configure"), self._tous, "configure"))
        
        # Start part ===========================================================
            # init period
        yield (self._le2mserv.gestionnaire_experience.run_func(
            self._tous, "newperiod", 0))

        # decision
        yield(self._le2mserv.gestionnaire_experience.run_step(
            le2mtrans(u"Decision"), self._tous, "display_decision"))

        # End of part ==========================================================
        yield (self._le2mserv.gestionnaire_experience.finalize_part(
            "partagevolontairequestionnaire"))

    @defer.inlineCallbacks
    def demarrer_questionnaire_final(self):
        if not self._le2mserv.gestionnaire_base.is_created() or \
        not hasattr(self, "_tous"):
            QtGui.QMessageBox.warning(
                self._le2mserv.gestionnaire_graphique.screen,
                u"Attention",
                u"Il faut lancer au moins une partie avant de lancer ce "
                u"questionnaire")
            return

        confirmation = QtGui.QMessageBox.question(
            self._le2mserv.gestionnaire_graphique.screen,
            le2mtrans(u"Confirmation"),
            le2mtrans(u"Start the final questionnaire?"),
            QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok)
        if confirmation != QtGui.QMessageBox.Ok:
            return

        yield (self._le2mserv.gestionnaire_experience.run_step(
            u"Questionnaire final", self._tous,
            "display_questionaire_final"))
