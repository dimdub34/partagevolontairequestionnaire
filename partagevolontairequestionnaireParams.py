# -*- coding: utf-8 -*-

FORTE_DIMINUTION = NON = PAS_DU_TOUT_D_ACCORD = TROP_ELEVE = NE_SAIT_PAS = 0
FAIBLE_DIMINUTION = OUI = PAS_D_ACCORD = UN_PEU_ELEVE = ENVIRON = 1
PAS_DE_MODIFICATION = NI_D_ACCORD_NI_PAS_D_ACCORD = OPTIMAL = 2
FAIBLE_AUGMENTATION = D_ACCORD = UN_PEU_FAIBLE = 3
FORTE_AUGMENTATION = TOUT_A_FAIT_D_ACCORD = TROP_FAIBLE = 4

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
ECHELLE_AUGMENTATION = {FORTE_DIMINUTION: u"Oui, forte diminution",
                        FAIBLE_DIMINUTION: u"Oui, faible diminution",
                        PAS_DE_MODIFICATION: u"Non, de pas modification",
                        FAIBLE_AUGMENTATION: u"Oui, faible augmentation",
                        FORTE_AUGMENTATION: u"Oui, forte augmentation"}

