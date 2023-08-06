import shelve

import sync_dl.config as cfg

from sync_dl_ytapi.helpers import getPlId,pushOrderMoves
from sync_dl_ytapi.credentials import getCredentials,revokeTokens

from sync_dl_ytapi.ytapiWrappers import getItemIds,moveSong, removeSong, addSong
from typing import Callable, Tuple, Union



# actual commands
def pushLocalOrder(plPath):
    credJson = getCredentials()
    if not credJson:
        return
    
    cfg.logger.info("Pushing Local Order to Remote...")
    
    with shelve.open(f"{plPath}/{cfg.metaDataName}", 'c',writeback=True) as metaData:
        url = metaData["url"]
        localIds = metaData["ids"]

    plId = getPlId(url)

    remoteIdPairs = getItemIds(credJson,plId)
    if len(remoteIdPairs) == 0:
        return

    remoteIds,remoteItemIds = zip(*remoteIdPairs)

    cfg.logger.debug(f'Order Before Push: \n'+'\n'.join( [f'{i}: {str(remoteId)}' for i,remoteId in enumerate(remoteIds) ] ))

    moves = pushOrderMoves(remoteIds,remoteItemIds,localIds)

    for move in moves:
        newIndex, songId,itemId = move

        if not moveSong(credJson,plId,songId,itemId,newIndex):
            cfg.logger.error("Ending PushLocalOrder Prematurly")
            return


def logout():
    revokeTokens()


def getPlAdder(plUrl: str) -> Union[Callable[[str, int], bool], None]:
    credJson = getCredentials()
    if not credJson:
        return None

    plId = getPlId(plUrl)

    return lambda songId, index: addSong(credJson, plId, songId, index, plUrl)


def getPlRemover(plUrl: str) -> Union[Tuple[Callable[[int], bool], list[str]], Tuple[None, None]]:
    '''
    returns function to remove remote songs from playlist by index, and list of remoteIds
    indices are not changed due to subsequent removals
    '''
    credJson = getCredentials()
    if not credJson:
        return None, None

    plId = getPlId(plUrl)

    remoteIdPairs = getItemIds(credJson,plId)
    if len(remoteIdPairs) == 0:
        return None, None

    remoteIds, remoteItemIds = zip(*remoteIdPairs)
    remoteIds = list(remoteIds)

    return lambda index: removeSong(credJson, remoteIds[index], plUrl, remoteItemIds[index]), remoteIds

