# -*- coding: utf-8 -*-

import logging
import random

from twisted.internet import defer
from client.cltremote import IRemote
import partagevolontairequestionnaireParams as pms
from partagevolontairequestionnaireGui import DQuestionnaire, DQuestionnaireFinalPVQ


logger = logging.getLogger("le2m")


class RemotePVQ(IRemote):
    def __init__(self, le2mclt):
        IRemote.__init__(self, le2mclt)

    def remote_configure(self, params):
        """
        Set the same parameters as in the server side
        :param params:
        :return:
        """
        logger.info(u"{} configure".format(self._le2mclt.uid))
        for k, v in params.viewitems():
            setattr(pms, k, v)

    def remote_newperiod(self, period):
        """
        Set the current period and delete the history
        :param period: the current period
        :return:
        """
        logger.info(u"{} Period {}".format(self._le2mclt.uid, period))
        self.currentperiod = period

    def remote_display_decision(self):
        logger.info(u"{} Decision".format(self._le2mclt.uid))
        if self._le2mclt.simulation:
            reponses = dict()
            reponses["PVQ_appreciation_groupe_prelevement"] = random.choice(
                pms.ECHELLE_ELEVE.keys())
            reponses["PVQ_appreciation_groupe_egoiste"] = random.choice(
                pms.ECHELLE_ACCORD.keys())
            reponses["PVQ_appreciation_groupe_cooperatif"] = random.choice(
                pms.ECHELLE_ACCORD.keys())
            reponses["PVQ_appreciation_groupe_comportement"] = random.choice(
                pms.OUI_NON.keys())
            reponses["PVQ_prelement_optimal"] = random.choice(
                pms.NE_SAIT_PAS_ENVIRON.keys())
            reponses["PVQ_prelement_optimal_valeur"] = \
                random.randint(0, 30) if \
                    reponses["PVQ_prelement_optimal"] == pms.ENVIRON else None
            logger.info("send back: {}".format(reponses))
            return reponses
        else: 
            defered = defer.Deferred()
            ecran_decision = DQuestionnaire(
                defered, self._le2mclt.automatique, self._le2mclt.screen)
            ecran_decision.show()
            return defered

    def remote_display_questionnaire_final(self):
        logger.info(u"{} display_questionnaire_final".format(self._le2mclt.uid))
        if self.le2mclt.simulation:
            from datetime import datetime
            inputs = {}
            today_year = datetime.now().year
            inputs['naissance'] = today_year - random.randint(16, 60)
            inputs['genre'] = random.randint(0, 1)
            inputs['nationalite'] = random.randint(1, 100)
            inputs['etudiant'] = random.randint(0, 1)
            if inputs['etudiant'] == 0:
                inputs['etudiant_discipline'] = random.randint(1, 10)
                inputs['etudiant_niveau'] = random.randint(1, 6)
            return inputs

        else:
            defered = defer.Deferred()
            screen = DQuestionnaireFinalPVQ(defered, self.le2mclt.automatique,
                                   self.le2mclt.screen)
            screen.show()
            return defered


