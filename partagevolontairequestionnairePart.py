# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from twisted.internet import defer
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, ForeignKey
from server.servbase import Base
from server.servparties import Partie
from util.utiltools import get_module_attributes
import partagevolontairequestionnaireParams as pms


logger = logging.getLogger("le2m")


class PartiePVQ(Partie):
    __tablename__ = "partie_partagevolontairequestionnaire"
    __mapper_args__ = {'polymorphic_identity': 'partagevolontairequestionnaire'}
    partie_id = Column(Integer, ForeignKey('parties.id'), primary_key=True)
    repetitions = relationship('RepetitionsPVQ')

    def __init__(self, le2mserv, joueur):
        super(PartiePVQ, self).__init__(
            nom="partagevolontairequestionnaire", nom_court="PVQ",
            joueur=joueur, le2mserv=le2mserv)
        self.PVQ_gain_ecus = 0
        self.PVQ_gain_euros = 0

    @defer.inlineCallbacks
    def configure(self):
        logger.debug(u"{} Configure".format(self.joueur))
        yield (self.remote.callRemote("configure", get_module_attributes(pms)))
        self.joueur.info(u"Ok")

    @defer.inlineCallbacks
    def newperiod(self, period):
        """
        Create a new period and inform the remote
        If this is the first period then empty the historic
        :param periode:
        :return:
        """
        logger.debug(u"{} New Period".format(self.joueur))
        self.currentperiod = RepetitionsPVQ(period)
        self.le2mserv.gestionnaire_base.ajouter(self.currentperiod)
        self.repetitions.append(self.currentperiod)
        yield (self.remote.callRemote("newperiod", period))
        logger.info(u"{} Ready for period {}".format(self.joueur, period))

    @defer.inlineCallbacks
    def display_decision(self):
        """
        Display the decision screen on the remote
        Get back the decision
        :return:
        """
        logger.debug(u"{} Decision".format(self.joueur))
        debut = datetime.now()
        reponses = yield(self.remote.callRemote(
            "display_decision"))
        for k, v in reponses.items():
            setattr(self.currentperiod, k, v)
        self.currentperiod.PVQ_decisiontime = (datetime.now() - debut).seconds
        for k, v in reponses.items():
            self.joueur.info(u"{} - {}".format(k, v))
        self.joueur.remove_waitmode()

    def compute_periodpayoff(self):
        self.currentperiod.PVQ_periodpayoff = 0
        self.currentperiod.PVQ_cumulativepayoff = 0

    @defer.inlineCallbacks
    def compute_partpayoff(self):
        self.PVQ_gain_ecus = 0
        self.PVQ_gain_euros = 0
        yield (self.remote.callRemote(
            "set_payoffs", self.PVQ_gain_euros, self.PVQ_gain_ecus))

    @defer.inlineCallbacks
    def display_questionnaire_final(self):
        logger.debug(u"{} display_questionnaire_final".format(self.joueur))
        inputs = yield (self.remote.callRemote("display_questionnaire_final"))
        part_questfinal = self.joueur.get_part("questionnaireFinal")
        for k, v in inputs.items():
            setattr(part_questfinal, k, v)
        self.joueur.info('ok')
        self.joueur.remove_waitmode()


class RepetitionsPVQ(Base):
    __tablename__ = 'partie_partagevolontairequestionnaire_repetitions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    partie_partie_id = Column(
        Integer,
        ForeignKey("partie_partagevolontairequestionnaire.partie_id"))

    PVQ_period = Column(Integer)
    PVQ_appreciation_groupe_prelevement = Column(Integer)
    PVQ_appreciation_groupe_egoiste = Column(Integer)
    PVQ_appreciation_groupe_cooperatif = Column(Integer)
    PVQ_appreciation_groupe_comportement = Column(Integer)
    PVQ_prelement_optimal = Column(Integer)
    PVQ_prelement_optimal_valeur = Column(Integer)
    PVQ_decisiontime = Column(Integer)
    PVQ_periodpayoff = Column(Float)
    PVQ_cumulativepayoff = Column(Float)

    def __init__(self, period):
        self.PVQ_period = period
        self.PVQ_decisiontime = 0
        self.PVQ_periodpayoff = 0
        self.PVQ_cumulativepayoff = 0

    def todict(self, joueur=None):
        temp = {c.name: getattr(self, c.name) for c in self.__table__.columns
                if "PVQ" in c.name}
        if joueur:
            temp["joueur"] = joueur
        return temp
