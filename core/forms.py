from django import forms
from .models import Candidate, Member


class CandidateAdminForm(forms.ModelForm):
    year_of_study = forms.IntegerField(required=False, label="Year of Study")

    class Meta:
        model = Candidate
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['member'].queryset = Member.objects.none()

        if self.instance and self.instance.pk:
            self.fields['member'].queryset = Member.objects.filter(
                faculty=self.instance.faculty,
                year_of_study=self.instance.member.year_of_study
            )
        elif 'faculty' in self.data and 'year_of_study' in self.data:
            faculty = self.data.get('faculty')
            year = self.data.get('year_of_study')
            if faculty and year:
                try:
                    self.fields['member'].queryset = Member.objects.filter(
                        faculty=faculty,
                        year_of_study=int(year)
                    )
                except ValueError:
                    pass

    class Media:
        js = ('admin/js/jquery.init.js', 'js/filter_members.js',)



class VotingForm(forms.Form):
    """
    A form to cast a vote by selecting multiple candidates.
    """
    candidates = forms.ModelMultipleChoiceField(
        # We'll populate this dynamically based on the election
        queryset=Candidate.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        label="Select Candidates"
    )

    def __init__(self, *args, **kwargs):
        # Get the election object to filter candidates
        election = kwargs.pop('election', None)
        super().__init__(*args, **kwargs)

        if election:
            self.fields['candidates'].queryset = Candidate.objects.filter(
                election=election)

