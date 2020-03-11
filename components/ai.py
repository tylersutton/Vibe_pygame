class BasicMonster:
    def take_turn(self, target, fov_map, game_map, entities):
        results = []
        monster = self.owner
        
        if fov_map[target.x][target.y]:
            if monster.distance_to(target) >= 2:
                monster.move_towards(target.x, target.y, game_map, entities)

            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)
        
        return results