import json, sys, re, hashlib, smtplib, base64, urllib, os

from auth import *
from django.http import *
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.core.validators import email_re
from django.db.utils import IntegrityError
from django.utils.http import urlquote_plus

'''
@author: Anant Bhardwaj
@date: Mar 21, 2013

Datahub Web Handler
'''
@login_required
def home(request):
  try:
    user = request.session[kUsername]
    return HttpResponseRedirect('/%s' %(user))
  except KeyError:
    return HttpResponseRedirect('/login')
  except Exception, e:
    return HttpResponse(
        {'error': str(e)},
        mimetype="application/json")

def user(request, username):
  try:
    if(username):
      res = manager.list_repos(username)
      repos = [t[0] for t in res['tuples']]
      return render_to_response("user.html", {
          'username': username,
          'repos': repos})      
  except Exception, e:
    return HttpResponse(
        {'error': str(e)},
        mimetype="application/json")

def repo(request, username, repo):
  try:
    res = manager.list_tables(username, repo)
    tables = [t[0] for t in res['tuples']]
    return render_to_response("repo.html", {
        'username': username,
        'repo': repo,
        'tables': tables})
  except Exception, e:
    return HttpResponse(
        {'error': str(e)},
        mimetype="application/json")

def table(request, username, repo, table):
  try:
    res = manager.execute_sql(
        username=username,
        query='SELECT * from %s.%s.%s' %(username, repo, table))
    column_names = res['column_names']
    tuples = res['tuples']
    return render_to_response("table.html", {
        'username': username,
        'repo': repo,
        'table': table,
        'column_names': column_names,
        'tuples': tuples})
  except Exception, e:
    return HttpResponse(
        {'error': str(e)},
        mimetype="application/json")



