# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import shortcuts

from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

# from myicenfire.webapp.external_apis.icenfire_api import IceNFireAPI

from .models import Book
from .serializers import BooksSerializer
# from .external_apis.icenfire_api import icenfire_api
import requests
from collections import OrderedDict
# from datetime import datetime


# Create your views here.

class ExternalAPI(APIView):
    def get(self, request):
        book_name = request.GET["name"]

        if book_name != "" and book_name is not None:

            # defining a params dict for the parameters to be sent to the API
            PARAMS = {'name': book_name}

            # sending get request and saving the response as response object
            r = requests.get(
                url="https://www.anapioficeandfire.com/api/books", params=PARAMS)

            # extracting data in json format
            data = r.json(object_pairs_hook=OrderedDict)

            # filter out unwanted keys in the json response
            unwanted_keys = ['url', 'povCharacters',
                             'mediaType', 'characters']
            for b in data:

                # rename keys as needed
                b["number_of_pages"] = b.pop("numberOfPages")
                b["release_date"] = b.pop("released")

                # remove unwanted keys
                for unwanted_key in unwanted_keys:
                    del b[unwanted_key]

                # mydo = "1996-08-01T00:00:00"
                # mydo = datetime.strptime(mydo, "%Y-%m-%dT%H:%M:%S")
                # mydo = str(mydo.year) + str(mydo.month) + str(mydo.day)

                # slicing the date string
                b['release_date'] = b["release_date"][:10]

                # TODO: use OrderedDict() for maintaing the insertion order of {}
            my_dict = {
                "status_code": 200,
                "status": "success",
                "data": data,
            }

        elif book_name is None or book_name == "":
            my_dict = {
                "status_code": 200,
                "status": "failed",
                "message": "Book Name query param is missing",
            }
        else:
            my_dict = {
                "status_code": 200,
                "status": "failed",
                "message": "Something went wrong",
            }

        res = Response(my_dict)
        return res


class BookList(APIView):
    def get(self, request):

        my_books = Book.objects.all()
        serializer = BooksSerializer(my_books, many=True)

        my_dict = {
            "status_code": 200,
            "status": "success",
            "data": serializer.data,
        }
        res = Response(my_dict)

        return res

    def post(self, request):
        print('post request')

        serializer = BooksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # my_dict = {
        #     "status_code": 200,
        #     "status": "success",
        #     "data": serializer.data,
        # }
        # res = Response(my_dict)
        # return res


#  elif request.method == 'PUT':
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
