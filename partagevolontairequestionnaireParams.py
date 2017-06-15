# -*- coding: utf-8 -*-
"""=============================================================================
This modules contains the variables and the parameters.
Do not change the variables.
Parameters that can be changed without any risk of damages should be changed
by clicking on the configure sub-menu at the server screen.
If you need to change some parameters below please be sure of what you do,
which means that you should ask to the developer ;-)
============================================================================="""

# variables --------------------------------------------------------------------
BASELINE = 0
TREATMENTS_NAMES = {BASELINE: "Baseline"}

NON = PAS_DU_TOUT_D_ACCORD = TROP_ELEVE = NE_SAIT_PAS = 0
OUI = PAS_D_ACCORD = UN_PEU_ELEVE = ENVIRON = 1
NI_D_ACCORD_NI_PAS_D_ACCORD = OPTIMAL = 2
D_ACCORD = UN_PEU_FAIBLE = 3
TOUT_A_FAIT_D_ACCORD = TROP_FAIBLE = 4

ECHELLE_ELEVE = {TROP_ELEVE: u"Trop élevé", UN_PEU_ELEVE: u"Un peu élevé",
                 OPTIMAL: u"Optimal", UN_PEU_FAIBLE: u"Un peu faible",
                 TROP_FAIBLE: u"Trop faible"}
ECHELLE_ACCORD = {PAS_DU_TOUT_D_ACCORD: u"Pas du tout d'accord",
                  PAS_D_ACCORD: u"Pas d'accord",
                  NI_D_ACCORD_NI_PAS_D_ACCORD: u"Ni d'accord ni pas d'accord",
                  D_ACCORD: u"D'accord",
                  TOUT_A_FAIT_D_ACCORD: u"Tout à fait d'accord"}
OUI_NON = {NON: u"Non", OUI: u"Oui"}
NE_SAIT_PAS_ENVIRON = {NE_SAIT_PAS: u"Je ne sais pas", ENVIRON: u"Environ"}

# parameters -------------------------------------------------------------------
TREATMENT = BASELINE
TAUX_CONVERSION = 1
NOMBRE_PERIODES = 0
TAILLE_GROUPES = 0
GROUPES_CHAQUE_PERIODE = False
MONNAIE = u"ecu"
PERIODE_ESSAI = False

# DECISION
DECISION_MIN = 0
DECISION_MAX = 100
DECISION_STEP = 1

