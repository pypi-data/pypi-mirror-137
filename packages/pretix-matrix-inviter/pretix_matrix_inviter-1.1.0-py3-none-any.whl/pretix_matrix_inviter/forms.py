from django import forms
from django.utils.translation import ugettext_lazy as _
from i18nfield.forms import I18nFormField, I18nTextInput
from pretix.base.forms import SettingsForm

from .helpers import matrix_room_info_for_event


class MatrixInviterForm(SettingsForm):
    matrix_inviter_items = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(
            attrs={"class": "scrolling-multiple-choice"}
        ),
        label=_("Ask Matrix ID for"),
        required=True,
        choices=[],
    )
    matrix_inviter_authorization_token = forms.CharField(
        label=_("Authorization token"),
        strip=True,
    )
    matrix_inviter_matrix_server = forms.CharField(
        label=_("Matrix server"),
        strip=True,
    )
    matrix_inviter_hint = I18nFormField(
        widget=I18nTextInput,
        label=_("Help text for the Matrix ID field"),
        required=True,
    )
    matrix_inviter_reason = I18nFormField(
        widget=I18nTextInput,
        label=_("Invitation message"),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["matrix_inviter_items"].choices = [
            (i.pk, i.name) for i in self.obj.items.all()
        ]

        room_info = matrix_room_info_for_event(self.obj)
        if self.obj.settings.matrix_inviter_matrix_room.startswith("!"):
            if room_info["canonical_alias"]:
                room_help_text = _('"{name}" (<code>{canonical_alias}</code>)')
            else:
                room_help_text = _('"{name}"')
        else:
            if room_info["canonical_alias"]:
                room_help_text = _(
                    '"{name}" (<code>{room_id}</code>, main alias: <code>{canonical_alias}</code>)'
                )
            else:
                room_help_text = _('"{name}" (<code>{room_id}</code>)')

        self.fields["matrix_inviter_matrix_room"] = forms.RegexField(
            label=_("Matrix room"),
            regex="(!|#)[^:]+:.+",
            strip=True,
            help_text=(room_help_text.format_map(room_info)),
        )
