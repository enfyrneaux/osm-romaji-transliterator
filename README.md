# OSM Romaji Transliterator

## Description

This Python script applies Hepburn transliteration to Japanese names in an OpenStreetMap (OSM) file. It leverages the [osmium](https://pypi.org/project/osmium/) and [cutlet](https://github.com/polm/cutlet) libraries to read, modify, and write OSM files. This tool is intended as an intermediate step before sending an OSM file to a tool that lacks proper transliteration such as [mkgmap](https://www.mkgmap.org.uk/doc/index.html).

This tool is not a proper translator, and there is a lot of room for improvement.

## Behavior

- Ignores names fully in Latin script.
- Transliterates names in non-Latin scripts to Hepburn Romaji.
- Replaces original names with transliterated names.
- Keeps original names as `name:ja` tag.

## Setup

```bash
git clone https://github.com/enfyrneaux/osm-romaji-transliterator
pip install -r requirements.txt
```

## Usage

Run the script with:

```bash
python osm-romaji-transliterate.py \
    --input-osm input.osm \
    --output-osm output.osm \
    --verbose
```

- `--input-osm`: OSM input map file (required)
- `--output-osm`: OSM output map file (required)
- `--verbose`: Write conversions to console

## License

MIT License