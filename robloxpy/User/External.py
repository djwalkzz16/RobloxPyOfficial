import requests,json,datetime
from .. import Utils as Utils
from . import Friends as Friends 
def GetID(Username):
    """
    Returns the ID of a user based on the username
    """
    response = requests.get(
        Utils.APIURL + f'users/get-by-username?username={Username}')
    try:
        return response.json()['Id']
    except:
        return response.json()['errorMessage']

def GetUserName(UserID):
    response = requests.get(Utils.UserAPI + f"{str(UserID)}")
    """
    Returns the username of a user based on the ID
    """
    try:
        return response.json()['displayName']
    except:
        return "Unable to convert ID"

def UsernameHistory(UserID):
    """
    Returns an array of previous usernames as user has had
    """
    Cursor = ""
    Done = False
    PastNames = []
    while(Done == False):
        response = requests.get(Utils.UserAPIV1 + f"{UserID}/username-history?limit=100&sortOrder=Asc&cursor={Cursor}")
        Names = response.json()['data']
        if((response.json()['nextPageCursor'] == "null") or response.json()['nextPageCursor'] == None):
            Done = True
        else:
            Done = False
            Cursor = response.json()['nextPageCursor']
        for Name in Names:
            PastNames.append(Name['name'])
        if(response.json()['nextPageCursor'] == 'None'):
            Done = True
    return PastNames

def IsOnline(UserID):
    """
    Returns whether a user is online
    """
    response = requests.get(Utils.UserAPI + str(UserID))
    try:
        return response.json()['IsOnline']
    except:
        return 'User not found'

def Isbanned(UserID):
    """
    Returns if a user account is currently banned
    """
    response = requests.get(Utils.UserAPIV1 + str(UserID))
    try:
        return response.json()['isBanned']
    except:
        return 'User not found'

def GetDescription(UserID):
    """
    Returns the description of a given user
    """
    response = requests.get(Utils.UserAPIV1 + str(UserID))
    try:
        return response.json()['description']
    except:
        return 'User not found'

def GetAge(UserID):
    """
    Returns the user's age in days
    """
    response = requests.get(Utils.UserAPIV1 + str(UserID))
    try:
        CreationDate = response.json()['created']
        CreationDate = CreationDate.split('T')
        CreationDate = CreationDate[0].split('-')
        CreationDate = datetime.date(int(CreationDate[0]), int(CreationDate[1]), int(CreationDate[2]))
        Days = ((datetime.date.today()) - (CreationDate))
        Days = str(Days).split(' ')
        return Days[0]
    except:
        return (Utils.UserAPIV1 + str(UserID))

def CreationDate(UserID, Style = 0):
    """
    Returns the date a user was created

    StandardFormat: dd/mm/yyyy
    Americans: mm/dd/yyyy

    If you wish you to use the American format set the 'Style' Vairable to 1

    """
    response = requests.get(Utils.UserAPIV1 + str(UserID))
    try:
        CreationDate = response.json()['created']
        CreationDate = CreationDate.split('T')
        CreationDate = CreationDate[0].split('-')
        if(Style == 0):
            return (str(CreationDate[2]) + '/' + str(CreationDate[1]) + '/' + str(CreationDate[0])) #DD/MM/YYYY -- The Correct Format
        else:
            return (str(CreationDate[1]) + '/' + str(CreationDate[2]) + '/' + str(CreationDate[0])) #MM/DD/YYYY -- Those Colonists Format
    except:
        return response.json()['errors'][0]['message']

def GetRAP(UserID):
    """
    Returns the total offical roblox RAP value for a user

    Please be aware this function can take some time to run depending on internet speed and how many limiteds a user owns
    """
    ErroredRAP = 0
    TotalValue = 0
    Cursor = ""
    Done = False
    while(Done == False):
        try:
            response = requests.get(Utils.Inventory1URL + f"/{UserID}/assets/collectibles?sortOrder=Asc&limit=100&cursor={Cursor}")
            Items = response.json()
            if((response.json()['nextPageCursor'] == "null") or response.json()['nextPageCursor'] == None):
                Done = True
            else:
                Done = False
                Cursor = response.json()['nextPageCursor']
            for Item in Items["data"]:
                try:
                    RAP = int((Item['recentAveragePrice']))
                    TotalValue = TotalValue + RAP
                except:
                    TotalValue = TotalValue
            if(response.json()['nextPageCursor'] == 'None'):
                Done = True
            
        except Exception as ex:
            Done = True
    return(TotalValue)

def GetBust(UserID,Width = 420, Height = 420):
    """
    Returns the link to a bust image of a user

    Width and Height can be customised
    """
    response = requests.get(f"https://www.roblox.com/bust-thumbnail/image?userId={UserID}&width={Width}&height={Height}&format=png")
    return response.url

def GetHeadshot(UserID,Width = 420, Height = 420):
    """
    Returns the link to a headshot image of a user

    Width and Height can be customised
    """
    response = requests.get(f"https://www.roblox.com/headshot-thumbnail/image?userId={UserID}&width={Width}&height={Height}&format=png")
    return response.url

def GetStatus(UserID):
    """
    Returns the current status of a user
    """
    response = requests.get(Utils.UserAPIV1 + f"{str(UserID)}/status")
    return response.json()['status']