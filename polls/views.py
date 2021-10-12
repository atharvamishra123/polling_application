from django.http import HttpResponse
from django.shortcuts import render
from polls.models import PollQuestion


def all_polls_utils(request):
    all_polls_by_followed = PollQuestion.objects.filter(
        user__in=request.user.get_all_followings()
    )
    return all_polls_by_followed


def all_polls(request, id=-1):
    all_polls = all_polls_utils(request)
    # question = PollQuestion.objects.all()
    context = {
        'pollquestion': all_polls
    }
    if request.method == "POST":
        poll = PollQuestion.objects.get(id=id)
        print(request.POST)
        option = request.POST['poll']
        if option == 'option1':
            poll.option_one_votes += 1
        elif option == 'option2':
            poll.option_two_votes += 1
        elif option == 'option3':
            poll.option_three_votes += 1
        elif option == 'option4':
            poll.option_three_votes += 1
        else:
            return HttpResponse(400, 'Invalid form option')
        poll.save()
        return render(request, 'availablepolls.html', context)
    else:
        return render(request, "availablepolls.html", context)
