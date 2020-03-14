class BasicMonster:
    def take_turn(self, target, fov_map, game_map, entities):
        results = []
        monster = self.owner
        
        if fov_map[monster.x][monster.y]: # updated to always use player's fov (temp fix)
            if monster.distance_to(target) >= 2:
                monster.move_astar(target.x, target.y, game_map, entities)

            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)
        
        return results