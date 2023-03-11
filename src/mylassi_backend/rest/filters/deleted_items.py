from enum import Enum


class FilterDeletedItems(str, Enum):
    all_items = 'all',
    only_deleted_items = 'only_deleted'
    only_not_deleted_items = 'only_not_deleted'
