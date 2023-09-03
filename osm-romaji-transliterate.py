import osmium
import os
import cutlet
import argparse

# program-wide defaults

g_default_kana_source_tags = [
    'name',
    'name:ja',
    'name:ja-Hira',
    'int_name',
    'name:en',
    'name:ja_rm',
]

g_default_romaji_source_tags = [
    'int_name',
    'name:en',
    'name:ja_rm',
]

g_default_romaji_dest_tags = [
    'name:ja_rm',
    'int_name',
]

g_default_kana_dest_tags = [
    'name:ja',
]

g_default_romaji_system = 'hepburn'

# helper functions
def is_all_latin(s:str) -> bool:
    for c in s:
        if ord(c) > 127:
            if any([
                    "\u4e00" <= c <= "\u9fff",
                    "\u3040" <= c <= "\u309F",
                    "\u30A0" <= c <= "\u30FF",
                    ]):
                return False
    return True

def has_latin_chars(s:str) -> bool:
    for c in s:
        if 'a' <= c <= 'z' or 'A' <= c <= 'Z':
            return True
    return False

def get_in_order(d:dict, keys:list, default=None):
    for k in keys:
        if k in d:
            return d[k]
    
    return default

class NameModifier(osmium.SimpleHandler):
    def __init__(self, writer, **kwargs):
        super(NameModifier, self).__init__()

        # some defaults
        self.verbose = False
        self.kana_source_tags = ['name']
        self.kana_dest_tags = ['name:ja']
        self.romaji_source_tags = ['name', 'int_name', 'name:en', 'name:ja_rm']
        self.romaji_dest_tags = ['int_name', 'name:ja_rm']
        self.clobber_kana = False
        self.clobber_romaji = False
        self.ensure_ascii = False
        self.disable_foreign_spelling = False
        self.romaji_system = 'hepburn'

        # load arg overrides
        for arg_k, arg_v in kwargs.items():
            setattr(self, arg_k, arg_v)


        self.writer = writer
        self.katsu = cutlet.Cutlet(
            self.romaji_system,
            ensure_ascii=self.ensure_ascii,
            use_foreign_spelling=not self.disable_foreign_spelling,
        )


    def modify(self, map_item):

        map_item_tags = {
            t.k:t for t in map_item.tags
        }

        orig_name = get_in_order(
            map_item_tags,
            self.kana_source_tags
        )
        if orig_name is None:
            return map_item

        orig_name = orig_name.v

        # don't even bother for full latin names
        if is_all_latin(orig_name):
            return map_item

        romaji_name = get_in_order(
            map_item_tags,
            self.romaji_source_tags,
        )

        if romaji_name is None:
            transliterate_src = orig_name

            converted_name = self.katsu.romaji(
                transliterate_src,
                title=not has_latin_chars(orig_name)
            )

            # fix weird hyphen spacing issues from cutlet
            converted_name = converted_name.replace(' - ', '-')
            converted_name = converted_name.replace(' -', '-')
            converted_name = converted_name.replace('- ', '-')

            # apply the romaji name
            applied_tags = []

            for tag in self.romaji_dest_tags:
                if tag not in map_item_tags or self.clobber_romaji:
                    map_item_tags[tag] = (tag, converted_name,)
                    applied_tags.append(tag)

            if self.verbose:
                if not self.clobber_romaji:
                    print(f'{orig_name} ==> {converted_name} ({", ".join(applied_tags)})')
                else:
                    print(f'{orig_name} ==> {converted_name}')

            for tag in self.kana_dest_tags:
                if tag not in map_item_tags or self.clobber_kana:
                    map_item_tags[tag] = (tag, orig_name,)

        # straight swapover
        if romaji_name is not None:
            for tag in self.romaji_dest_tags:
                if tag not in map_item_tags or self.clobber_romaji:
                    map_item_tags[tag] = (tag, romaji_name.v,)

        return map_item.replace(tags=list(map_item_tags.values()))

    def node(self, n):
        self.writer.add_node(self.modify(n))

    def way(self, w):
        self.writer.add_way(self.modify(w))

    def relation(self, r):
        self.writer.add_relation(self.modify(r))


def main(args):
    input_file = args.input_osm
    output_file = args.output_osm

    if os.path.exists(output_file):
        os.remove(output_file)

    writer = osmium.SimpleWriter(output_file)
    handler = NameModifier(
        writer,
        verbose=args.verbose,
        kana_source_tags=args.kana_source_tags,
        kana_dest_tags=args.kana_dest_tags,
        romaji_source_tags=args.romaji_source_tags,
        romaji_dest_tags=args.romaji_dest_tags,
        clobber_romaji=args.clobber_romaji_tags,
        clobber_kana=args.clobber_kana_tags,
        ensure_ascii=args.ensure_ascii,
        disable_foreign_spelling=args.disable_loanwords,
    )

    handler.apply_file(input_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-osm", type=str, help="osm/o5m/pbf input map file", required=True)
    parser.add_argument("--output-osm", type=str, help="osm/pbf output map file", required=True)
    parser.add_argument("--verbose", action='store_true', help="print conversions")

    parser.add_argument("--romaji-system", default="hepburn", help="romanization system - hepburn (default), nihon, or kunrei")

    parser.add_argument("--kana-source-tags", nargs="+", 
                        help=f"space-delimited list of source tags for kana names, checked in order (default: {' '.join(g_default_kana_source_tags)})",
                        default=g_default_kana_source_tags)
    parser.add_argument("--romaji-source-tags",
                        nargs="+",
                        help=f"list of source tags for romaji (default: {' '.join(g_default_romaji_source_tags)})",
                        default=g_default_romaji_source_tags)

    parser.add_argument("--romaji-dest-tags",
                        nargs="+",
                        help=f"list of destination tags for generated romaji (default: {' '.join(g_default_romaji_dest_tags)})",
                        default=g_default_romaji_dest_tags)
    
    parser.add_argument("--kana-dest-tags", nargs="+",
                        help=f"copy extant kana to these tags (default: {' '.join(g_default_kana_dest_tags)})",
                        default=g_default_kana_dest_tags)

    parser.add_argument("--disable-loanwords", action="store_true", help="turn off detection of known foreign loanwords")
    parser.add_argument("--clobber-romaji-tags", action="store_true", help="always write converted romaji to --romaji-dest-tags, even if they already have data")
    parser.add_argument("--clobber-kana-tags", action="store_true", help="always write converted kana to --kana-dest-tags, even if they already have data")
    parser.add_argument("--ensure-ascii", action="store_true", help="force ASCII output for all converted romaji - non-ASCII characters are replaced with \"????\"")

    args = parser.parse_args()
    main(args)