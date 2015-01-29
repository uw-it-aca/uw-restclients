"""
This is a class that makes it possible to bulk-save cache entries.
For restclients methods that use threading, this can be used to prevent
innodb gap locks from deadlocking sequential inserts.
"""

__manage_bulk_inserts = False
__bulk_insert_queue = []
from django.db import IntegrityError

def store_cache_entry(entry):
    global __manage_bulk_inserts
    global __bulk_insert_queue

    if __manage_bulk_inserts:
        __bulk_insert_queue.append(entry)
        return
    else:
        entry.save()

def save_all_queued_entries():
    global __bulk_insert_queue

    seen_urls = {}
    bulk_create = []

    try:
        for entry in __bulk_insert_queue:
            if not entry.url in seen_urls:
                entry.save()
                seen_urls[entry.url] = True
    except Exception as ex:
        print("Error bulk saving cache entries: %s" % ex)

    __bulk_insert_queue = []

def enable_cache_entry_queueing():
    global __manage_bulk_inserts
    __manage_bulk_inserts = True

def disable_cache_entry_queueing():
    global __manage_bulk_inserts
    __manage_bulk_inserts = False
    save_all_queued_entries()
