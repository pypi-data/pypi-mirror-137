# imports
import asyncio
import logging
from aiohttp import ClientSession
from atexit import register
from os import name
from typing import Optional

class WebhookLogger(logging.Handler):
    '''The Discord webhook logger.
    Args:
        url (str): Webhook URL to send messages to.
        ids_to_ping (list[str]): List of IDs to ping in the message if an error occurs. (Optional)
        session (ClientSession): ClientSession to make webhook requests with. (Optional)
    '''
    def __init__(self, url: str, ids_to_ping: Optional[list[str]] = [], session: Optional[ClientSession] = None):
        super().__init__()
        self.__loop = None
        self.__record_formatter = logging.Formatter()
        self.__session = session
        self.__to_ping = ids_to_ping
        self.__webhook_url = url
        # register session closing to happen when deallocated
        register(self.__close)
        
    def __close(self):
        # error checks
        if self is None: return
        if self.__session is None: return
        # close the http session
        if not self.__session.closed:
            asyncio.run(self.__session.close())
        
    def __calculate_prefix(self, levelname: str):
        # debug
        if levelname == 'DEBUG':
            return '```fix\n?  | '
        # info
        elif levelname == 'INFO':
            return '```diff\n+  | '
        # warning
        elif levelname == 'WARNING':
            return '```css\n[  | '
        # error
        elif levelname == 'ERROR':
            return '```diff\n-!  | '
        # critical
        elif levelname == 'CRITICAL':
            return '```diff\n-!!  | '
        # we don't know
        else:
            return '```  |'

    def __calculate_suffix(self, levelname: str):
        # warning
        if levelname == 'WARNING':
            return '  ]```'
        # everything else
        else:
            return '```'

    def emit(self, record: logging.LogRecord):
        # emit our log
        self.__send(self.__record_formatter.format(record), record)
            
    async def __post_content(self, payload):
        # conserve some memory by making a permanent session variable
        if self.__session is None:
            self.__session = ClientSession()
        try:
            # send off our result
            await self.__session.post(url=self.__webhook_url, json=payload)
        except Exception:
            pass

    def __send(self, formatted, record):
        # if we don't have a webhook url, abort the mission!
        if self.__webhook_url is None:
            return

        # make sure the message isn't too long
        parts = [formatted[i:i+1800] for i in range(0, len(formatted), 1800)]
        for i, part in enumerate(parts):
            content = f"{self.__calculate_prefix(record.levelname)}{part}{self.__calculate_suffix(record.levelname)}"
            if i == len(parts) - 1:
                if (record.levelname == 'ERROR' or record.levelname == 'CRITICAL') and self.__to_ping != []:
                    for ind, id in enumerate(self.__to_ping):
                        if len(self.__to_ping) == 1:
                            content += f'||<@{id}>||'
                        elif ind == 0: 
                            content += f'||<@{id}> '
                        elif ind == len(self.__to_ping) - 1:
                            content += f'<@{id}>||'
                        else:
                            content += f'<@{id}> '
            
            # send it off
            payload = {
                "content": content
            }
            # this can crash / fail sometimes, so we add handling for it
            try:
                loop = asyncio.get_event_loop()
                asyncio.ensure_future(self.__post_content(payload))
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self.__post_content(payload))