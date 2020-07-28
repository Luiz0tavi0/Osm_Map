import os
from lxml import etree
import csv
from model.local import Local
from model.node import Node


def osm_to_csv(osmfile):
    global local
    path = os.path.abspath(os.path.dirname(__file__)) + f"/data/{osmfile}"
    context = etree.iterparse(path, events=('end',), tag=['node', 'way'], encoding="utf8")

    # Tags que excluem node's representando ruas, semáforos e outros elemntos de tráfego
    tag_to_ignore = {"maxspeed", "place", "waterway", "noexit", "natural", "barrier",
                     "railway", "crossing", "highway", "traffic_calming", "direction"}

    header = ["_id", '_lat', '_lon', "_name", "_street", "_number",
              "_city", "_suburb", "_state", "_country", "_postcode",
              "_landuse", "_amenity", "_phone", "_email", '_building']

    with open('data/points_of_interest.csv', 'a', encoding='utf-8', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, delimiter=';', fieldnames=header)
        writer.writeheader()

    for _, elem in context:
        if elem.tag == 'node':
            local = Node(elem.attrib.get('lat'), elem.attrib.get('lon'))
            filter_tags = tag_to_ignore
        else:
            local = Local()
            filter_tags = {"addr:street", "addr:housenumber"}  # minimal_tags

        if is_point_of_interest(elem, filter_tags):
            local._id = elem.attrib.get("id")

            for tag in elem.iter("tag"):
                if tag.attrib['k'] == "name": local.name = tag.attrib['v']
                if tag.attrib['k'] == "addr:street": local.street = tag.attrib['v']
                if tag.attrib['k'] == "addr:housenumber": local._number = tag.attrib['v']
                if tag.attrib['k'] == "addr:city": local.city = tag.attrib['v']
                if tag.attrib['k'] == "addr:suburb": local.suburb = tag.attrib['v']
                if tag.attrib['k'] == "addr:state": local.state = tag.attrib['v']
                # if tag.attrib['k'] == "addr:country": local.country = tag.attrib['v']
                local.country = "BR"
                if tag.attrib['k'] == "addr:postcode": local.postcode = tag.attrib['v']
                if tag.attrib['k'] == "building" and tag.attrib['v'] != "no":
                    local._building = True
                if tag.attrib['k'] == "landuse": local.landuse = tag.attrib['v']
                if tag.attrib['k'] == "amenity": local.amenity = tag.attrib['v']
                if tag.attrib['k'] == "phone" or tag.attrib['k'] == "contact:phone":
                    local.phone = tag.attrib['v']
                if tag.attrib['k'] == "email": local.email = tag.attrib['v']
            with open('data/points_of_interest.csv', 'a', encoding='UTF-8', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, delimiter=';', fieldnames=header)
                d = local.to_row()
                writer.writerow(d)
                print(d['_id'])
            local.clean()
        elem.clear()


# Deve informar se o elemento possui tags mínimas para identificação
def is_point_of_interest(elem, filter_tags) -> bool:
    tags_found_in_element = get_all_tags(elem, 'tag')
    if len(tags_found_in_element) < 2: return False

    if elem.tag == 'way':
        return len(tags_found_in_element.intersection(filter_tags)) == len(filter_tags)
    return tags_found_in_element.isdisjoint(filter_tags)


# Pega todas as keys de tags com nome 'tag_name'
def get_all_tags(eleme_iter, tag_name: str) -> set:
    return {tag.attrib["k"] for tag in eleme_iter.iter(tag_name)}


if __name__ == '__main__':
    OSMFILE = "brazil-latest.osm"
    osm_to_csv(OSMFILE)
