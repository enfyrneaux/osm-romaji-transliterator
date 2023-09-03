# OSM Romaji Transliterator

## Description

This Python script applies Hepburn transliteration to Japanese names in an [OpenStreetMap](https://www.openstreetmap.org/) (OSM) file. It leverages the [osmium](https://pypi.org/project/osmium/) and [cutlet](https://github.com/polm/cutlet) libraries to read, modify, and write OSM files. This tool is intended as an intermediate step before sending an OSM file to a tool that lacks proper transliteration such as [mkgmap](https://www.mkgmap.org.uk/doc/index.html).

This tool is not a proper translator, and there is a lot of room for improvement.

## Behavior

- Ignores names fully in Latin script.
- Transliterates names in Japanese scripts to Hepburn Romaji.
- Updates or replaces designated name fields with transliterated names.
- Keeps original names as `name:ja` tag.

## Setup

```bash
git clone https://github.com/enfyrneaux/osm-romaji-transliterator
cd osm-romaji-transliterator
python3 -m venv venv # or your preferred virtual environment
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

Run the `osm-romaji-transliterate.py` script to convert and manipulate Japanese Kana and Romaji tags in OSM (OpenStreetMap) files.

```bash
python3 osm-romaji-transliterate.py \
    --input-osm input.osm \
    --output-osm output.osm \
    --verbose
```

### Required Arguments

- `--input-osm INPUT_OSM`: Specify the input OSM/O5M/PBF file.
- `--output-osm OUTPUT_OSM`: Specify the output OSM/PBF file. O5M outputs are not directly supported.

### Optional Arguments

- `-h, --help`: Show help message and exit.
- `--verbose`: Print conversions.
- `--romaji-system ROMAJI_SYSTEM`: Choose the Romanization system ('hepburn' [default], 'nihon', or 'kunrei').
  
### Tag Handling

_All tag lists are space-delimited._

- `--kana-source-tags [KANA_SOURCE_TAGS ...]`: Source tags for Kana names.
- `--romaji-source-tags [ROMAJI_SOURCE_TAGS ...]`: Source tags for Romaji names.
- `--romaji-dest-tags [ROMAJI_DEST_TAGS ...]`: Destination tags for generated Romaji.
- `--kana-dest-tags [KANA_DEST_TAGS ...]`: Destination tags for extant Kana.

### Miscellaneous

- `--disable-loanwords`: Disable detection of known foreign loanwords.
- `--clobber-romaji-tags`: Overwrite Romaji destination tags.
- `--clobber-kana-tags`: Overwrite Kana destination tags.
- `--ensure-ascii`: Force ASCII output for all converted Romaji.

## Examples

Basic usage (PBF):

```bash
osm-romaji-transliterate.py \
    --input-osm input.osm.pbf \
    --output-osm output.osm.pbf
```

Using a different Romaji system and disable loanword detection:

```bash
osm-romaji-transliterate.py \
    --input-osm input.osm \
    --output-osm output.osm \
    --romaji-system nihon \
    --disable-loanwords
```

Overwrite the `name` tag:

```bash
osm-romaji-transliterate.py \
    --input-osm input.osm \
    --output-osm output.osm \
    --romaji-dest-tags name \
    --clobber-romaji-tags
```

## Known Issues

- Tag replacement logic is a bit all-or-nothing
- Macrons are not supported, (those already present in the `name:ja_rm` tag will be imported, depending on precedence)
- Chinese names (or anything else not handled by Cutlet) will be ignored

## License

MIT License