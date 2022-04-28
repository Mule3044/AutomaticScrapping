#!/usr/bin/env python
from re import findall,sub
from rest_framework.response import Response
import sqlite3
from urllib import response
from django.shortcuts import render

import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse

from rest_framework.decorators import api_view
from lxml import html
import os
import selenium
from selenium import webdriver
import time
from PIL import Image
import io

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

from rest_framework import viewsets, permissions
from .models import google_link_analyzer
from .serialzers import google_link_analyzerSerializer

from datetime import datetime

import urllib
from requests_html import HTML
from requests_html import HTMLSession


def get_source(url):
    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

@api_view(['GET'])
def load_google_link(request):
    formatted_links = []
    query_url =request.GET.get('search_key') 
    user_email =request.GET.get('user_email')
    print(user_email) 
    links = [] # Initiate empty list to capture final results
    if query_url.find("=")> -1:
        query_url = query_url.split('=')[1]

    query = urllib.parse.quote_plus(query_url)
    
    response = get_source("https://www.google.com/search?q=" + query)

    links = list(response.html.absolute_links)
    
    google_domains = ('https://www.google.', 
                      'https://google.', 
                      'https://webcache.googleusercontent.', 
                      'http://webcache.googleusercontent.', 
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.')

    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)
   
    for link in links:
        detail_value = ""
        current_date_time= datetime.now()
        item = {
                    "search_key": query_url,
                    "user":user_email,
                    "status":'Not opened',                        
                    "web_link":link,
                    "details":detail_value,
                    "timestamp": current_date_time

            }
        formatted_links.append(item)

    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()

    for record in formatted_links:
        sqlite_insert_with_param = """INSERT INTO google_link_analyzer
                          (search_key, user, status, details,web_link, timestamp) 
                          VALUES (?, ?, ?, ?, ?, ?);"""

        data_tuple = (record['search_key'], record['user'], record['status'], record['details'],  record['web_link'], record['timestamp'])
        c.execute(sqlite_insert_with_param, data_tuple)
        conn.commit()
    time.sleep(25)#sleep_between_interactions
    return  Response({"message": formatted_links})

@api_view(['GET'])
def update_web_link(request):
    query_url =request.GET.get('url_value') 
    # getting response object
    res = requests.get(query_url)
    # Initialize the object with the document
    soup = BeautifulSoup(res.content, "html.parser")
    # Get the whole body tag
    tag = soup.body
    detail_value = "" 
    # Print each string recursively
    for string in tag.strings:
        detail_value= detail_value +  string 
    detail_value = detail_value.replace('\n', ' ')
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    status = "Opened"
    sqlite_insert_with_param = """Update google_link_analyzer set status = ?, details = ? where web_link = ?"""
    data = (status, detail_value,query_url)
    c.execute(sqlite_insert_with_param, data)
    conn.commit()
    time.sleep(25)#sleep_between_interactions
    return  Response({"message": "Updated"})   

@api_view(['GET'])
def delete_google_link(request):
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    sqlite_insert_with_param = """DELETE From google_link_analyzer;"""
    c.execute(sqlite_insert_with_param)
    conn.commit()
    return Response({"message": "Successfully deleted"})

@api_view(['GET'])
def scrapped_list(request):
    """
    The following list is dynamically scrapped from internet
    """
    if request.method == 'GET':
        snippets = google_link_analyzer.objects.all()
        serializer = google_link_analyzerSerializer(snippets, many=True)
        return Response(serializer.data)


