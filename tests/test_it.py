import asyncio
import unittest

import asynchooks


class ItTest(unittest.TestCase):
    def test_it(self):
        loop = asyncio.new_event_loop()
        asynchooks.install(loop=loop)
        asynchooks.register(
            create_listener=lambda t, p: print("created {}, {}".format(t.get_name(), p.get_name() if p else None)),
            start_listener=lambda t: print("started {}".format(t.get_name())),
            finish_listener=lambda t: print("finished {}".format(t.get_name())))

        async def worker(sleep_time):
            await asyncio.sleep(sleep_time)

        async def launch():
            await asyncio.gather(worker(0.3), worker(2), worker(1))

        loop.run_until_complete(launch())
