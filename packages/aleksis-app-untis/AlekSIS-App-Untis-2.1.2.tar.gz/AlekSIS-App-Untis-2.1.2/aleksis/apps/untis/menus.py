from django.utils.translation import gettext_lazy as _

MENUS = {
    "DATA_MANAGEMENT_MENU": [
        {
            "name": _("Link subjects to groups (for Untis MySQL import)"),
            "url": "untis_groups_subjects",
            "validators": [
                (
                    "aleksis.core.util.predicates.permission_validator",
                    "untis.assign_subjects_to_groups_rule",
                ),
            ],
        },
    ]
}
