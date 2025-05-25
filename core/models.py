from django.db import models
from accounts.models import Member

FACULTY_CHOICES = [
    ('CIT', 'CIT'),
    ('BUS', 'Business'),
    ('ENG', 'Engineering'),
    ('FSS', 'Social Sciences'),
    ('MMC', 'Media & Communication'),
    ('FST', 'Science & Technology'),
]


class Election(models.Model):

    faculty = models.CharField(max_length=30, choices=FACULTY_CHOICES)
    year_of_study = models.PositiveIntegerField()
    title = models.CharField(
        max_length=100, help_text="Title of the election, e.g. 'Year 1 CIT Delegates Election'")
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        Member, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'is_staff': True})
    number_of_winners = models.PositiveIntegerField(
        default=3, help_text="Number of winning candidates for this election")
    allowed_candidates = models.PositiveIntegerField(
        default=2,
        help_text="Maximum number of candidates a student can vote for in this election"
    )

    def __str__(self):
        return f"{self.title} ({self.faculty} - Year {self.year_of_study})"

    class Meta:
        unique_together = ('faculty', 'year_of_study', 'start_time')


class Candidate(models.Model):
    faculty = models.CharField(max_length=30, choices=FACULTY_CHOICES)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    election = models.ForeignKey(
        Election, on_delete=models.CASCADE, related_name='candidates')
    manifesto = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('member', 'election')

    def __str__(self):
        return f"{self.member.firstname} {self.member.secondname} - {self.election}"


class Vote(models.Model):

    voter = models.ForeignKey(Member, on_delete=models.CASCADE)
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    candidates = models.ManyToManyField(Candidate, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)


    tx_hash = models.CharField("Transaction Hash", max_length=66, blank=True, null=True)
    block_number = models.PositiveBigIntegerField("Block Number", blank=True, null=True)
    from_address = models.CharField("From Wallet Address", max_length=42, blank=True, null=True)
    to_address = models.CharField("To (Contract) Address", max_length=42, blank=True, null=True)
    gas_used = models.PositiveBigIntegerField("Gas Used", blank=True, null=True)
    tx_status = models.BooleanField("Transaction Successful", blank=True, null=True)

    class Meta:
        unique_together = ('voter', 'election')

    def __str__(self):
        return f"Vote by {self.voter.reg_no} in {self.election.title}"


class Result(models.Model):
    election = models.ForeignKey('Election', on_delete=models.CASCADE)
    candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE)
    total_votes = models.FloatField(default=0.0)
    is_winner = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('election', 'candidate')
        ordering = ['-total_votes']

    def __str__(self):
        return f"{self.candidate.member.firstname} {self.candidate.member.secondname} - {self.total_votes} votes"
