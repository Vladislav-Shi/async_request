import asyncio
from datetime import datetime

from app.app import main

if __name__ == '__main__':
    print('Start:', datetime.now())
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(main())
    loop.run_until_complete(future)
    print('End:', datetime.now())
