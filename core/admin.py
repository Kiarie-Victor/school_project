from django.contrib import admin
from .models import Election, Candidate, Vote, Result
from .forms import CandidateAdminForm


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    form = CandidateAdminForm
    list_display = ('member_full_name', 'faculty', 'election', 'created_at')
    list_filter = ('faculty', 'election')
    search_fields = ('member__firstname', 'member__secondname',
                     'election__title', 'faculty')
    fields = ('faculty', 'year_of_study', 'member', 'election', 'manifesto')

    def member_full_name(self, obj):
        return f"{obj.member.firstname} {obj.member.secondname}"
    member_full_name.short_description = 'Candidate Name'



@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'faculty',
        'year_of_study',
        'start_time',
        'end_time',
    )
    list_filter = (
        'faculty',
        'year_of_study',
        'is_active',
        'start_time',
    )
    search_fields = ('title',)
    ordering = ('-start_time',)

    fieldsets = (
        (None, {
            'fields': ('title', 'faculty', 'year_of_study', 'is_active')
        }),
        ('Time Information', {
            'fields': ('start_time', 'end_time')
        }),
        ('Voting Rules', {
            'fields': ('number_of_winners', 'allowed_candidates')
        }),
        ('Administration', {
            'fields': ('created_by',)
        }),
    )
# admin.site.register(Vote)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = (
        'voter',
        'election',
        'candidate_list',
    )
    list_filter = (
        'election',
        'timestamp',
    )
    search_fields = (
        'voter__reg_no',
        'election__title',
    )
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)

    # Disable adding new Vote instances via admin
    def has_add_permission(self, request):
        return False

    # Disable editing existing Vote instances via admin
    def has_change_permission(self, request, obj=None):
        return False


    def candidate_list(self, obj):
        return ", ".join([str(candidate) for candidate in obj.candidates.all()])
    candidate_list.short_description = 'Candidates Voted'

admin.site.register(Result)
