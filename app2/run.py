import asyncio
from datetime import datetime

from app import main

if __name__ == '__main__':
    print('Start:', datetime.now())
    asyncio.run(main())
    print('End:', datetime.now())
