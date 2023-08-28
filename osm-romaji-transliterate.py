import osmium
import os
import cutlet
import re
import argparse

katsu = cutlet.Cutlet(ensure_ascii=False)

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

g_verbose = False

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
        romaji_name = map_item.tags.get('name:en')

        # don't even bother for full latin names
        if is_latin(orig_name):
            return map_item

        if romaji_name is None:

            transliterate_src = orig_name

            converted_name = katsu.romaji(
                transliterate_src,
                title=not has_latin_chars(orig_name)
            )

            if g_verbose:
                print(f'{orig_name} ==> {converted_name}')

            newtags['name'] = ('name', converted_name,)
            newtags['name:ja'] = ('name:ja', orig_name,) # preserve the japanese name

        # straight swapover
        if romaji_name is not None:
            newtags['name'] = ('name', romaji_name)

        return map_item.replace(tags=list(newtags.values()))

    def node(self, n):
        self.writer.add_node(self.modify(n))

    def way(self, w):
        self.writer.add_way(self.modify(w))

    def relation(self, r):
        self.writer.add_relation(self.modify(r))


def main(args):
    global g_verbose
    input_file = args.input_osm
    output_file = args.output_osm
    g_verbose = args.verbose

    if os.path.exists(output_file):
        os.remove(output_file)

    writer = osmium.SimpleWriter(output_file)
    handler = NameModifier(writer)
    handler.apply_file(input_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-osm", type=str, help="OSM input map file", required=True)
    parser.add_argument("--output-osm", type=str, help="OSM output map file", required=True)
    parser.add_argument("--verbose", action='store_true', help="Print conversions")
    args = parser.parse_args()
    main(args)