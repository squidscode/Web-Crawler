import json

def init():
    global data
    try:
        with open("./config/crawler_config.json", "r") as read_file:
            data = json.load(read_file)
    except:
        print("config/crawler_config.json file not found!")
        raise SystemExit

    data["word_dictionary"] = {"word_map" : {}, "series_count": {}}
    # "word_dictionary": {"word_map": {}, "series_count": {}}
