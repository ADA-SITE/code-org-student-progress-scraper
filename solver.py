# -*- coding: utf-8 -*-
"""
Created on Tue Oct 26 21:54:03 2021

@author: nsadili
@maintainer: ayusubov
"""
from asyncio.windows_events import NULL
import os
import sys
from bs4 import BeautifulSoup
import json

DIR = "./progress_files"

progressLabels = None
userData = None
userIdToProgress = {}


def __checkColorCode(code):
    if(code.startswith('#')):
        h = code.lstrip('#')

        if(len(h) == 3):
            h = ''.join([ch + ch for ch in h])

        code = 'rgb(' + \
            ', '.join(tuple(str(int(h[i:i+2], 16)) for i in (0, 2, 4))) + ')'

    return code


def __styleToProgressLabel(attrList):
    # ['border-color:rgb(14, 190, 14)', 'border-style:solid', 'color:#fff', 'background-color:rgb(14, 190, 14)']

    del attrList[1]  # no need for border-style

    key = {}
    for attr in attrList:
        parts = attr.split(':')
        key[parts[0]] = __checkColorCode(parts[1])

    return progressLabels[json.dumps(key)]


def __extractUserDataDashboard(path):
    soup = None

    with open(path, 'r', encoding='utf-8') as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    # container_main = soup.find('div', attrs={'class': 'container main'})
    # New version of the Code.org vermicelli code.
    # It stopped working because of the class name change.
    container_main = soup.find('div', attrs={'class': 'full_container'})

    user_data = json.loads(container_main.find('script').get(
        'data-dashboard').replace('&quot;', '"'))

    with open("user_data.json", 'w') as fp:
        fp.write(json.dumps(user_data))


def __getUserIdUserMapping(path):

    data = None
    with open(path, 'r', encoding='utf-8') as fp:
        data = json.load(fp)

    selected_section = None
    # for sec in data['sections']:
    # Super-duper changes in the new version of the Code.org vermicelli code.
    # for sec in data['section']:
    #     if(sec['name'] == SECTION_NAME):
    #         selected_section = sec
    #         break
    # It stopped working because section now is an object instead of the previous array of objects.
    selected_section = data['section']

    extracted_studs = {}
    for student in selected_section['students']:
        extracted_studs[student['id']] = student

    # print(extracted_studs)

    with open(os.path.join('extracted_students.json'), 'w') as out:
        out.write(json.dumps(extracted_studs))

    return extracted_studs


def __getUserIdToProgressMapping(path):

    soup = None

    with open(path, 'r', encoding='utf-8') as fp:
        soup = BeautifulSoup(fp, 'html.parser')

    content_view = soup.find_all('div', attrs={'class': 'content-view'})

    if(len(content_view) == 0):
        return None

    progress_table = content_view[0].find("table")

    table_body = progress_table.find("tbody")

    rows = table_body.find_all('tr', attrs={'class': 'primary-row'})

    userIdToProgress = {}
    for row in rows:
        user_id = int(row['data-rowkey'].split('.')[0])
        userIdToProgress[user_id] = []

        cells = row.find_all('td')
        for cell in cells:
            content = cell.find('div', attrs={'class': 'cell-content'})
            divs = content.findChildren('div', recursive=False)

            # print(len(divs))
            if(len(divs) == 2):
                userIdToProgress[user_id].append([])
                continue  # CELL WITH VALUE "UNPLUGGED ACTIVITY"

            taskResults = []
            for div in divs:
                divTaskResult = div.find(
                    'div', attrs={'class': 'progress-bubble'})

                if(divTaskResult == None):
                    continue

                style = divTaskResult['style']

                label = __styleToProgressLabel(style.split(';')[-4:])

                taskResults.append(label)
            userIdToProgress[user_id].append(taskResults)

    return userIdToProgress


def __getProgressLabelsRGB(path):

    activity_legends = {}

    activity_legends[json.dumps({
        "border-color": "rgb(198, 202, 205)", "color": "rgb(91, 103, 112)", "background-color": "rgb(254, 254, 254)"})] = ("not started", 0)
    activity_legends[json.dumps({
        "border-color": "rgb(14, 190, 14)", "color": "rgb(91, 103, 112)", "background-color": "rgb(254, 254, 254)"})] = ("in progress", 1)
    activity_legends[json.dumps({
        "border-color": "rgb(14, 190, 14)", "color": "rgb(91, 103, 112)", "background-color": "rgb(159, 212, 159)"})] = ("completed (too many blocks)", 2)
    activity_legends[json.dumps({
        "border-color": "rgb(14, 190, 14)", "color": "rgb(255, 255, 255)", "background-color": "rgb(14, 190, 14)"})] = ("Completed (perfect)", 3)
    activity_legends[json.dumps({
        "border-color": "rgb(118, 101, 160)", "color": "rgb(255, 255, 255)", "background-color": "rgb(118, 101, 160)"})] = ("Assessments / Surveys", 4)

    return activity_legends


def processCodeOrgData():
    print('Processing code.org results...')

    global progressLabels
    progressLabels = __getProgressLabelsRGB(None)

    print('->Processing user progress...')
    global userIdToProgress

    for filename in os.listdir(DIR):
        path = os.path.join(DIR, filename)
        print(f'->Processing progress file: {path}...')
        userIdToProgress.update(__getUserIdToProgressMapping(path))

    print('->Processing user data...')
    print('\t->Extracting script tag from html...')
    __extractUserDataDashboard(os.path.join(DIR, os.listdir(DIR)[0]))

    print('\t->Extracting user data from script tag...')
    global userData
    userData = __getUserIdUserMapping(os.path.join("user_data.json"))

    return userIdToProgress


def generateUserProgressReport():
    userProgress = processCodeOrgData()

    userProgressData = []
    for id in userProgress:
        row = ''
        if(id in userData):
            row = str(id) + ',' + userData[id]['name'] + ','

            ns, ip, ic, c, sur = 0, 0, 0, 0, 0
            for info in userProgress[id]:
                for tup in info:
                    if(tup[1] == 0):
                        ns += 1
                    elif(tup[1] == 1):
                        ip += 1
                    elif(tup[1] == 2):
                        ic += 1
                    elif(tup[1] == 3):
                        c += 1
                    else:
                        sur += 1

            # row += f'Not Started: {ns}, In Progress: {ip}, Incomplete: {ic}, Complete: {c}, Assessment/Survey: {sur}'
            row += f'{ns},{ip},{ic},{c},{sur}'
        else:
            row += f'User id ({id}) is NOT FOUND in the USER data dictionary!'

        userProgressData.append(row)

    #with open('user_progress_report.csv', 'w') as fp:
    # We add encoding so it works with Unicode characters in names
    with open('user_progress_report.csv', 'w', encoding='utf-8') as fp:
        fp.write(
            ',ID,Name,' + 'Not Started,In Progress,Incomplete,Complete,Assessment/Survey' + '\n')
        for i in range(len(userProgressData)):
            fp.write(str(i+1) + ',' + userProgressData[i] + '\n')


if __name__ == "__main__":

    global SECTION_NAME
    # SECTION_NAME = "SITE 1101: Homework 1 (Fall 2022)"
    SECTION_NAME = "".join(sys.argv[1:])

    generateUserProgressReport()

    pass
