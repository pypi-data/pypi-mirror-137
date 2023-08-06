from django import forms
from django.utils.translation import ugettext_lazy as _
from pretix.base.forms import SettingsForm


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
    matrix_inviter_matrix_room = forms.RegexField(
        label=_("Matrix room"),
        regex="![^:]+:.+",
        strip=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["matrix_inviter_items"].choices = [
            (i.pk, i.name) for i in self.obj.items.all()
        ]
