# -*- coding: utf-8 -*-

DRUGS_COLUMNS = ["CIS",
                 "denomination",
                 "galenic_form",
                 "route_of_administration",
                 "clearance_status",
                 "clearance_type",
                 "commercialisation_status",
                 "clearance_date",
                 "bdm_status",
                 "clearance_id",
                 "owners",
                 "enhanced_monitoring"]

FORMS_COLUMNS = ["CIS",
                 "CIP7",
                 "label",
                 "administrative_status",
                 "commercialisation_status",
                 "commercialisation_date",
                 "CIP13",
                 "collectivities_aggreement",
                 "reinbursement_rate",
                 "price",
                 "total_price",
                 "dispensing_fee",  # Je suppose...
                 "description"]

SMR_COLUMNS = ["CIS",
               "dossier_HAS",
               "motif_evaluation",
               "date_avis_commission_transparence",
               "SMR_value",
               "SMR_label"]

ASMR_COLUMNS = ["CIS",
                "dossier_HAS",
                "motif_evaluation",
                "date_avis_commission_transparence",
                "ASMR_value",
                "ASMR_label"]

DRUGS_FORMS_COLUMNS = ['CIS', 'label', 'administrative_status',
                       'commercialisation_status_left', 'commercialisation_date', 'CIP13',
                       'collectivities_aggreement', 'reinbursement_rate', 'price', 'total_price',
                       'dispensing_fee', 'description', 'denomination', 'galenic_form',
                       'route_of_administration', 'clearance_status', 'clearance_type',
                       'commercialisation_status_right', 'clearance_date', 'bdm_status', 'clearance_id', 'owners',
                       'enhanced_monitoring']

DRUGS_FORMS_REORDERED_COLUMNS = ['denomination', 'label', 'galenic_form', 'price',
                                 'reinbursement_rate', 'commercialisation_date', 'clearance_date', 'owners',
                                 'commercialisation_status_left', 'collectivities_aggreement', 'total_price',
                                 'administrative_status', 'dispensing_fee', 'description', 'route_of_administration',
                                 'clearance_status', 'clearance_type', 'commercialisation_status_right', 'bdm_status',
                                 'clearance_id', 'enhanced_monitoring', 'CIS', 'CIP13', ]
