# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import shortcuts

from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status


from .models import Book
from .serializers import BooksSerializer
import requests
from collections import OrderedDict
import json
from django.db.models import Q
import pathlib
from django.core.exceptions import ObjectDoesNotExist

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

    def filter_books(self, filter_d):

        # iterate thru the filter options entered by user and cascade the query set results repeatedly for each k, v condition in {}
        qs = Book.objects.all()
        query = None
        for key in filter_d:
            val = filter_d[key]
            if query is None:
                query = Q(**{key: val})
            else:
                query = query | Q(**{key: val})
        if query:
            qs = qs.filter(query)

        # for year passed as integer in req.body
        if 'release_date' in filter_d:
            year = filter_d['release_date']
            qs1 = Book.objects.filter(release_date__contains=year)
            # qs1 = Book.objects.filter.contains(release_date__icontains=year)
            # qs1 = Book.release_date.objects.filter(field__icontains=year)

            qs = qs | qs1

        return qs

    def get(self, request):
        rb = request.body
        encoding = 'utf-8'
        rb = rb.decode(encoding)

        if rb == "":
            # req body is empty; so, no filtering; 
            # return either list view or detail view
            # that is, fetch all objects or fetch details about one object
            last_path = str(pathlib.PurePath(request.path).name)

            if last_path == "books":
                # list view
                # return all books from the db
                my_books = Book.objects.all()
                serializer = BooksSerializer(my_books, many=True)

                my_dict = {
                    "status_code": 200,
                    "status": "success",
                    "data": serializer.data,
                }
                return Response(my_dict)
            else:
                # details view
                book_id_to_fetch = int(pathlib.PurePath(request.path).name)
                try:
                    book = Book.objects.get(pk=book_id_to_fetch)
                    fetched_book_name = book.name
                    post_fetch_msg = "The book, " + fetched_book_name + " was fetched successfully"

                    res = {
                        "status_code": 200,
                        "status": "success",
                        "message": post_fetch_msg,
                        "data": BooksSerializer(book).data
                    }

                    res = Response(res)
                    return res
                except ObjectDoesNotExist:
                    res = {
                        "status_code": 200,
                        "status": "failed",
                        "message": "Object does not exist.",
                        "data": []
                    }

                    res = Response(res, status=status.HTTP_204_NO_CONTENT)
                    return res
        else:
            # req body is not empty 
            # so, use filter options 
            # and return books based on filter options by user
            try:
                rb = json.loads(rb)

                my_books = self.filter_books(rb)
                serializer = BooksSerializer(my_books, many=True)

                my_dict = {
                    "status_code": 200,
                    "status": "success",
                    "data": serializer.data,
                }
            except:
                # wrong params user might hav sent
                my_dict = {
                    "status_code": 400,
                    "status": "failure",
                    "message": "bad request. Check your req body!"
                }
        res = Response(my_dict)
        return res

    def post(self, request):
        serializer = BooksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            my_dict = {
                "status_code": 201,
                "status": "success",
                "data": [
                    {
                        "book": serializer.data,
                    }
                ],
            }

            res = Response(my_dict, status=status.HTTP_201_CREATED)
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):

        book_id_to_update = int(pathlib.PurePath(request.path).name)
        try:
            book = Book.objects.get(pk=book_id_to_update)
            updated_book_name = book.name

            serializer = BooksSerializer(
                book, data=request.data,  partial=True)
            if serializer.is_valid():
                serializer.save()
                post_update_msg = "The book, " + updated_book_name + " was updated successfully"
                my_dict = {
                    "status_code": 200,
                    "status": "success",
                    "message": post_update_msg,
                    "data": serializer.data,
                }
                return Response(my_dict)
            else:
                my_dict = {
                    "status_code": 400,
                    "status": "failed",
                    "message": "Check the parameters you've sent.",
                    "data": serializer.errors,
                }
                return Response(my_dict)
        except ObjectDoesNotExist:
            my_dict = {
                "status_code": 200,
                "status": "failed",
                "message": "Object does not exist.",
            }
            return Response(my_dict)

    def delete(self, request, *args, **kwargs):
        book_id_to_delete = int(pathlib.PurePath(request.path).name)
        try:
            book = Book.objects.get(pk=book_id_to_delete)
            deleted_book_name = book.name
            post_delete_msg = "The book, " + deleted_book_name + " was deleted successfully"
            book.delete()

            res = {
                "status_code": 200,
                "status": "success",
                "message": post_delete_msg,
                "data": []
            }

            res = Response(res, status=status.HTTP_204_NO_CONTENT)
            return res
        except ObjectDoesNotExist:
            res = {
                "status_code": 200,
                "status": "failed",
                "message": "Object does not exist.",
                "data": []
            }

            res = Response(res, status=status.HTTP_204_NO_CONTENT)
            return res
