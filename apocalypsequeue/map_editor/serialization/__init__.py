from system.MapElements.MapElements import CashRegister
from system.MapElements.MapElements import Entrance
from system.MapElements.MapElements import Shelf
from system.MapElements.MapElementType import Int2MapElementType
from system.pathfinding import NavGraphNode
from system.Vector import Vector
import json
import pygame


class MapSerializer:

    @staticmethod
    def save(created_map_elements, map_image_name):
        dic = {}
        for map_element in created_map_elements:
            node_type = map_element.__class__.__name__
            if node_type not in dic:
                dic[node_type] = []
            dic[node_type].append(map_element.serialization())
        if map_image_name is not None:
            with open(map_image_name + ".map", "w+") as outfile:
                json.dump(dic, outfile)


class MapDeserializer:
    @staticmethod
    def load_map_file(map_image_name):
        created_map_elements = []
        with open(map_image_name + ".map") as map_file:
            data = json.load(map_file)
            for key, value in data.items():
                if key == "Shelf":
                    for sh in value:
                        created_map_elements.append(Shelf(pygame.Rect(sh['pos'], sh['dim'])))
                elif key == "NavGraphNode":
                    node_dic = {}
                    for n in value:
                        node = NavGraphNode(Vector(n['pos']['left'], n['pos']['top']))
                        node.set_id(n['id'])
                        node.set_type(Int2MapElementType[n['type']])
                        node_dic[node.get_id()] = node
                        created_map_elements.append(node)
                    for n1 in value:
                        for n2 in n1['neighbor']:
                            node_dic[n1['id']].add_neighbor( node_dic[n2['neighbor_id']] )
                elif key == "Entrance":
                    for en in value:
                        created_map_elements.append(Entrance(pygame.Rect(en['pos'], en['dim'])))
                elif key == "CashRegister":
                    for cr in value:
                        created_map_elements.append(CashRegister(pygame.Rect(cr['pos'], cr['dim'])))
        return created_map_elements
