# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from .models import Comment
from django.http import Http404, JsonResponse

from api.serializers import CommentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import api_view

from rest_framework.parsers import JSONParser
from HTMLParser import HTMLParser
import codecs
import json
import sys
sys.path.append('/home/thuynv/Desktop/CommentDetectionApi/api/binhnp/spam_detection/libsvm/python/')
from train import *
from py4j.java_gateway import JavaGateway

@api_view(['GET', 'POST'])
def hello_world(request):
    if request.method == 'POST':
        comment = request.data
        rs = json.dumps(comment)
        comment = json.loads(rs)
        h = HTMLParser()
        comment = h.unescape(comment['comment'])
        print comment
        m = svm_load_model('spam.model')
        vocabs = load_vocabs('vocabs.obj')
	comment = token(comment)
	print comment
        label = predict(m, vocabs, comment)
        print label
        print type(label)
        print type(request.data)
        if(label[0] == 0.0):
            check = 'showPass'
            print "ok"
        else:
            check = 'showFailed'
            print 'not ok'
        return JsonResponse({"result":label[0]})
    return Response({"result": ""})

#call py4j token
def token(comment):
    print "enter"
    gateway = JavaGateway()
    response = gateway.entry_point.getResponse()
    response.setUETSegmentResponse(comment)
    comment = response.execute()
    return comment

