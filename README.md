# OSM Romaji Transliterator

## Description

This Python script applies Hepburn transliteration to names in an OpenStreetMap (OSM) file. It leverages the `osmium` and `cutlet` libraries to read, modify, and write OSM files.

## Requirements

- Python 3.x
- osmium
- cutlet
- argparse

Install dependencies:

```bash
pip install osmium pyosmium cutlet argparse
```

## Usage

Run the script with:

```bash
python osm-romaji-transliterate.py --input-osm input.osm --output-osm output.osm
```

- `--input-osm`: OSM input map file (required)
- `--output-osm`: OSM output map file (required)

## Behavior

- Ignores names fully in Latin script.
- Transliterates names in non-Latin scripts to Hepburn Romaji.
- Replaces original names with transliterated names.
- Keeps original names as `name:ja` tag.

## License

MIT License