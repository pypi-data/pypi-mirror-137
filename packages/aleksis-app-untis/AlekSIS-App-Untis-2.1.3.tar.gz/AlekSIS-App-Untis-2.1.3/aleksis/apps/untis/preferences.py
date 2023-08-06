from django.utils.translation import gettext_lazy as _

from dynamic_preferences.preferences import Section
from dynamic_preferences.types import BooleanPreference

from aleksis.core.registries import site_preferences_registry

untis_mysql = Section("untis_mysql", verbose_name=_("Untis: MySQL"))


@site_preferences_registry.register
class UpdateSubjects(BooleanPreference):
    section = untis_mysql
    name = "update_subjects"
    default = True
    verbose_name = _("Update values of existing subjects")


@site_preferences_registry.register
class UpdatePersonsShortName(BooleanPreference):
    section = untis_mysql
    name = "update_persons_short_name"
    default = False
    verbose_name = _("Update short name of existing persons")


@site_preferences_registry.register
class UpdatePersonsName(BooleanPreference):
    section = untis_mysql
    name = "update_persons_name"
    default = False
    verbose_name = _("Update name of existing persons")


@site_preferences_registry.register
class UpdateGroupsShortName(BooleanPreference):
    section = untis_mysql
    name = "update_groups_short_name"
    default = False
    verbose_name = _("Update short name of existing groups")


@site_preferences_registry.register
class UpdateGroupsName(BooleanPreference):
    section = untis_mysql
    name = "update_groups_name"
    default = False
    verbose_name = _("Update name of existing groups")


@site_preferences_registry.register
class DisambiguateGroupsName(BooleanPreference):
    section = untis_mysql
    name = "disambiguate_groups_name"
    default = True
    verbose_name = _("Disambiguate name of new groups")


@site_preferences_registry.register
class OverwriteGroupOwners(BooleanPreference):
    section = untis_mysql
    name = "overwrite_group_owners"
    verbose_name = _("Overwrite group owners")
    default = True


@site_preferences_registry.register
class UpdateRoomsName(BooleanPreference):
    section = untis_mysql
    name = "update_rooms_name"
    default = True
    verbose_name = _("Update name of existing rooms")


@site_preferences_registry.register
class UpdateSupervisionAreas(BooleanPreference):
    section = untis_mysql
    name = "update_supervision_areas"
    default = True
    verbose_name = _("Update existing supervision areas")


@site_preferences_registry.register
class UseCourseGroups(BooleanPreference):
    section = untis_mysql
    name = "use_course_groups"
    default = True
    verbose_name = _("Use course groups")
    help_text = _(
        "Build or search course groups for every course" " instead of setting classes as groups."
    )


@site_preferences_registry.register
class IgnoreIncompleteSubstitutions(BooleanPreference):
    section = untis_mysql
    name = "ignore_incomplete_substitutions"
    default = True
    verbose_name = _("Ignore incomplete substitutions")
