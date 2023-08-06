import requests
import json
from math import ceil

from sync_dl_ytapi.helpers import getHttpErr
import sync_dl.config as cfg


def getItemIds(credJson,plId):
    requestURL = "https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=25&pageToken={pageToken}&playlistId={plId}"
    
    def makeRequest(pageToken,pageNum, attempts = 3):
        getRequest = lambda pageToken: requests.get(
            requestURL.format(pageToken=pageToken,plId = plId),
                headers = {
                    'Authorization':'Bearer '+credJson["token"],
                    'Accept':'application/json',
                }
        )

        response = getRequest(pageToken)

        i = 1 

        while not response.ok and i<attempts:
            cfg.logger.debug(response.content.decode("utf8"))
            cfg.logger.error(getHttpErr(response))


            cfg.logger.error(f"Failed to get item Ids for page {pageNum}")
            cfg.logger.info(f"Retrying...")
            response = getRequest(pageToken)
            i+=1

        if not response.ok:
            cfg.logger.debug(response.content.decode("utf8"))
            cfg.logger.error(getHttpErr(response))

            cfg.logger.error(f"Max number of attempts reached for page {pageNum}")
            return
        
        return json.loads(response.content)
    

    try:
        response = makeRequest('',0)
    except Exception as e:
        cfg.logger.debug(e)
        return []

    if not response:
        cfg.logger.error("Issue Getting Playlist Infomration (Potentially Out of Quota for Today)")
        return []

    ids = [] # contains tuples (songId, plItemId)
    for item in response['items']:
        ids.append((item["contentDetails"]['videoId'], item["id"]))

    #repeat the above process for all pages
    plLen = response['pageInfo']['totalResults']
    pageLen = response['pageInfo']['resultsPerPage']
    
    numPages = ceil(plLen/pageLen)
    for i in range(1,numPages): # 0th page already dealt with
        
        response = makeRequest(response['nextPageToken'],i)
        if not response:
            cfg.logger.error("Issue Getting Playlist Infomration (Potentially Out of Quota for Today)")
            return []

        for item in response['items']:
            ids.append((item["contentDetails"]['videoId'], item["id"]))

    return ids


def moveSong(credJson, plId, songId, plItemId, index, attempts = 3):
    '''
    song and plItem Id corrispond to what is being moved index is the where it is moved.
    returns true/false on success/failure
    '''
    # TODO sanitize/ clamp input index 

    putRequest = lambda: requests.put('https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet',
        headers = {
            'Authorization':'Bearer '+credJson["token"],
            'Accept':'application/json',
            'Content-Type':'application/json',
        },
        data = f'{{"id": "{plItemId}","snippet": {{"playlistId": "{plId}","position": {index},"resourceId": {{"kind": "youtube#video","videoId": "{songId}" }} }} }}'
        )
    
    i=1
    try:
        response = putRequest()
    except Exception as e:
        cfg.logger.debug(e)
        return False

    while not response.ok and i<attempts:
        cfg.logger.debug(response.content)
        cfg.logger.error(getHttpErr(response))

        cfg.logger.error(f"Failed attempt to move Song ID: {songId} to Index: {index}")
        cfg.logger.info(f"Retrying...")
        response = putRequest()
        i+=1


    if not response.ok:
        cfg.logger.error(f"Max Attempts to Move Song ID: {songId} to Index: {index} Reached (Potentially Out of Quota for Today)")
        return False
    
    title = json.loads(response.content)["snippet"]["title"]
    cfg.logger.info(f'Moved Song: {title} to Index: {index}')
    
    return True

def removeSong(credJson, songId, plUrl, plItemId, attempts = 3):
    deleteRequest = lambda: requests.delete(f'https://youtube.googleapis.com/youtube/v3/playlistItems?id={plItemId}',
        headers = {
            'Authorization':'Bearer '+credJson["token"],
            'Accept':'application/json',
            'Content-Type':'application/json',
        })
    
    i=1

    try:
        response = deleteRequest()
    except Exception as e:
        cfg.logger.debug(e)
        return False

    while not response.ok and i<attempts:
        cfg.logger.debug(response.content)
        cfg.logger.error(getHttpErr(response))

        cfg.logger.error(f"Failed Attempt to Delete Song ID: {songId} of Playlist: {plUrl}")
        cfg.logger.info(f"Retrying...")
        response = deleteRequest()
        i+=1

    if not response.ok:
        cfg.logger.error(f"Max Attempts Reached to Delete Song ID: {songId} of Playlist: {plUrl} (Potentially Out of Quota for Today)")
        return False

    cfg.logger.debug(f"Deleted Song ID: {songId} from Playlist: {plUrl}")
    return True


def addSong(credJson, plId, songId, index, plUrl, attempts = 3):
    postRequest = lambda: requests.post('https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet',
        headers = {
            'Authorization':'Bearer '+credJson["token"],
            'Accept':'application/json',
            'Content-Type':'application/json',
        },
        data = f'{{"snippet": {{"playlistId": "{plId}","position": {index},"resourceId": {{"kind": "youtube#video","videoId": "{songId}" }} }} }}'
        )

    i=1
    try:
        response = postRequest()
    except Exception as e:
        cfg.logger.debug(e)
        return False

    while not response.ok and i<attempts:
        cfg.logger.debug(response.content)
        cfg.logger.error(getHttpErr(response))

        cfg.logger.error(f"Failed attempt to Add Song ID: {songId} to Index: {index} of Playlist: {plUrl}")
        cfg.logger.info(f"Retrying...")
        response = postRequest()
        i+=1


    if not response.ok:
        cfg.logger.error(f"Max Attempts Reached to Add Song ID: {songId} to Index: {index} of Playlist: {plUrl} (Potentially Out of Quota for Today)")
        return False

    title = json.loads(response.content)["snippet"]["title"]
    cfg.logger.debug(f'Added Song: {title} to Index: {index} of Playlist: {plUrl}')
    return True
