import copy

from ui.elements.game_messages import Message

class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []
    
    def add_item(self, item):
        results = []

        if len(self.items) >= self.capacity:
            results.append({
                'item_added': None,
                'message': Message('You cannot carry any more, your inventory is full')
            })
        else:
            results.append({
                'item_added': item,
                'message': Message('You pick up the {0}!'.format(item.name))
            })
            for the_item in self.items:
                if the_item.name == item.name:
                    the_item.item.count += 1
                    break
            else:
                self.items.append(item)
                

        return results
    
    def use(self, item_entity, **kwargs):
        results = []

        item_component = item_entity.item

        if item_component.use_function is None:
            results.append({'message': Message('The {0} cannot be used'.format(item_entity.name))})
        else:
            kwargs = {**item_component.function_kwargs, **kwargs}
            item_use_results = item_component.use_function(self.owner, **kwargs)

            for item_use_result in item_use_results:
                if item_use_result.get('consumed'):
                    self.remove_item(item_entity)

            results.extend(item_use_results)

        return results

    def remove_item(self, item):
        for the_item in self.items:
            if the_item.name == item.name:
                the_item.item.count -= 1
                if the_item.item.count < 1:
                    self.items.remove(item)
                    

    def drop_item(self, item):
        results = []
        new_item = item.copy()
        new_item.x = self.owner.x
        new_item.y = self.owner.y

        self.remove_item(item)
        results.append({'item_dropped': new_item, 'message': Message('You dropped the {0}'.format(item.name))})

        return results