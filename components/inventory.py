class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []
    
    def add_item(self, item):
        results = []

        if len(self.items) >= self.capacity:
            results.append({
                'item_added': None,
                'message': 'You cannot carry any more, your inventory is full'
            })
        else:
            results.append({
                'item_added': item,
                'message': 'You pick up the {0}!'.format(item.name)
            })

            self.items.append(item)

        return results