from django.shortcuts import render
import datetime
now = datetime.datetime.now()
lol = 2022


def lols(now, lol):
    if lol != now:
        print('1')

lols(now, lol)
