# Weather

Weather displays the current local weather to the terminal. The location is deteremind by the user's IP address, or a city can be specified via postal code.

## Installation and Usage

```bash
# Install the requests module
pip3 install requests

# Clone project
git clone https://github.com/michaeljgallagher/weather && cd weather

# Run weather.py
python3 weather.py
```

The weather for other locations can be obtained by passing the postal code as an argument:

```bash
python3 weather.py -z 01003
```

The script defaults to the US for postal codes, but other countries can be specified by passing the country code after the postal code:

```bash
# Geelong, Victoria, Australia
python3 weather.py -z 3220 AU

# Toronto, Ontario, Canada
python3 weather.py --zip m5h ca
```

## argparse settings
```
usage: weather.py [-h] [-z ZIP [ZIP ...]]

Display the current weather

optional arguments:
  -h, --help            show this help message and exit
  -z ZIP [ZIP ...], --zip ZIP [ZIP ...]
                        specify a postal code and/or a country code
```