# -*- coding: utf-8 -*-
"""
This module contains the GUI
"""
import sys
import logging
from PyQt4 import QtGui, QtCore
from util.utili18n import le2mtrans
import partagevolontairequestionnaireParams as pms
from partagevolontairequestionnaireTexts import trans_PVQ
import partagevolontairequestionnaireTexts as texts_PVQ
from client.cltgui.cltguidialogs import DQuestFinal
from client.cltgui.cltguiwidgets import WPeriod, WExplication, WSpinbox


logger = logging.getLogger("le2m")


class DQuestionnaire(QtGui.QDialog):
    def __init__(self, defered, automatique, parent):
        super(DQuestionnaire, self).__init__(parent)

        self.defered = defered
        self.automatique = automatique

        layout = QtGui.QVBoxLayout()
        self.setLayout(layout)

        self.wexplication = WExplication(
            parent=self, text=texts_PVQ.get_text_explanation(), size=(600, 50))
        layout.addWidget(self.wexplication)

        gridlayout = QtGui.QGridLayout()
        layout.addLayout(gridlayout)

        label_q1 = QtGui.QLabel(
            u"D’après vous, par rapport à un niveau de prélèvement permettant "
            u"d’obtenir\nle meilleur gain du groupe, le niveau de prélèvement "
            u"de votre groupe était: ")
        gridlayout.addWidget(label_q1, 0, 0)
        self.radio_group_q1 = QtGui.QButtonGroup()
        hlayout_q1 = QtGui.QHBoxLayout()
        for k, v in sorted(pms.ECHELLE_ELEVE.items()):
            radio = QtGui.QRadioButton(v)
            self.radio_group_q1.addButton(radio, k)
            hlayout_q1.addWidget(radio)
        hlayout_q1.addSpacerItem(
            QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Expanding,
                              QtGui.QSizePolicy.Minimum))
        gridlayout.addLayout(hlayout_q1, 0, 1)

        gridlayout.addWidget(QtGui.QLabel(
            u"Comment jugez-vous les actions des autres personnes de votre "
            u"groupe: "), 1, 0, 1, 2)

        hlayout_q2_1_label = QtGui.QHBoxLayout()
        hlayout_q2_1_label.addSpacerItem(
            QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Expanding,
                              QtGui.QSizePolicy.Minimum))
        hlayout_q2_1_label.addWidget(QtGui.QLabel(u"Egoistes"))
        gridlayout.addLayout(hlayout_q2_1_label, 2, 0)
        self.radio_group_q2_1 = QtGui.QButtonGroup()
        hlayout_q2_1 = QtGui.QHBoxLayout()
        for k, v in sorted(pms.ECHELLE_ACCORD.items()):
            radio = QtGui.QRadioButton(v)
            self.radio_group_q2_1.addButton(radio, k)
            hlayout_q2_1.addWidget(radio)
        gridlayout.addLayout(hlayout_q2_1, 2, 1)

        hlayout_q2_2_label = QtGui.QHBoxLayout()
        hlayout_q2_2_label.addSpacerItem(
            QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Expanding,
                              QtGui.QSizePolicy.Minimum))
        hlayout_q2_2_label.addWidget(QtGui.QLabel(u"Coopératives"))
        gridlayout.addLayout(hlayout_q2_2_label, 3, 0)

        self.radio_group_q2_2 = QtGui.QButtonGroup()
        hlayout_q2_2 = QtGui.QHBoxLayout()
        for k, v in sorted(pms.ECHELLE_ACCORD.items()):
            radio = QtGui.QRadioButton(v)
            self.radio_group_q2_2.addButton(radio, k)
            hlayout_q2_2.addWidget(radio)
        gridlayout.addLayout(hlayout_q2_2, 3, 1)

        gridlayout.addWidget(QtGui.QLabel(
            u"Vous attendiez-vous à un tel comportement de la part de votre "
            u"groupe?"), 4, 0)
        self.radio_group_q3 = QtGui.QButtonGroup()
        hlayout_q3 = QtGui.QHBoxLayout()
        for k, v in sorted(pms.OUI_NON.items()):
            radio = QtGui.QRadioButton(v)
            self.radio_group_q3.addButton(radio, k)
            hlayout_q3.addWidget(radio)
        hlayout_q3.addSpacerItem(
            QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Expanding,
                              QtGui.QSizePolicy.Minimum))
        gridlayout.addLayout(hlayout_q3, 4, 1)

        gridlayout.addWidget(QtGui.QLabel(
            u"Quel est d’après vous le niveau de prélèvement individuel "
            u"qui, s’il \nétait respecté par les 5 personnes du "
            u"groupe, permettrait d’obtenir \nle gain du groupe maximum?"), 5, 0)
        self.radio_group_q4 = QtGui.QButtonGroup()
        hlayout_q4 = QtGui.QHBoxLayout()
        for k, v in sorted(pms.NE_SAIT_PAS_ENVIRON.items()):
            radio = QtGui.QRadioButton(v)
            self.radio_group_q4.addButton(radio, k)
            hlayout_q4.addWidget(radio)
        self.spinbox_estimation = QtGui.QSpinBox()
        self.spinbox_estimation.setMinimum(0)
        self.spinbox_estimation.setButtonSymbols(QtGui.QSpinBox.NoButtons)
        self.spinbox_estimation.setFixedWidth(30)
        self.spinbox_estimation.setEnabled(False)
        self.radio_group_q4.button(pms.ENVIRON).toggled.connect(
            self.spinbox_estimation.setEnabled)
        hlayout_q4.addWidget(self.spinbox_estimation)
        hlayout_q4.addSpacerItem(
            QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Expanding,
                              QtGui.QSizePolicy.Minimum))
        gridlayout.addLayout(hlayout_q4, 5, 1)

        buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

        if self.automatique:
            pass #todo

    def accept(self):
        try:
            for k, v in self.__dict__.items():
                if type(v) is QtGui.QButtonGroup:
                    if v.checkedId() == -1:
                        raise ValueError(u"Il y a au moins une question à "
                                         u"laquelle vous n'avez pas répondu")
        except ValueError as e:
            QtGui.QMessageBox.warning(
                self, u"Attention", e.message)
            return
        else:
            reponses = dict()
            reponses["PVQ_appreciation_groupe_prelevement"] = \
                self.radio_group_q1.checkedId()
            reponses["PVQ_appreciation_groupe_egoiste"] = \
                self.radio_group_q2_1.checkedId()
            reponses["PVQ_appreciation_groupe_cooperatif"] = \
                self.radio_group_q2_2.checkedId()
            reponses["PVQ_appreciation_groupe_comportement"] = \
                self.radio_group_q3.checkedId()
            reponses["PVQ_prelement_optimal"] = \
                self.radio_group_q4.checkedId()
            reponses["PVQ_prelement_optimal_valeur"] = \
                self.spinbox_estimation.value() if \
                    self.radio_group_q4.checkedId() == pms.ENVIRON else None
            if not self.automatique:
                confirmation = QtGui.QMessageBox.question(
                    self, u"Confirmation", u"Vous confirmez vos réponses?",
                    QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
                if confirmation != QtGui.QMessageBox.Yes:
                    return
            logger.info(u"Send back: {}".format(reponses))
            super(DQuestionnaire, self).accept()
            self.defered.callback(reponses)

    def reject(self):
        pass


class DQuestionnaireFinalPVQ(DQuestFinal):
    def __init__(self, defered, automatique, parent):
        DQuestFinal.__init__(self, defered, automatique, parent)

        self._couple.setVisible(False)
        self._brothers.setVisible(False)
        self._brothers_rank.setVisible(False)
        self._sport.setVisible(False)
        self._sport_competition.setVisible(False)
        self._sport_individuel.setVisible(False)
        self._religion_belief.setVisible(False)
        self._religion_name.setVisible(False)
        self._religion_place.setVisible(False)

        self.setMinimumSize(0, 0)
        self.setMaximumSize(16777215, 16777215)
        self.adjustSize()
        self.setFixedSize(self.size())

    def _accept(self):
        try:
            self._timer_automatique.stop()
        except AttributeError:
            pass
        inputs = self._get_inputs()
        if inputs is None:
            return
        if not self._automatique:
            confirm = QtGui.QMessageBox.question(
                self, le2mtrans(u"Confirmation"),
                le2mtrans(u"Do you confirm your answers?"),
                QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
            if confirm != QtGui.QMessageBox.Yes:
                return
        logger.info(u"Send back: {}".format(inputs))
        self.accept()
        self._defered.callback(inputs)


if __name__ == "__main__":
    app = QtGui.QApplication([])
    screen = DQuestionnaireFinalPVQ(None, 0, None)
    screen.show()
    sys.exit(app.exec_())