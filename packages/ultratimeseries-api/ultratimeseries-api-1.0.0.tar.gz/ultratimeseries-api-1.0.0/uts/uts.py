from uts import httpHandler
from uts import utils

class UTS(object):
    url = ''
    host = ''

    def __init__(self, url='http://localhost:8080',host='localhost'):
        self.url = url
        self.host = host

    class Actors(object):
        actors = []

        def __init__(self):
            self.actors = []
        
        def addActor(self,key):
            self.actors.append(utils.actorRequestBody(key))
        def clearActors(self):
            self.actors = []

    class Messages(object):
        messages = []

        def __init__(self):
            self.messages = []

        def addMessage(self,subject,action,measure,value,date=""):
            self.messages.append(utils.messageCreateBody(subject,action,measure,value,date))

        def clearMessages(self):
            self.messages = []

    class Role(object):

        key = ''
        properties = []

        def __init__(self,key):
            self.key = key

        def addProperties(self,properties):
            for prop in properties:
                self.properties.append(utils.roleProperty(prop[0],prop[1]))

        def clearProperties(self):
            self.properties= []

        def updateKey(self,key):
            self.key = key

    class ActorRole(object):

        roleKey  = ''
        actorKey = ''

        properties = []
        
        def __init__(self,roleKey='',actorKey=''):
            self.roleKey = roleKey
            self.actorKey = actorKey

        def addProperties(self,properties):
            for prop in properties:
                self.properties.append(utils.rolePropertySetValue(prop[0],prop[1]))

        def clearProperties(self):
            self.properties= []

        def updateActorKey(self,actorKey):
            self.actorKey = actorKey

        def updateRoleKey(self,roleKey):
            self.roleKey = roleKey

    #Actor related requests

    def actorCreate(self,actors):
        """
        This function inserts an array of actors in the database

        Args:
            key:    An array of Actor bodies
        Returns:
            A String indicating the result of the operation, an empty String is returned in case of success
        Example:
            >>> actors = actors() \n
            >>> actors.addActor("Cristiano Ronaldo") \n
            >>> #you can add as much messages as your HTTP Post buffer can handle\n
            >>> actorCreate(actors)
        """
        return httpHandler.post(self.url,'/api/actor/create',self.host,actors.actors)

    def actorExists(self,key):
        """
        This function checks if a user exists in the database

        Args:
            key:    Actor's unique identifier
        Returns:
            A String representation of a JSON object indicating the actor's key and the date it was created, "Invalid Request" if the actor doesn't exist
        Example:
            >>> print(actorExists("Cristiano Ronaldo"))\n
            >>> "{ key: "Cristiano Ronaldo", "created":"2021-07-09T16:47:36Z"}"
        """
        return httpHandler.get(self.url,'/api/actor/exist',self.host,utils.actorGetBody(key))

    def actorContains(self,key):
        """
        This function checks if there are Actors that contain a given String in their key

        Args:
            key:    Actor's unique identifier
        Returns:
            A String representation of an array of JSON objects indicating the actor's key and the date it was created, "Invalid Request" if the actor doesn't exist
        Example:
            >>> print(actorContains("Ronaldo"))\n
            >>> "[{ key: "Cristiano Ronaldo", "created":"2021-07-09T16:47:36Z"},{ key: "Ronaldo Nazário", "created":"2021-07-09T16:47:36Z"}]" \n
            >>> \n
            >>> print(actorContains("Cristiano"))\n
            >>> "[{ key: "Cristiano Ronaldo", "created":"2021-07-09T16:47:36Z"}]"
        """
        return httpHandler.get(self.url,'/api/actor/contains',self.host,utils.actorGetBody(key))

    def actorCount(self):
        """
        This function returns the amount of Actors in the database

        Returns:
            An Integer that represents the amount of Actors present in the database
        Example:
            >>> Print(actorCount())\n
            >>> 2
        """
        return int(httpHandler.get(self.url,'/api/actor/count',self.host,""))

    def actorAll(self):
        """
        This function returns a list containing every Actor present in the database

        Returns:
            A String representation of an array of JSON objects indicating the actor's key and the date it was created
        Example:
            >>> print(actorAll())\n
            >>> "[{ key: "Cristiano Ronaldo", "created":"2021-07-09T16:47:36Z"},{ key: "Ronaldo Nazário", "created":"2021-07-09T16:47:36Z"}]"
        """
        return httpHandler.get(self.url,'/api/actor',self.host,"")

    #Message related requests

    def getAllUnits(self):
        """
        This function returns a list with every unit suported by UTS

        Returns:
            A String representation of an array of JSON objects indicating the unit and the respective measure
        Example:
            >>> print(getAllUnits())\n
            >>> "[ ... , {"dimension": {"id": 13,"name": "Length"},"unit": {"id": 183,"name": "Meter"}}, ...]"
        """
        return httpHandler.get(self.url,'/api/units',self.host,"")

    def getAllTimewindows(self):
        """
        This function returns a list with every timewindow suported by UTS

        Returns:
            A String representation of a JSON object indicating the timewindows
        Example:
            >>> print(getAllTimewindows())\n
            >>> {"dayOfWeek":1,"month":3,"year":4,"hour":5}
        """
        return httpHandler.get(self.url,'/api/time-window',self.host,"")

    def messageCreate(self,messages):
        """
        This function inserts an array of messages into the database

        Args:
            messages:    An array of Message bodies
        Returns:
            An empty String in case of success
        Example:
            >>> messages = Messages()\n
            >>> messages.addMessage("Cristiano Ronaldo","Distance covered",LengthMeter(),11587.27,"2021-07-09T16:47:36Z")\n
            >>> #you can add as much messages as your HTTP Post buffer can handle\n
            >>> messageCreate(messages)
        """
        return httpHandler.post(self.url,'/api/messages/create',self.host,messages.messages)

    def getAllMessages(self):
        """
        This function all the existing time series present in the database. A time series is a unique combination of Action and Subject

        Returns:
            A String representation of an array of JSON objects indicating the existing time series
        Example:
            >>> print(getAllMessages())\n
            >>> [{"action": "Distance covered","subject": "Ronaldo Nazário","dimension": "Length","preferedUnit": "Meter","created": "2021-07-09T16:47:36Z"}]
        """
        return httpHandler.get(self.url,'/api/messages/all',self.host,"")

    def getMaxMessage(self,subject,action,start="",end=""):
        """
        This function returns the max value registered for a certain Action, Subject and period

        Args:
            subject:    Actor's unique identifier
            action:    Action's identifier
            start:  the lower end of the time period to be evaluated (optional)
            end:    the upper end of the time period to be evaluated (optional)
        Returns:
            A float
        Example:
            >>> print(getMaxMessage("Cristiano Ronaldo","Distance covered"))\n
            >>> 11587.27
        """
        return float(httpHandler.get(self.url,'/api/messages/max',self.host,utils.messageQueryBody(subject,action,start,end)))

    def getMinMessage(self,subject,action,start="",end=""):
        """
        This function returns the min value registered for a certain Action, Subject and period

        Args:
            subject:    Actor's unique identifier
            action:    Action's identifier
            start:  the lower end of the time period to be evaluated (optional)
            end:    the upper end of the time period to be evaluated (optional)
        Returns:
            A Decimal
        Example:
            >>> print(getMinMessage("Cristiano Ronaldo","Distance covered"))\n
            >>> 11587.27
        """
        return float(httpHandler.get(self.url,'/api/messages/min',self.host,utils.messageQueryBody(subject,action,start,end)))

    def getFirstMessage(self,subject,action,start="",end=""):
        """
        This function returns the first value registered for a certain Action, Subject and period

        Args:
            subject:    Actor's unique identifier
            action:    Action's identifier
            start:  the lower end of the time period to be evaluated (optional)
            end:    the upper end of the time period to be evaluated (optional)
        Returns:
            A String representation of a JSON object
        Example:
            >>> print(getFirstMessage("Cristiano Ronaldo","Distance covered"))\n
            >>> {"date": "2021-07-09T16:47:36Z","value": 11587.27,"created": "2021-07-09T16:47:36Z"}
        """
        return httpHandler.get(self.url,'/api/messages/first',self.host,utils.messageQueryBody(subject,action,start,end))

    def getLastMessage(self,subject,action,start="",end=""):
        """
        This function returns the last value registered for a certain Action, Subject and period

        Args:
            subject:    Actor's unique identifier
            action:    Action's identifier
            start:  the lower end of the time period to be evaluated (optional)
            end:    the upper end of the time period to be evaluated (optional)
        Returns:
            A String representation of a JSON object
        Example:
            >>> print(getLastMessage("Cristiano Ronaldo","Distance covered"))\n
            >>> {"date": "2021-07-09T16:47:36Z","value": 11587.27,"created": "2021-07-09T16:47:36Z"}
        """
        return httpHandler.get(self.url,'/api/messages/last',self.host,utils.messageQueryBody(subject,action,start,end))

    def getMessageCount(self,subject,action,start="",end=""):
        """
        This function returns the amount of messages present in the database for a certain Action, Subject and period

        Args:
            subject:    Actor's unique identifier
            action:    Action's identifier
            start:  the lower end of the time period to be evaluated (optional)
            end:    the upper end of the time period to be evaluated (optional)
        Returns:
            An Integer
        Example:
            >>> print(getMessageCount("Cristiano Ronaldo","Distance covered"))\n
            >>> 1
        """
        return int(httpHandler.get(self.url,'/api/messages/count',self.host,utils.messageQueryBody(subject,action,start,end)))

    def getMessageSum(self,subject,action,start="",end=""):
        """
        This function returns the sum of the values from the messages present in the database for a certain Action, Subject and period

        Args:
            subject:    Actor's unique identifier
            action:    Action's identifier
            start:  the lower end of the time period to be evaluated (optional)
            end:    the upper end of the time period to be evaluated (optional)
        Returns:
            A Decimal
        Example:
            >>> print(getMessageSum("Cristiano Ronaldo","Distance covered"))\n
            >>> 11587.27
        """
        return httpHandler.get(self.url,'/api/messages/sum',self.host,utils.messageQueryBody(subject,action,start,end))

    def getMessageAverage(self,subject,action,start="",end=""):
        """
        This function returns the average value from the messages present in the database for a certain Action, Subject and period

        Args:
            subject:    Actor's unique identifier
            action:    Action's identifier
            start:  the lower end of the time period to be evaluated (optional)
            end:    the upper end of the time period to be evaluated (optional)
        Returns:
            A Decimal
        Example:
            >>> print(getMessageAverage("Cristiano Ronaldo","Distance covered"))\n
            >>> 11587.27
        """
        return httpHandler.get(self.url,'/api/messages/avg',self.host,utils.messageQueryBody(subject,action,start,end))

    def getMessageMedian(self,subject,action,start="",end=""):
        """
        This function returns the median value from the messages present in the database for a certain Action, Subject and period

        Args:
            subject:    Actor's unique identifier
            action:    Action's identifier
            start:  the lower end of the time period to be evaluated (optional)
            end:    the upper end of the time period to be evaluated (optional)
        Returns:
            A Decimal
        Example:
            >>> print(getMessageMedian("Cristiano Ronaldo","Distance covered"))\n
            >>> 11587.27
        """
        return httpHandler.get(self.url,'/api/messages/med',self.host,utils.messageQueryBody(subject,action,start,end))

    def getMessageMode(self,subject,action,start="",end=""):
        """
        This function returns the mode from the messages present in the database for a certain Action, Subject and period

        Args:
            subject:    Actor's unique identifier
            action:    Action's identifier
            start:  the lower end of the time period to be evaluated (optional)
            end:    the upper end of the time period to be evaluated (optional)
        Returns:
            A Decimal
        Example:
            >>> print(getMessageMode("Cristiano Ronaldo","Distance covered"))\n
            >>> 11587.27
        """
        return httpHandler.get(self.url,'/api/messages/mod',self.host,utils.messageQueryBody(subject,action,start,end))

    def getMessageStdDev(self,subject,action,start="",end=""):
        """
        This function returns the standard deviation from the messages present in the database for a certain Action, Subject and period

        Args:
            subject:    Actor's unique identifier
            action:    Action's identifier
            start:  the lower end of the time period to be evaluated (optional)
            end:    the upper end of the time period to be evaluated (optional)
        Returns:
            A Decimal
        Example:
            >>> print(getMessageStdDev("Cristiano Ronaldo","Distance covered"))\n
            >>> 232.36
        """
        return httpHandler.get(self.url,'/api/messages/stddev',self.host,utils.messageQueryBody(subject,action,start,end))

    def getMessageKurtosis(self,subject,action,start="",end=""):
        """
        This function returns the kurtosis from the messages present in the database for a certain Action, Subject and period

        Args:
            subject:    Actor's unique identifier
            action:    Action's identifier
            start:  the lower end of the time period to be evaluated (optional)
            end:    the upper end of the time period to be evaluated (optional)
        Returns:
            A Decimal
        Example:
            >>> print(getMessageKurtosis("Cristiano Ronaldo","Distance covered"))\n
            >>> -0.177515
        """
        return httpHandler.get(self.url,'/api/messages/kurtosis',self.host,utils.messageQueryBody(subject,action,start,end))

    def getMessageSkewness(self,subject,action,start="",end=""):
        """
        This function returns the skewness from the messages present in the database for a certain Action, Subject and period

        Args:
            subject:    Actor's unique identifier
            action:    Action's identifier
            start:  the lower end of the time period to be evaluated (optional)
            end:    the upper end of the time period to be evaluated (optional)
        Returns:
            A Decimal
        Example:
            >>> print(getMessageSkewness("Cristiano Ronaldo","Distance covered"))\n
            >>> -0.404796.
        """
        return httpHandler.get(self.url,'/api/messages/skewness',self.host,utils.messageQueryBody(subject,action,start,end))

    def getMessageCountGroup(self,subject,action,aggregator,start="",end="",dimension=-2,unit=-2):
        return httpHandler.get(self.url,'/api/messages/countgroupby',self.host,utils.messageQueryGroupBody(subject,action,aggregator,start,end,dimension,unit))

    def getMessageSumGroup(self,subject,action,aggregator,start="",end="",dimension=-2,unit=-2):
        return httpHandler.get(self.url,'/api/messages/sumgroupby',self.host,utils.messageQueryGroupBody(subject,action,aggregator,start,end,dimension,unit))

    def getMessageAverageGroup(self,subject,action,aggregator,start="",end="",dimension=-2,unit=-2):
        return httpHandler.get(self.url,'/api/messages/avggroupby',self.host,utils.messageQueryGroupBody(subject,action,aggregator,start,end,dimension,unit))

    def messageQuery(self,subject,action,start="",end="",dimension=-2,unit=-2):
        return httpHandler.get(self.url,'/api/messages',self.host,utils.messageQueryBody(subject,action,start,end,dimension,unit))

    #Role related requests

    def roleCreate(self,role):
        """
        This function inserts a Role into the database

        Args:
            role:    Role's unique identifier
            properties:    An array that stores RolePropertiesBodies for each pretended property
        Returns:
            An empty String in case of success
        Example:
            >>> role = Role("key")\n
            >>> # properties = [[propertyName,propertyType],[...,...],...]\n
            >>> properties = [["Position","text"]]\n
            >>> role.addProperties(properties)\n
            >>> roleCreate(role)
        """
        return httpHandler.post(self.url,'/api/role/create',self.host,utils.roleBody(role.key,role.properties))

    def roleExists(self,role):
        """
        This function returns an existing Role in the database with a given identifier

        Args:
            role:    Role's unique identifier
        Returns:
            A String that represents a JSON object
        Example:
            >>> print(roleExists("Position"))\n
            >>> {"role": "Position","created": "2021-07-09T16:47:36Z","properties": [{"name": "Position","type": "Text"}]}
        """
        return httpHandler.get(self.url,'/api/role/exist',self.host,utils.roleQueryBody(role))

    def roleAll(self):
        """
        This function returns all the existing Roles in the database

        Returns:
            A String that represents an array of JSON object
        Example:
            >>> print(roleAll())\n
            >>> [{"role": "Position","created": "2021-07-09T16:47:36Z"}]
        """
        return httpHandler.get(self.url,'/api/role',self.host,"")

    def roleAddActor(self,actorRole):
        """
        This function returns all the existing Roles in the database

        Args:
            actorRole: an ActorRole object that contains the actor key and role key to be associated and also the pretended properties
        Returns:
            An empty String in case of success
        Example:
            >>> actorRole = ActorRole("Postion","Cristiano Ronaldo")\n
            >>> # properties = [[propertyName,propertyValue],[...,...],...]\n
            >>> properties = [["Position","Strike"]]\n
            >>> actorRole.addProperties(properties)\n
            >>> roleAddActor(actorRole)
        """
        return httpHandler.post(self.url,'/api/role/add',self.host,utils.roleAddActorBody(actorRole.roleKey,actorRole.actorKey,actorRole.properties))

    def actorsByRole(self,role):
        """
        This function returns all the existing Actors in the database associated with a given role

        Args:
            role:    Role's unique identifier
        Returns:
            A String that represents an array of JSON objects
        Example:
            >>> print(actorsByRole("Position"))\n
            >>> [{"key": "Cristiano ronaldo","Position": "Striker"}]
        """
        return httpHandler.get(self.url,'/api/role/actors',self.host,utils.roleQueryBody(role))
    
