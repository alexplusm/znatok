from django.shortcuts import render, redirect
from django.http import JsonResponse

from accounts.models import Profile
from .models import Comment
import bleach


def load_comments(request):
    if request.method == "GET":
        result = []
        comment = Comment.objects.all()[:3]

        for i in comment:
            result.append({
                'user': i.user.first_name,
               'text': i.comment_text,
               'rating': i.rating,
               'date': i.pub_date,
               'city': i.user.profile.city,
               'avatar': i.user.profile.user_avatar.url
              })

        return JsonResponse({'comments': result}, safe=False)


def add_comments(request):
    if request.method == "POST":
        score = request.POST['score']

        if score == '':
            score = 5
        comment = Comment(user=request.user)
        text = bleach.clean(request.POST['comment-text'])
        comment.comment_text = text
        comment.rating = score
        comment.save()
    return redirect('home')


def get_leaders(request):
    if request.method == "GET" and request.is_ajax():
        leaders = Profile.objects.all()[:3]

        results_leaders = []

        for i in leaders:
            results_leaders.append({
                'user_leader': i.user.first_name,
               'points': i.points,
               'city': i.user.profile.city,
               'avatar': i.user.profile.user_avatar.url
              })
        return JsonResponse({'leaders': results_leaders})


def get_more_comments(request):
    if request.method == "GET" and request.is_ajax():
        comment_num = int(request.GET["number"])
        result = []
        bool = False
        comment = Comment.objects.all()[3 * (comment_num + 1):3 * (comment_num + 1) + 3]

        if len(comment) != 3:
            bool = True

        for i in comment:
            result.append({
                'user': i.user.first_name,
               'text': i.comment_text,
               'rating': i.rating,
               'date': i.pub_date,
               'city': i.user.profile.city,
               'avatar': i.user.profile.user_avatar.url
              })

        return JsonResponse({'more_comments': result, 'bool': bool})
