from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import requests



# Create your views here.
def index(request):

    # Set the request parameters
    url = 'https://dev14710.service-now.com/api/now/table/incident'
    # /ed59d46e0fa03200470d47bce1050e46'

    # Eg. User name="admin", Password="admin" for this code sample.
    user = 'admin8'
    pwd = 'admin8'

    # Set proper headers
    headers = {"Content-Type":"application/json","Accept":"application/json"}

    # Do the HTTP request
    response = requests.get(url, auth=(user, pwd), headers=headers )

    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()

    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    results = data.get("result")
    resultList = []
    size = len(results) - 1
    for n in range(size):
        if ("1" == results[n].get("priority")):
            lv = results[n].get("sys_created_on"); #becuase im too lazy to type the whole thing every time
            numericTime = lv[:4]+lv[5:7]+lv[8:10]+lv[11:13]+lv[14:16]+lv[17:19]
            timeNumber = int(numericTime)
            incident = {
                        'numericTime':      timeNumber,
                        'urgency':          results[n].get('urgency'),
                        'createTime':       results[n].get ("sys_created_on"),
                        'incidentNum':      results[n].get ("number"),
                        'shortDesc':        results[n].get("short_description"),
                        'callerId':         results[n].get("caller_id").get("value"),
                        'respondedTime':    results[n].get("sys_updated_on"),
                        'resolvedTime':     results[n].get("resolved_at"),
                        }
            resultList.append(incident)
    # for n in range (len(resultList)):
    #     print (resultList[n].get("createTime") + ",")
    #     print (resultList[n].get("incidentNum") + ",")
    #     print (resultList[n].get("shortDesc") + ",")
    #     print (resultList[n].get("respondedTime") + ",")
    #     print (resultList[n].get("resolvedTime") + ",")
    #     print ("--")
    resultList = sorted(resultList, key = lambda time: time['numericTime'], reverse= True)
    c = {'title' : "Database", 'resultList' :  resultList,}
    # template = loader.get_template('app/base.html')
    return render (request, 'app/base.html', c)
    # return HttpResponse(template.render(c, request))
    # return HttpResponse ("<h1>wtf</h1>")
