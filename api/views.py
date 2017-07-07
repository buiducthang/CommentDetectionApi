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

import json
import sys
sys.path.append('/home/ducthang/Desktop/Comment/comment/CommentAnal/binhnp/spam_detection/libsvm/python/')
from train import *

@api_view(['GET', 'POST'])
def hello_world(request):
    if request.method == 'POST':
        # print "result"
        # print request.POST.get('_content',"")
        # data = JSONParser().parse(request)
        # serializer = CommentSerializer(data = data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return JsonResponse(serializer.data, status=201)
        comment = request.data
        rs = json.dumps(comment)
        comment = json.loads(rs)
        print comment['comment']
        #print type(comment)
        m = svm_load_model('spam.model')
        vocabs = load_vocabs('vocabs.obj')
        #message = u'fgjghkyhjkdgjdrgjhfgjghk'
        label = predict(m, vocabs, comment['comment'])
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
    return Response({"message": "Hello, world!"})