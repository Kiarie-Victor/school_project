import csv
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from blockchain.web3_utils import get_all_votes
from blockchain.web3_utils import send_vote_transaction
from core.forms import VotingForm
from core.models import Election, Candidate, Vote, Result
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils import timezone
from .forms import VotingForm
from .models import Election, Candidate, Vote
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import Election, Vote, Candidate
from datetime import date
from django.contrib.auth.decorators import user_passes_test
from django.db import transaction
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


@login_required
def student_dashboard(request):
    user = request.user

    elections = Election.objects.filter(
        faculty=user.faculty,
        year_of_study=user.year_of_study
    )

    voted_election_ids = Vote.objects.filter(
        voter=user).values_list('election_id', flat=True)

    context = {
        "student": user,
        "elections": elections,
        "voted_election_ids": voted_election_ids
    }

    return render(request, "core/dashboard.html", context)

@login_required
def student_profile(request):
    user = request.user

    return render(request, "core/profile.html", {"student": user})


@login_required
def vote_page(request, election_id):
    election = get_object_or_404(Election, id=election_id)

    # Check if election is currently active
    if not (election.start_time <= timezone.now() <= election.end_time):
        return render(request, 'election_closed.html')

    # Check if user already voted
    if Vote.objects.filter(election=election, voter=request.user).exists():
        return redirect('already_voted', election_id=election.id)

    candidates = Candidate.objects.filter(election=election)
    form = VotingForm(request.POST or None, election=election)

    if request.method == 'POST' and form.is_valid():
        selected_candidates = form.cleaned_data['candidates']

        if len(selected_candidates) > election.allowed_candidates:
            form.add_error(
                'candidates', f"You can only select {election.allowed_candidates} candidates."
            )
        else:
            try:
                print("Attempting to send blockchain vote transaction...")
                print(
                    f"Election ID: {election.id} Candidate IDs: {[c.id for c in selected_candidates]}"
                )

                tx_receipt = send_vote_transaction(
                    election_id=election.id,
                    candidate_ids=[c.id for c in selected_candidates],
                )
                print("Transaction sent. Receipt:", tx_receipt)

                with transaction.atomic():
                    vote = Vote.objects.create(
                        election=election,
                        voter=request.user,
                        tx_hash=tx_receipt.transactionHash.hex(),
                        block_number=tx_receipt.blockNumber,
                        from_address=tx_receipt['from'] if 'from' in tx_receipt else None,
                        to_address=tx_receipt['to'] if 'to' in tx_receipt else None,
                        gas_used=tx_receipt.gasUsed,
                        tx_status=tx_receipt.status == 1,
                    )
                    vote.candidates.set(selected_candidates)
                    vote.save()

                    # Each selected candidate gets 1 full vote (instead of fractional)
                    for candidate in selected_candidates:
                        result, created = Result.objects.get_or_create(
                            election=election,
                            candidate=candidate,
                            defaults={'total_votes': 0.0}
                        )
                        result.total_votes += 1  # <- updated to full 1 vote per candidate
                        result.save()

            except Exception as e:
                print(f"Blockchain TX failed: {e}")
                messages.error(
                    request, f"Blockchain transaction failed: {str(e)}")
                return render(request, 'core/vote_page.html', {
                    'form': form, 'candidates': candidates, 'election': election
                })

            return redirect('thank_you', election_id=election.id)

    # If GET request or invalid form, render the page with form and candidates
    return render(request, 'core/vote_page.html', {
        'form': form, 'candidates': candidates, 'election': election
    })



@login_required
def already_voted(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    vote = get_object_or_404(Vote, election=election, voter=request.user)
    voted_candidates = vote.candidates.all()

    context = {
        "election": election,
        "voted_candidates": voted_candidates,
        "vote": vote  # Include vote to access blockchain fields
    }

    return render(request, "core/already_voted.html", context)



@login_required
def thank_you(request, election_id):
    election = get_object_or_404(Election, id=election_id)
    vote = get_object_or_404(Vote, election=election, voter=request.user)
    voted_candidates = vote.candidates.all()

    context = {
        "election": election,
        "voted_candidates": voted_candidates,
        "vote": vote 
    }

    return render(request, "core/thank_you.html", context)



def custom_404_dev(request, exception=None):
    return render(request, 'core/404.html')


def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)


@superuser_required
def admin_dashboard(request):
    return render(request, 'admin_page')


@login_required
def voting_results(request):
    student = request.user

    # Fetch the election for this student's faculty and year
    election = Election.objects.filter(
        faculty=student.faculty,
        year_of_study=student.year_of_study
    ).first()

    if not election:
        messages.error(
            request, "No elections found for your faculty and year.")
        return redirect('student_dashboard')

    # Get candidates and results for this election
    candidates = Candidate.objects.filter(election=election)
    results = Result.objects.filter(election=election).order_by('-total_votes')

    # Get vote details (optional, to show per candidate when requested)
    votes = Vote.objects.filter(election=election)

    context = {
        'election': election,
        'candidates': candidates,
        'results': results,
        'votes': votes,
        'student': student,
    }

    return render(request, 'core/voting_results.html', context)


@login_required
def vote_details(request, candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)

    votes = Vote.objects.filter(candidates=candidate).order_by('-timestamp')

    context = {
        'candidate': candidate,
        'votes': votes
    }

    return render(request, 'core/vote_details.html', context)


@login_required
def export_votes_csv(request, candidate_id):
    candidate = Candidate.objects.get(id=candidate_id)
    votes = Vote.objects.filter(candidates=candidate)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="votes_{candidate.id}.csv"'

    writer = csv.writer(response)
    writer.writerow(['#', 'Tx Hash', 'From', 'Block Number',
                    'Gas Used', 'Status', 'Timestamp'])

    for index, vote in enumerate(votes, start=1):
        writer.writerow([
            index,
            vote.tx_hash,
            vote.from_address,
            vote.block_number,
            vote.gas_used,
            "Confirmed" if vote.tx_status else "Failed",
            vote.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        ])

    return response

@login_required
def export_votes_pdf(request, candidate_id):
    candidate = Candidate.objects.get(id=candidate_id)
    votes = Vote.objects.filter(candidates=candidate)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="votes_{candidate.id}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    y = height - 50
    p.setFont("Helvetica-Bold", 14)
    p.drawString(
        50, y, f"Vote Records for {candidate.member.firstname} {candidate.member.secondname}")
    y -= 30

    p.setFont("Helvetica", 10)
    headers = ['#', 'Tx Hash', 'From Address',
               'Block', 'Gas', 'Status', 'Timestamp']
    for i, header in enumerate(headers):
        p.drawString(50 + i * 75, y, header)
    y -= 20

    for index, vote in enumerate(votes, start=1):
        if y < 50:  # New page if out of space
            p.showPage()
            y = height - 50

        data = [
            str(index),
            vote.tx_hash[:10] + "..." if vote.tx_hash else "",
            vote.from_address[:10] + "..." if vote.from_address else "",
            str(vote.block_number),
            str(vote.gas_used),
            "Confirmed" if vote.tx_status else "Failed",
            vote.timestamp.strftime("%Y-%m-%d %H:%M")
        ]
        for i, item in enumerate(data):
            p.drawString(50 + i * 75, y, item)
        y -= 20

    p.showPage()
    p.save()
    return response
