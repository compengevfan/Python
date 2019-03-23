import sys
import json

data = {
    "president": {
        "name": "Zaphod Beeblebrox",
        "species": "Betelgeusian"
    }
}

json_string = json.dumps(data)

print(json_string)