#! coding:utf-8
import asyncio


class SyncCallMixin(object):

    def call_sync(self, *args, **kwargs):
        return asyncio.get_event_loop().run_until_complete(
            self.call(*args, **kwargs)
        )
