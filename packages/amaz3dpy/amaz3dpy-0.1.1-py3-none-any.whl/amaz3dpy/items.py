from abc import ABC, abstractmethod
import asyncio
from threading import Thread
import threading
from typing import Any, final
from xml.dom import NotFoundErr
from amaz3dpy.models import CursorPaging, ProjectFilter, StringFieldComparison

class ListeningCompleted(Exception):
    pass

class Item():
    content: Any

class Paging(ABC):

    def __init__(self, item_type, filter_type, sort_type):
        self._item_type = item_type
        self._filter_type = filter_type
        self._sort_type = sort_type
        self._items_in_page = 5
        self._sort = sort_type(**{
            "direction": "DESC",
            "field": "lastActivityAt"
        })
        self._t = None
        self._lock = threading.Lock()
        self.__stop_thread = False
        self._on_item_received = None
        
    def clear(self):
        self._has_next_page = True
        self._paging = CursorPaging()
        self._paging.first = self._items_in_page
        self.clear_after_value()
        self._items = {}
        self._items_by_id = {}
        self._new_items = {}
        self._filter = self._filter_type()

    def clear_after_value(self):
        self.after = ""

    @property
    def items_in_page(self):
        return self._items_in_page

    @items_in_page.setter
    def items_in_page(self, value: str):
        self._items_in_page = value

    def list(self):
        with self._lock:
            return Paging.get_list(self._items)

    def list_new(self):
        with self._lock:
            return Paging.get_list(self._new_items)

    @staticmethod
    def get_list(dict: dict):
        return {k: v.content for (k,v) in dict.items()}.values()

    @abstractmethod
    def clear_and_load(self, paging: CursorPaging) -> dict:
        pass
    
    @abstractmethod
    def _load_items(self, paging: CursorPaging) -> dict:
        pass

    def load_by_id(self, id: str) -> dict:
        filter = self._filter_type()
        filter.id = StringFieldComparison()
        filter.id.eq = id
        sort = self._sort
        item = self._load_items(CursorPaging(**{"first":1}), filter, sort)
        item = item.edges[0]
        self._store_item(item.node, id=item.node.id)
        return item.node

    def load_next(self) -> int:
        filter = self._filter
        sort = self._sort
        items = self._load_items(self._paging, filter, sort) if self._has_next_page else None
        if items is None:
            return 0

        self._add_items(items.edges)
        self._paging.after = items.pageInfo.endCursor
        self._has_next_page = items.pageInfo.hasNextPage
        return len(items.edges)

    def _add_items(self, items: list):
        for item in items:
            self._store_item(item.node, id=item.node.id, cursor=item.cursor)

    def update_status(self, item):
        current_item = self.get(item.id)

        if current_item is None:
            raise NotFoundErr("Item not found")

        filter = self._filter_type()
        filter.id = StringFieldComparison()
        filter.id.eq = item.id
        result = self._load_items(CursorPaging(**{"first":1}), filter, self._sort)
        updated_item = result.edges[0].node
        self._set_item(updated_item)
        return updated_item

    def _set_item(self, item):
        with self._lock:
            if item.id in self._items_by_id:
                self._items_by_id[item.id].content = item

    def get(self, id: str):
        with self._lock:
            if id in self._items_by_id:
                return self._items_by_id[id].content
            return None

    def _remove_item(self, id):
        item = self.get(id)
        
        if hasattr(item, 'conversionStatus'):
            item.conversionStatus = "deleted"
        
    def add_existing_item(self, item):
        self._store_item(item, item.id)

    def _store_item(self, item_content, id: str, cursor: str = None):
        with self._lock:
            item = Item()
            item.content = item_content
            self._items_by_id[id] = item
            
            if cursor is not None:
                self._items[cursor] = item
            else:
                self._new_items[id] = item

    async def _on_item_received(self, item):
        self._set_item(item)

    async def __check_stop(self):
        while True:
            await asyncio.sleep(5)
            if self.__stop_thread:
                raise ListeningCompleted("Listening completed gracefully")

    @abstractmethod
    async def _handle_subscription(self):
        pass

    async def _listening(self):

        task1 = asyncio.create_task(self.__check_stop())
        task2 = asyncio.create_task(self._handle_subscription())

        try:
            await task1
        except ListeningCompleted:
            task2.cancel()

        try:
            await task2
        except:
            pass

    def __dispatch_event_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._listening())
    
    @final
    def listen(self, on_item_received = None):
        self._on_item_received = on_item_received
        self._t = Thread(target=self.__dispatch_event_loop)
        self._t.start()

    def stop_listen(self):
        self.__stop_thread = True