#Available Measures

def measureBuilder(dimension,unit):
    return {"dimension" : dimension, "unit" : unit}

def AbsorbedDoseGray():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AbsorbedDoseGray())
        >>> {"dimension":0,"unit":0}
    """
    return {"dimension" : 0, "unit" : 0}

def AbsorbedDoseExagray():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AbsorbedDoseExagray())
        >>> {"dimension":0,"unit":1}
    """
    return {"dimension" : 0, "unit" : 1}

def AbsorbedDosePetagray():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AbsorbedDosePetagray())
        >>> {"dimension":0,"unit":2}
    """
    return {"dimension" : 0, "unit" : 2}

def AbsorbedDoseTeragray():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AbsorbedDoseTeragray())
        >>> {"dimension":0,"unit":3}
    """
    return {"dimension" : 0, "unit" : 3}

def AbsorbedDoseGigagray():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AbsorbedDoseGigagray())
        >>> {"dimension":0,"unit":4}
    """
    return {"dimension" : 0, "unit" : 4}

def AbsorbedDoseMegagray():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AbsorbedDoseMegagray())
        >>> {"dimension":0,"unit":5}
    """
    return {"dimension" : 0, "unit" : 5}

def AbsorbedDoseKilogray():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AbsorbedDoseKilogray())
        >>> {"dimension":0,"unit":6}
    """
    return {"dimension" : 0, "unit" : 6}

def AbsorbedDoseHectogray():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AbsorbedDoseHectogray())
        >>> {"dimension":0,"unit":7}
    """
    return {"dimension" : 0, "unit" : 7}

