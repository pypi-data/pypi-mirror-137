def validate(request,endpoint):

    print(endpoint+" "+"returned a status code of "+str(request.status_code))

    #add a print to every status suggesting what caused the issue

    if(request.status_code == 200):
        return True
    elif(request.status_code == 400):
        return False
    elif(request.status_code == 401):
        return False
    elif(request.status_code == 404):
        return False
    elif(request.status_code == 500):
        return False
    else:
        return False

def actorRequestBody(key):
    return { "key" : key }

def actorGetBody(key):
    return "?key="+key

def specificActionBody(subject,action):
    return {
        "subject" : subject,
        "action" : action
    }

def messageCreateBody(subject,action,measure,value,date=""):
    
    return {
        "subject" : subject,
        "action" : action,
        "measure" : measure,
        "value" : value,
        "date" : date
    }

def messageQueryGroupBody(subject,action,aggregator,start="",end="",dimension=-2,unit=-2):
    queryString = "?subject="+subject+"&action="+action

    if(start != ""):
        queryString += "&start="+start
    if(end != ""):
        queryString += "&end="+end
    if(dimension > -2 and unit > -2):
        queryString += "&dimension="+str(dimension)+"&unit="+str(unit)
    
    queryString += "&aggregator="+str(aggregator)

    return queryString

def messageQueryBody(subject,action,start="",end="",dimension=-2,unit=-2):

    queryString = "?subject="+subject+"&action="+action

    if(start != ""):
        queryString += "&start="+start
    if(end != ""):
        queryString += "&end="+end
    if(dimension > -2 and unit > -2):
        queryString += "&dimension="+str(dimension)+"&unit="+str(unit)

    return queryString

def roleProperty(name,type):
    return {
        "name":name,
        "type":type
    }

def rolePropertySetValue(name,value):
    return {
        name: value
    }

def roleBody(role, properties):
    body = {
        "role" : role,
    }

    body["properties"] = []

    for i in properties:
        body['properties'].append(i)

    return body

def roleQueryBody(role):
    return "?role="+role

def roleAddActorBody(role,actor,properties):

    body = {
        "role" : role,
        "actor" : actor
    }

    body["properties"] = []

    for i in properties:
        body['properties'].append(i)

    return body