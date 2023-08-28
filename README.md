# OSM Romaji Transliterator

## Description

This Python script applies Hepburn transliteration to Japanese names in an [OpenStreetMap](https://www.openstreetmap.org/) (OSM) file. It leverages the [osmium](https://pypi.org/project/osmium/) and [cutlet](https://github.com/polm/cutlet) libraries to read, modify, and write OSM files. This tool is intended as an intermediate step before sending an OSM file to a tool that lacks proper transliteration such as [mkgmap](https://www.mkgmap.org.uk/doc/index.html).

This tool is not a proper translator, and there is a lot of room for improvement.

## Behavior

- Ignores names fully in Latin script.
- Transliterates names in Japanese scripts to Hepburn Romaji.
- Replaces original names with transliterated names.
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

Run the script with:

```bash
python3 osm-romaji-transliterate.py \
    --input-osm input.osm \
    --output-osm output.osm \
    --verbose
```

### Command Line Flags

- `--input-osm`: OSM input map file (required)
- `--output-osm`: OSM output map file (required)
- `--verbose`: Write conversions to console

## Known Issues

- Tag language precedence is hardcoded (a flag will be added for this)
- Macrons are not supported, (those already present in the `name:ja_rm` tag will be imported, depending on precedence)
- Chinese names (or anything else not handled by Cutlet) will be ignored

## License

MIT License