def AbsorbedDoseDekagray():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AbsorbedDoseDekagray())
        >>> {"dimension":0,"unit":8}
    """
    return {"dimension" : 0, "unit" : 8}

def AbsorbedDoseDecigray():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AbsorbedDoseDecigray())
        >>> {"dimension":0,"unit":9}
    """
    return {"dimension" : 0, "unit" : 9}

def AbsorbedDoseCentigray():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AbsorbedDoseCentigray())
        >>> {"dimension":0,"unit":10}
    """
    return {"dimension" : 0, "unit" : 10}

def AbsorbedDoseMilligray():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AbsorbedDoseMilligray())
        >>> {"dimension":0,"unit":11}
    """
    return {"dimension" : 0, "unit" : 11}

def AbsorbedDoseMicrogray():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AbsorbedDoseMicrogray())
        >>> {"dimension":0,"unit":12}
    """
    return {"dimension" : 0, "unit" : 12}

def AbsorbedDoseNanogray():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AbsorbedDoseNanogray())
        >>> {"dimension":0,"unit":13}
    """
    return {"dimension" : 0, "unit" : 13}

def AbsorbedDoseRad():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AbsorbedDoseRad())
        >>> {"dimension":0,"unit":14}
    """
    return {"dimension" : 0, "unit" : 14}

def AbsorbedDoseMillirad():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AbsorbedDoseMillirad())
        >>> {"dimension":0,"unit":15}
    """
    return {"dimension" : 0, "unit" : 15}

