# -*- coding: utf-8 -*-

import logging
from collections import OrderedDict
from twisted.internet import defer
from util.utili18n import le2mtrans
import partagevolontairequestionnaireParams as pms


logger = logging.getLogger("le2m.{}".format(__name__))


class Serveur(object):
    def __init__(self, le2mserv):
        self._le2mserv = le2mserv
        actions = OrderedDict()
        actions[u"Démarrer"] = lambda _: \
            self._demarrer()
        self._le2mserv.gestionnaire_graphique.add_topartmenu(
            u"Partage volontaire - Questionnaire pour tous", actions)

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
        self._le2mserv.gestionnaire_graphique.infoserv(
            [None, le2mtrans(u"Period") + u" {}".format(0)])
        self._le2mserv.gestionnaire_graphique.infoclt(
            [None, le2mtrans(u"Period") + u" {}".format(0)],
            fg="white", bg="gray")
        yield (self._le2mserv.gestionnaire_experience.run_func(
            self._tous, "newperiod", 0))

        # decision
        yield(self._le2mserv.gestionnaire_experience.run_step(
            le2mtrans(u"Decision"), self._tous, "display_decision"))

        # End of part ==========================================================
        yield (self._le2mserv.gestionnaire_experience.finalize_part(
            "partagevolontairequestionnaire"))
