import osmium
import os
import pykakasi
import cutlet
import re

kks = pykakasi.kakasi()
katsu = cutlet.Cutlet(ensure_ascii=False)

g_replacement_table = []

def is_latin(s):
    for c in s:
        if ord(c) > 127:
            if any(["\u4e00" <= c <= "\u9fff", "\u3040" <= c <= "\u309F", "\u30A0" <= c <= "\u30FF"]):
                return False
    return True

def has_latin_chars(s):
    for c in s:
        if 'a' <= c <= 'z' or 'A' <= c <= 'Z':
            return True
    return False

def appends(node_tags):
    if 'highway' in node_tags:
        if node_tags['highway'].v == 'bus_stop':
            return 'bus stop'
        if node_tags['highway'].v == 'traffic_signals':
            return 'signal'
        else:
            return '????'
        
    return None

class NameModifier(osmium.SimpleHandler):
    def __init__(self, writer):
        super(NameModifier, self).__init__()
        self.writer = writer

    def modify(self, map_item):
        if 'name' not in map_item.tags:
            return map_item

        newtags = {
            t.k:t for t in map_item.tags
        }

        orig_name = map_item.tags.get('name')
        kana_name = map_item.tags.get('name:ja')
        hira_name = map_item.tags.get('name:ja-Hira')
        romaji_name = map_item.tags.get('name:en')

        # don't even bother for full latin names
        if is_latin(orig_name):
            return map_item

        modified = False

        if romaji_name is None:
            
            transliterate_src = None
            #if hira_name is not None:
            #    transliterate_src = hira_name
            #elif kana_name is not None:
            #    transliterate_src = kana_name
            #else:
            transliterate_src = orig_name

            kks_result = kks.convert(transliterate_src)
            kks_converted = ' '.join([
                i['hepburn'] for i in kks_result
            ])

            katsu_converted = katsu.romaji(
                transliterate_src,
                title=not has_latin_chars(orig_name)
            )

            #a = appends(newtags)
            converted_name = None

            #if a is not None:
            #    converted_name = f'{katsu_converted} {a}'
            #else:
            #    converted_name = kks_converted
            converted_name = katsu_converted

            print(f'{orig_name} / {kana_name} / {hira_name} ==> {kks_converted} / {katsu_converted} ==> {converted_name}')
            newtags['name'] = ('name', converted_name)
            modified = True

        # straight swapover
        if romaji_name is not None:
            newtags['name'] = ('name', romaji_name)
            modified = True

        if modified:
            return map_item.replace(tags=list(newtags.values()))

        return map_item

    def node(self, n):
        self.writer.add_node(self.modify(n))

    def way(self, w):
        self.writer.add_way(self.modify(w))

    def relation(self, r):
        self.writer.add_relation(self.modify(r))


input_file = "data/shikoku.osm.pbf"
#input_file = "data/shikoku-updated.osm.pbf"
output_file = "data/shikoku-updated.osm.pbf"
#output_file = "data/shikoku-updated-round2.osm.pbf"

if __name__ == '__main__':
    os.remove(output_file)
    writer = osmium.SimpleWriter(output_file)
    handler = NameModifier(writer)
    handler.apply_file(input_file)