def AccelerationMeterPerSecondSquared():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AccelerationMeterPerSecondSquared())
        >>> {"dimension":2,"unit":16}
    """
    return {"dimension" : 2, "unit" : 16}

def AccelerationKilometerPerSecondSquared():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AccelerationKilometerPerSecondSquared())
        >>> {"dimension":2,"unit":17}
    """
    return {"dimension" : 2, "unit" : 17}

def AccelerationCentimeterPerSecondSquared():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AccelerationCentimeterPerSecondSquared())
        >>> {"dimension":2,"unit":18}
    """
    return {"dimension" : 2, "unit" : 18}

def AccelerationMillimeterPerSecondSquared():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AccelerationMillimeterPerSecondSquared())
        >>> {"dimension":2,"unit":19}
    """
    return {"dimension" : 2, "unit" : 19}

def AccelerationYardPerSecondSquared():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AccelerationYardPerSecondSquared())
        >>> {"dimension":2,"unit":20}
    """
    return {"dimension" : 2, "unit" : 20}

def AccelerationMilePerSecondSquared():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AccelerationMilePerSecondSquared())
        >>> {"dimension":2,"unit":21}
    """
    return {"dimension" : 2, "unit" : 21}

def AccelerationFootPerSecondSquared():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AccelerationFootPerSecondSquared())
        >>> {"dimension":2,"unit":22}
    """
    return {"dimension" : 2, "unit" : 22}

def AccelerationInchPerSecondSquared():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AccelerationInchPerSecondSquared())
        >>> {"dimension":2,"unit":23}
    """
    return {"dimension" : 2, "unit" : 23}

def AccelerationGalileo():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AccelerationGalileo())
        >>> {"dimension":2,"unit":24}
    """
    return {"dimension" : 2, "unit" : 24}

def AngularAccelerationRadianSquareSecond():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AngularAccelerationRadianSquareSecond())
        >>> {"dimension":4,"unit":40}
    """
    return {"dimension" : 4, "unit" : 40}

def AngularAccelerationRadianSquareMinute():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AngularAccelerationRadianSquareMinute())
        >>> {"dimension":4,"unit":41}
    """
    return {"dimension" : 4, "unit" : 41}

def AngularAccelerationRevolutionSquareSecond():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AngularAccelerationRevolutionSquareSecond())
        >>> {"dimension":4,"unit":42}
    """
    return {"dimension" : 4, "unit" : 42}

def AngularAccelerationRevolutionSquareMinute():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AngularAccelerationRevolutionSquareMinute())
        >>> {"dimension":4,"unit":43}
    """
    return {"dimension" : 4, "unit" : 43}

def AngularAccelerationRevolutionsPerMinutePerSecond():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AngularAccelerationRevolutionsPerMinutePerSecond())
        >>> {"dimension":4,"unit":44}
    """
    return {"dimension" : 4, "unit" : 44}

def AngularVelocityRadianPerSecond():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AngularVelocityRadianPerSecond())
        >>> {"dimension":5,"unit":46}
    """
    return {"dimension" : 5, "unit" : 46}

def AngularVelocityRadianPerMinute():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AngularVelocityRadianPerMinute())
        >>> {"dimension":5,"unit":47}
    """
    return {"dimension" : 5, "unit" : 47}

def AngularVelocityRevolutionPerSecond():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AngularVelocityRevolutionPerSecond())
        >>> {"dimension":5,"unit":48}
    """
    return {"dimension" : 5, "unit" : 48}

def AngularVelocityRevolutionPerMinute():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AngularVelocityRevolutionPerMinute())
        >>> {"dimension":5,"unit":49}
    """
    return {"dimension" : 5, "unit" : 49}

def AreaSquareMeter():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AreaSquareMeter())
        >>> {"dimension":6,"unit":50}
    """
    return {"dimension" : 6, "unit" : 50}

def AreaSquareCentimeter():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AreaSquareCentimeter())
        >>> {"dimension":6,"unit":51}
    """
    return {"dimension" : 6, "unit" : 51}

def AreaSquareKilometer():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AreaSquareKilometer())
        >>> {"dimension":6,"unit":52}
    """
    return {"dimension" : 6, "unit" : 52}

def AreaSquareMile():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AreaSquareMile())
        >>> {"dimension":6,"unit":53}
    """
    return {"dimension" : 6, "unit" : 53}

def AreaSquareYard():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AreaSquareYard())
        >>> {"dimension":6,"unit":54}
    """
    return {"dimension" : 6, "unit" : 54}

def AreaSquareFoot():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AreaSquareFoot())
        >>> {"dimension":6,"unit":55}
    """
    return {"dimension" : 6, "unit" : 55}

def AreaSquareInch():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AreaSquareInch())
        >>> {"dimension":6,"unit":56}
    """
    return {"dimension" : 6, "unit" : 56}

def AreaHectare():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AreaHectare())
        >>> {"dimension":6,"unit":57}
    """
    return {"dimension" : 6, "unit" : 57}

def AreaAcre():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(AreaAcre())
        >>> {"dimension":6,"unit":58}
    """
    return {"dimension" : 6, "unit" : 58}

def CurrencyMoney():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(CurrencyMoney())
        >>> {"dimension":29,"unit":89}
    """
    return {"dimension" : 29, "unit" : 89}

def CurrencyEuro():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(CurrencyEuro())
        >>> {"dimension":29,"unit":90}
    """
    return {"dimension" : 29, "unit" : 90}

def CurrencyDollar():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(CurrencyDollar())
        >>> {"dimension":29,"unit":91}
    """
    return {"dimension" : 29, "unit" : 91}

