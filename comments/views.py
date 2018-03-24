from django.shortcuts import render
from django.http import JsonResponse


from accounts.models import Profile
from .models import Comment
from .models import CommentForm

import datetime


def load_comments(request):
    if request.method == "GET":
        result, comment_4, comment_3, comment_2, comment_1 = [], [], [], [], []
        comment_5 = Comment.objects.filter(rating=5)[:3]
        for i in comment_5:
            result.append(to_json(i))
        if len(comment_5) < 3:
            comment_4 = Comment.objects.filter(rating=4)[:3-len(comment_5)]
            for k in comment_4:
                result.append(to_json(k))
        if (len(comment_5) + len(comment_4)) < 3:
            comment_3 = Comment.objects.filter(rating=3)[:3-(len(comment_5) + len(comment_4))]
            for j in comment_3:
                result.append(to_json(j))
        return JsonResponse({'comments': result}, safe=False)


# def add_comments(request):
#     if request.method == "POST" and request.is_ajax():
#         comment_form = CommentForm(request.POST)
#         if request.method == 'POST':
#             formset = comment_form
#             if formset.is_valid():
#                 author = formset.save(commit=False)
#                 comment = Comment(user=author.user)
#                 comment.comment_text = author.comment_text
#                 comment.pub_date = datetime.datetime.now()
#                 comment.rating = author.rating
#                 comment.save()
#         else:
#             formset = comment_form
#         return render(request, "add_comment.html", {"formset": formset})


def to_json(comment):
    # {'1 comment': {'user': asd, 'text': asfasd, 'rating': 1/2/3, 'date': asojd},
    # '2 comment': {},
    # '3 comment': {},
    # '4 comment': {},
    # '5 comment': {}}
    results = {'user': comment.user.first_name,
               'text': comment.comment_text,
               'rating': comment.rating,
               'date': comment.pub_date,
               'city': comment.user.profile.city,
               'avatar': comment.user.profile.user_avatar.url
              }
    return results


def to_json_2(leader):
    # {'1 comment': {'user': asd, 'text': asfasd, 'rating': 1/2/3, 'date': asojd},
    # '2 comment': {},
    # '3 comment': {},
    # '4 comment': {},
    # '5 comment': {}}
    results = {'user_leader': leader.user.first_name,
               'points': leader.points,
               'city': leader.user.profile.city,
               'avatar': leader.user.profile.user_avatar.url
              }
    return results


def get_leaders(request):
    if request.method == "GET" and request.is_ajax():
        leaders = Profile.objects.filter()[:3]
        results_leaders = []
        for i in leaders:
            results_leaders.append(to_json_2(i))
        return JsonResponse({'leaders': results_leaders})