def CurrencyCents():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(CurrencyCents())
        >>> {"dimension":29,"unit":92}
    """
    return {"dimension" : 29, "unit" : 92}

def CurrentAmpere():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(CurrentAmpere())
        >>> {"dimension":7,"unit":93}
    """
    return {"dimension" : 7, "unit" : 93}

def CurrentKiloampere():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(CurrentKiloampere())
        >>> {"dimension":7,"unit":94}
    """
    return {"dimension" : 7, "unit" : 94}

def CurrentMilliampere():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(CurrentMilliampere())
        >>> {"dimension":7,"unit":95}
    """
    return {"dimension" : 7, "unit" : 95}

def CurrentBiot():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(CurrentBiot())
        >>> {"dimension":7,"unit":96}
    """
    return {"dimension" : 7, "unit" : 96}

def CurrentAbampere():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(CurrentAbampere())
        >>> {"dimension":7,"unit":97}
    """
    return {"dimension" : 7, "unit" : 97}

def CustomCustom():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(CustomCustom())
        >>> {"dimension":1,"unit":98}
    """
    return {"dimension" : 1, "unit" : 98}

def ElectricPotentialVolt():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(ElectricPotentialVolt())
        >>> {"dimension":26,"unit":139}
    """
    return {"dimension" : 26, "unit" : 139}

def ElectricPotentialWattAmpere():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(ElectricPotentialWattAmpere())
        >>> {"dimension":26,"unit":140}
    """
    return {"dimension" : 26, "unit" : 140}

def ElectricPotentialAbVolt():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(ElectricPotentialAbVolt())
        >>> {"dimension":26,"unit":141}
    """
    return {"dimension" : 26, "unit" : 141}

def ElectricPotentialEmuOfElectricPotential():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(ElectricPotentialEmuOfElectricPotential())
        >>> {"dimension":26,"unit":142}
    """
    return {"dimension" : 26, "unit" : 142}

def EnergyJoule():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(EnergyJoule())
        >>> {"dimension":9,"unit":143}
    """
    return {"dimension" : 9, "unit" : 143}

def EnergyKilojoule():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(EnergyKilojoule())
        >>> {"dimension":9,"unit":144}
    """
    return {"dimension" : 9, "unit" : 144}

def EnergyCalorie():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(EnergyCalorie())
        >>> {"dimension":9,"unit":145}
    """
    return {"dimension" : 9, "unit" : 145}

def EnergyKilocalorie():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(EnergyKilocalorie())
        >>> {"dimension":9,"unit":146}
    """
    return {"dimension" : 9, "unit" : 146}

def EnergyWattHour():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(EnergyWattHour())
        >>> {"dimension":9,"unit":147}
    """
    return {"dimension" : 9, "unit" : 147}

def EnergyKilowattHour():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(EnergyKilowattHour())
        >>> {"dimension":9,"unit":148}
    """
    return {"dimension" : 9, "unit" : 148}

def EnergyElectronvolt():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(EnergyElectronvolt())
        >>> {"dimension":9,"unit":149}
    """
    return {"dimension" : 9, "unit" : 149}

def EnergyBtu():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(EnergyBtu())
        >>> {"dimension":9,"unit":150}
    """
    return {"dimension" : 9, "unit" : 150}

def EnergyTherm():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(EnergyTherm())
        >>> {"dimension":9,"unit":151}
    """
    return {"dimension" : 9, "unit" : 151}

def EnergyErgs():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(EnergyErgs())
        >>> {"dimension":9,"unit":152}
    """
    return {"dimension" : 9, "unit" : 152}

def ForceNewton():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(ForceNewton())
        >>> {"dimension":10,"unit":153}
    """
    return {"dimension" : 10, "unit" : 153}

def ForceMicronewton():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(ForceMicronewton())
        >>> {"dimension":10,"unit":154}
    """
    return {"dimension" : 10, "unit" : 154}

def ForceMillinewton():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(ForceMillinewton())
        >>> {"dimension":10,"unit":155}
    """
    return {"dimension" : 10, "unit" : 155}

def ForceKilonewton():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(ForceKilonewton())
        >>> {"dimension":10,"unit":156}
    """
    return {"dimension" : 10, "unit" : 156}

def ForceFemtonewton():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(ForceFemtonewton())
        >>> {"dimension":10,"unit":157}
    """
    return {"dimension" : 10, "unit" : 157}

def ForceGramForce():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(ForceGramForce())
        >>> {"dimension":10,"unit":158}
    """
    return {"dimension" : 10, "unit" : 158}

def ForceKilogramForce():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(ForceKilogramForce())
        >>> {"dimension":10,"unit":159}
    """
    return {"dimension" : 10, "unit" : 159}

def ForceTonForce():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(ForceTonForce())
        >>> {"dimension":10,"unit":160}
    """
    return {"dimension" : 10, "unit" : 160}

def ForceDyne():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(ForceDyne())
        >>> {"dimension":10,"unit":161}
    """
    return {"dimension" : 10, "unit" : 161}

def ForceJouleMeter():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(ForceJouleMeter())
        >>> {"dimension":10,"unit":162}
    """
    return {"dimension" : 10, "unit" : 162}

def ForceJouleCentimeter():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(ForceJouleCentimeter())
        >>> {"dimension":10,"unit":163}
    """
    return {"dimension" : 10, "unit" : 163}

def ForcePoundForce():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(ForcePoundForce())
        >>> {"dimension":10,"unit":164}
    """
    return {"dimension" : 10, "unit" : 164}

def ForceOunceForce():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(ForceOunceForce())
        >>> {"dimension":10,"unit":165}
    """
    return {"dimension" : 10, "unit" : 165}

def FrequencyHertz():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(FrequencyHertz())
        >>> {"dimension":11,"unit":166}
    """
    return {"dimension" : 11, "unit" : 166}

def FrequencyKilohertz():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(FrequencyKilohertz())
        >>> {"dimension":11,"unit":167}
    """
    return {"dimension" : 11, "unit" : 167}

def FrequencyMegahertz():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(FrequencyMegahertz())
        >>> {"dimension":11,"unit":168}
    """
    return {"dimension" : 11, "unit" : 168}

def FrequencyGigahertz():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(FrequencyGigahertz())
        >>> {"dimension":11,"unit":169}
    """
    return {"dimension" : 11, "unit" : 169}

def JerkMetersPerCubicSecond():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(JerkMetersPerCubicSecond())
        >>> {"dimension":12,"unit":178}
    """
    return {"dimension" : 12, "unit" : 178}

def JerkKilometersPerCubicSecond():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(JerkKilometersPerCubicSecond())
        >>> {"dimension":12,"unit":179}
    """
    return {"dimension" : 12, "unit" : 179}

def JerkYardsPerCubicSecond():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(JerkYardsPerCubicSecond())
        >>> {"dimension":12,"unit":180}
    """
    return {"dimension" : 12, "unit" : 180}

def JerkMilesPerCubicSecond():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(JerkMilesPerCubicSecond())
        >>> {"dimension":12,"unit":181}
    """
    return {"dimension" : 12, "unit" : 181}

def LengthMeter():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(LengthMeter())
        >>> {"dimension":13,"unit":183}
    """
    return {"dimension" : 13, "unit" : 183}

def LengthKilometer():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(LengthKilometer())
        >>> {"dimension":13,"unit":184}
    """
    return {"dimension" : 13, "unit" : 184}

def LengthCentimeter():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(LengthCentimeter())
        >>> {"dimension":13,"unit":185}
    """
    return {"dimension" : 13, "unit" : 185}

def LengthMillimeter():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(LengthMillimeter())
        >>> {"dimension":13,"unit":186}
    """
    return {"dimension" : 13, "unit" : 186}

def LengthMicrometer():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(LengthMicrometer())
        >>> {"dimension":13,"unit":187}
    """
    return {"dimension" : 13, "unit" : 187}

def LengthNanometer():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(LengthNanometer())
        >>> {"dimension":13,"unit":188}
    """
    return {"dimension" : 13, "unit" : 188}

def LengthMile():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(LengthMile())
        >>> {"dimension":13,"unit":189}
    """
    return {"dimension" : 13, "unit" : 189}

def LengthYard():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(LengthYard())
        >>> {"dimension":13,"unit":190}
    """
    return {"dimension" : 13, "unit" : 190}

def LengthFoot():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(LengthFoot())
        >>> {"dimension":13,"unit":191}
    """
    return {"dimension" : 13, "unit" : 191}

def LengthInch():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(LengthInch())
        >>> {"dimension":13,"unit":192}
    """
    return {"dimension" : 13, "unit" : 192}

def LengthNauticalMile():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(LengthNauticalMile())
        >>> {"dimension":13,"unit":193}
    """
    return {"dimension" : 13, "unit" : 193}

def MassKilogram():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(MassKilogram())
        >>> {"dimension":8,"unit":203}
    """
    return {"dimension" : 8, "unit" : 203}

def MassMetricTon():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(MassMetricTon())
        >>> {"dimension":8,"unit":204}
    """
    return {"dimension" : 8, "unit" : 204}

def MassGram():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(MassGram())
        >>> {"dimension":8,"unit":205}
    """
    return {"dimension" : 8, "unit" : 205}

def MassMilligram():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(MassMilligram())
        >>> {"dimension":8,"unit":206}
    """
    return {"dimension" : 8, "unit" : 206}

def MassMicrogram():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(MassMicrogram())
        >>> {"dimension":8,"unit":207}
    """
    return {"dimension" : 8, "unit" : 207}

def MassImperialTon():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(MassImperialTon())
        >>> {"dimension":8,"unit":208}
    """
    return {"dimension" : 8, "unit" : 208}

def MassUsTon():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(MassUsTon())
        >>> {"dimension":8,"unit":209}
    """
    return {"dimension" : 8, "unit" : 209}

def MassImperialStone():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(MassImperialStone())
        >>> {"dimension":8,"unit":210}
    """
    return {"dimension" : 8, "unit" : 210}

def MassPound():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(MassPound())
        >>> {"dimension":8,"unit":211}
    """
    return {"dimension" : 8, "unit" : 211}

def MassOunce():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(MassOunce())
        >>> {"dimension":8,"unit":212}
    """
    return {"dimension" : 8, "unit" : 212}

def MassDensityKilogramPerCubicMeter():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(MassDensityKilogramPerCubicMeter())
        >>> {"dimension":8,"unit":213}
    """
    return {"dimension" : 8, "unit" : 213}

def MassDensityKilogramPerLiter():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(MassDensityKilogramPerLiter())
        >>> {"dimension":8,"unit":214}
    """
    return {"dimension" : 8, "unit" : 214}

def MassDensityGramsPerLiter():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(MassDensityGramsPerLiter())
        >>> {"dimension":8,"unit":215}
    """
    return {"dimension" : 8, "unit" : 215}

def MassDensityGramsPerMilliLiter():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(MassDensityGramsPerMilliLiter())
        >>> {"dimension":8,"unit":216}
    """
    return {"dimension" : 8, "unit" : 216}

def MassDensityGramsPerCubicCentimeter():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(MassDensityGramsPerCubicCentimeter())
        >>> {"dimension":8,"unit":217}
    """
    return {"dimension" : 8, "unit" : 217}

def MassFlowRateKilogramPerSecond():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(MassFlowRateKilogramPerSecond())
        >>> {"dimension":15,"unit":218}
    """
    return {"dimension" : 15, "unit" : 218}

def MassFlowRateGramsPerSecond():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(MassFlowRateGramsPerSecond())
        >>> {"dimension":15,"unit":219}
    """
    return {"dimension" : 15, "unit" : 219}

def MassFlowRateKilogramPerMinute():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(MassFlowRateKilogramPerMinute())
        >>> {"dimension":15,"unit":220}
    """
    return {"dimension" : 15, "unit" : 220}

def MassFlowRateKilogramPerHour():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(MassFlowRateKilogramPerHour())
        >>> {"dimension":15,"unit":221}
    """
    return {"dimension" : 15, "unit" : 221}

def MassFlowRatePoundsPerSeconds():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(MassFlowRatePoundsPerSeconds())
        >>> {"dimension":15,"unit":222}
    """
    return {"dimension" : 15, "unit" : 222}

def MomentumKilogramPerMetersSecond():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(MomentumKilogramPerMetersSecond())
        >>> {"dimension":16,"unit":224}
    """
    return {"dimension" : 16, "unit" : 224}

def MomentumGramsPerCentimetersSecond():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(MomentumGramsPerCentimetersSecond())
        >>> {"dimension":16,"unit":225}
    """
    return {"dimension" : 16, "unit" : 225}

def MomentumKilogramPerMetersMinute():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(MomentumKilogramPerMetersMinute())
        >>> {"dimension":16,"unit":226}
    """
    return {"dimension" : 16, "unit" : 226}

def MomentumKilogramPerKilometersHour():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(MomentumKilogramPerKilometersHour())
        >>> {"dimension":16,"unit":227}
    """
    return {"dimension" : 16, "unit" : 227}

def MomentumPoundsPerMilesHour():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(MomentumPoundsPerMilesHour())
        >>> {"dimension":16,"unit":228}
    """
    return {"dimension" : 16, "unit" : 228}

def NumericEmpty():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(NumericEmpty())
        >>> {"dimension":17,"unit":229}
    """
    return {"dimension" : 17, "unit" : 229}

def NumericNumber():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(NumericNumber())
        >>> {"dimension":17,"unit":230}
    """
    return {"dimension" : 17, "unit" : 230}

def NumericPercentage():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(NumericPercentage())
        >>> {"dimension":17,"unit":231}
    """
    return {"dimension" : 17, "unit" : 231}

def PlaneAngleRadian():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(PlaneAngleRadian())
        >>> {"dimension":3,"unit":234}
    """
    return {"dimension" : 3, "unit" : 234}

def PlaneAngleDegree():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(PlaneAngleDegree())
        >>> {"dimension":3,"unit":235}
    """
    return {"dimension" : 3, "unit" : 235}

def PlaneAngleGradian():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(PlaneAngleGradian())
        >>> {"dimension":3,"unit":236}
    """
    return {"dimension" : 3, "unit" : 236}

def PlaneAngleMinute():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(PlaneAngleMinute())
        >>> {"dimension":3,"unit":237}
    """
    return {"dimension" : 3, "unit" : 237}

def PlaneAngleSecond():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(PlaneAngleSecond())
        >>> {"dimension":3,"unit":238}
    """
    return {"dimension" : 3, "unit" : 238}

def PlaneAngleRevolution():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(PlaneAngleRevolution())
        >>> {"dimension":3,"unit":239}
    """
    return {"dimension" : 3, "unit" : 239}

def PowerWatt():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(PowerWatt())
        >>> {"dimension":18,"unit":240}
    """
    return {"dimension" : 18, "unit" : 240}

def PowerKilowatts():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(PowerKilowatts())
        >>> {"dimension":18,"unit":241}
    """
    return {"dimension" : 18, "unit" : 241}

def PowerMegawatts():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(PowerMegawatts())
        >>> {"dimension":18,"unit":242}
    """
    return {"dimension" : 18, "unit" : 242}

def PowerNewtonMetersPerSecond():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(PowerNewtonMetersPerSecond())
        >>> {"dimension":18,"unit":243}
    """
    return {"dimension" : 18, "unit" : 243}

def PowerCaloriesPerHour():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(PowerCaloriesPerHour())
        >>> {"dimension":18,"unit":244}
    """
    return {"dimension" : 18, "unit" : 244}

def PowerCaloriesPerMinute():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(PowerCaloriesPerMinute())
        >>> {"dimension":18,"unit":245}
    """
    return {"dimension" : 18, "unit" : 245}

def PowerCaloriesPerSecond():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(PowerCaloriesPerSecond())
        >>> {"dimension":18,"unit":246}
    """
    return {"dimension" : 18, "unit" : 246}

def PowerJoulesPerHour():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(PowerJoulesPerHour())
        >>> {"dimension":18,"unit":247}
    """
    return {"dimension" : 18, "unit" : 247}

def PowerJoulesPerMinute():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(PowerJoulesPerMinute())
        >>> {"dimension":18,"unit":248}
    """
    return {"dimension" : 18, "unit" : 248}

def PowerJoulesPerSecond():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(PowerJoulesPerSecond())
        >>> {"dimension":18,"unit":249}
    """
    return {"dimension" : 18, "unit" : 249}

def PowerHorsepower():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(PowerHorsepower())
        >>> {"dimension":18,"unit":250}
    """
    return {"dimension" : 18, "unit" : 250}

def PowerErgPerSecond():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(PowerErgPerSecond())
        >>> {"dimension":18,"unit":251}
    """
    return {"dimension" : 18, "unit" : 251}

def PressurePascals():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(PressurePascals())
        >>> {"dimension":19,"unit":252}
    """
    return {"dimension" : 19, "unit" : 252}

def PressureBar():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(PressureBar())
        >>> {"dimension":19,"unit":253}
    """
    return {"dimension" : 19, "unit" : 253}

def PressureAtmosphere():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(PressureAtmosphere())
        >>> {"dimension":19,"unit":254}
    """
    return {"dimension" : 19, "unit" : 254}

def PressureKilopascal():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(PressureKilopascal())
        >>> {"dimension":19,"unit":255}
    """
    return {"dimension" : 19, "unit" : 255}

def PressureHectopascal():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(PressureHectopascal())
        >>> {"dimension":19,"unit":256}
    """
    return {"dimension" : 19, "unit" : 256}

def PressurePsi():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(PressurePsi())
        >>> {"dimension":19,"unit":257}
    """
    return {"dimension" : 19, "unit" : 257}

def PressureKsi():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(PressureKsi())
        >>> {"dimension":19,"unit":258}
    """
    return {"dimension" : 19, "unit" : 258}

def PressureKilogramForcePerSquareMeter():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(PressureKilogramForcePerSquareMeter())
        >>> {"dimension":19,"unit":259}
    """
    return {"dimension" : 19, "unit" : 259}

def PressureTorr():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(PressureTorr())
        >>> {"dimension":19,"unit":260}
    """
    return {"dimension" : 19, "unit" : 260}

def SpeedMetersPerSecond():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(SpeedMetersPerSecond())
        >>> {"dimension":22,"unit":268}
    """
    return {"dimension" : 22, "unit" : 268}

def SpeedMilesPerHour():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(SpeedMilesPerHour())
        >>> {"dimension":22,"unit":269}
    """
    return {"dimension" : 22, "unit" : 269}

def SpeedFootPerSecond():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(SpeedFootPerSecond())
        >>> {"dimension":22,"unit":270}
    """
    return {"dimension" : 22, "unit" : 270}

def SpeedKilometersPerHour():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(SpeedKilometersPerHour())
        >>> {"dimension":22,"unit":271}
    """
    return {"dimension" : 22, "unit" : 271}

def SpeedKnot():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(SpeedKnot())
        >>> {"dimension":22,"unit":272}
    """
    return {"dimension" : 22, "unit" : 272}

def SpeedCentimeterPerSecond():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(SpeedCentimeterPerSecond())
        >>> {"dimension":22,"unit":273}
    """
    return {"dimension" : 22, "unit" : 273}

def TemperatureKelvin():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(TemperatureKelvin())
        >>> {"dimension":23,"unit":275}
    """
    return {"dimension" : 23, "unit" : 275}

def TemperatureCelsius():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(TemperatureCelsius())
        >>> {"dimension":23,"unit":276}
    """
    return {"dimension" : 23, "unit" : 276}

def TemperatureFahrenheit():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(TemperatureFahrenheit())
        >>> {"dimension":23,"unit":277}
    """
    return {"dimension" : 23, "unit" : 277}

def TemperatureRankine():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(TemperatureRankine())
        >>> {"dimension":23,"unit":278}
    """
    return {"dimension" : 23, "unit" : 278}

def TimeHour():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(TimeHour())
        >>> {"dimension":24,"unit":279}
    """
    return {"dimension" : 24, "unit" : 279}

def TimeNanoseconds():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(TimeNanoseconds())
        >>> {"dimension":24,"unit":280}
    """
    return {"dimension" : 24, "unit" : 280}

def TimeMicroseconds():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(TimeMicroseconds())
        >>> {"dimension":24,"unit":281}
    """
    return {"dimension" : 24, "unit" : 281}

def TimeMilliseconds():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(TimeMilliseconds())
        >>> {"dimension":24,"unit":282}
    """
    return {"dimension" : 24, "unit" : 282}

def TimeDay():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(TimeDay())
        >>> {"dimension":24,"unit":283}
    """
    return {"dimension" : 24, "unit" : 283}

def TimeWeek():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(TimeWeek())
        >>> {"dimension":24,"unit":284}
    """
    return {"dimension" : 24, "unit" : 284}

def TimeMonth():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(TimeMonth())
        >>> {"dimension":24,"unit":285}
    """
    return {"dimension" : 24, "unit" : 285}

def TimeYear():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(TimeYear())
        >>> {"dimension":24,"unit":286}
    """
    return {"dimension" : 24, "unit" : 286}

def TimeDecade():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(TimeDecade())
        >>> {"dimension":24,"unit":287}
    """
    return {"dimension" : 24, "unit" : 287}

def TimeCentury():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(TimeCentury())
        >>> {"dimension":24,"unit":288}
    """
    return {"dimension" : 24, "unit" : 288}

def TorqueNewtonMeter():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(TorqueNewtonMeter())
        >>> {"dimension":25,"unit":289}
    """
    return {"dimension" : 25, "unit" : 289}

def TorqueKilogramForcePerMeter():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(TorqueKilogramForcePerMeter())
        >>> {"dimension":25,"unit":290}
    """
    return {"dimension" : 25, "unit" : 290}

def TorquePoundForceFoot():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(TorquePoundForceFoot())
        >>> {"dimension":25,"unit":291}
    """
    return {"dimension" : 25, "unit" : 291}

def VolumeCubicMeter():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(VolumeCubicMeter())
        >>> {"dimension":27,"unit":292}
    """
    return {"dimension" : 27, "unit" : 292}

def VolumeCubicKilometer():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(VolumeCubicKilometer())
        >>> {"dimension":27,"unit":293}
    """
    return {"dimension" : 27, "unit" : 293}

def VolumeCubicCentimeter():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(VolumeCubicCentimeter())
        >>> {"dimension":27,"unit":294}
    """
    return {"dimension" : 27, "unit" : 294}

def VolumeCubicMillimeter():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(VolumeCubicMillimeter())
        >>> {"dimension":27,"unit":295}
    """
    return {"dimension" : 27, "unit" : 295}

def VolumeLiter():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(VolumeLiter())
        >>> {"dimension":27,"unit":296}
    """
    return {"dimension" : 27, "unit" : 296}

def VolumeMilliLiter():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(VolumeMilliLiter())
        >>> {"dimension":27,"unit":297}
    """
    return {"dimension" : 27, "unit" : 297}

def VolumeGallon():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(VolumeGallon())
        >>> {"dimension":27,"unit":298}
    """
    return {"dimension" : 27, "unit" : 298}

def VolumeQuart():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(VolumeQuart())
        >>> {"dimension":27,"unit":299}
    """
    return {"dimension" : 27, "unit" : 299}

def VolumePint():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(VolumePint())
        >>> {"dimension":27,"unit":300}
    """
    return {"dimension" : 27, "unit" : 300}

def VolumeCup():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(VolumeCup())
        >>> {"dimension":27,"unit":301}
    """
    return {"dimension" : 27, "unit" : 301}

def VolumeTablespoon():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(VolumeTablespoon())
        >>> {"dimension":27,"unit":302}
    """
    return {"dimension" : 27, "unit" : 302}

def VolumeTeaspoon():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(VolumeTeaspoon())
        >>> {"dimension":27,"unit":303}
    """
    return {"dimension" : 27, "unit" : 303}

def VolumeCubicFoot():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(VolumeCubicFoot())
        >>> {"dimension":27,"unit":304}
    """
    return {"dimension" : 27, "unit" : 304}

def VolumeCubicInch():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(VolumeCubicInch())
        >>> {"dimension":27,"unit":305}
    """
    return {"dimension" : 27, "unit" : 305}

def VolumetricFlowCubicMetersPerSecond():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(VolumetricFlowCubicMetersPerSecond())
        >>> {"dimension":28,"unit":306}
    """
    return {"dimension" : 28, "unit" : 306}

def VolumetricFlowCubicYardsPerSecond():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(VolumetricFlowCubicYardsPerSecond())
        >>> {"dimension":28,"unit":307}
    """
    return {"dimension" : 28, "unit" : 307}

def VolumetricFlowLitersPerSecond():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(VolumetricFlowLitersPerSecond())
        >>> {"dimension":28,"unit":308}
    """
    return {"dimension" : 28, "unit" : 308}

def VolumetricFlowLitersPerMinute():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(VolumetricFlowLitersPerMinute())
        >>> {"dimension":28,"unit":309}
    """
    return {"dimension" : 28, "unit" : 309}

def VolumetricFlowLitersPerHour():
    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(VolumetricFlowLitersPerHour())
        >>> {"dimension":28,"unit":310}
    """
    return {"dimension" : 28, "unit" : 310}

def VolumetricFlowGallonsPerSecond():

    """
    Helper function to help creating a measure body when inserting messages into the database

    Returns:
        A JSON object
    Example:
        >>> print(VolumetricFlowGallonsPerSecond())
        >>> {"dimension":28,"unit":311}
    """
    return {"dimension" : 28, "unit" : 311}
