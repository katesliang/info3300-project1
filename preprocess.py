import csv
import json

FILE_NAME = "tv_shows.csv"
data = {
    "Streaming Platform": {
        "Netflix": {
            "rt_sum": 0,
            "imdb_sum": 0,
            "rt_count": 0, 
            "imdb_count": 0, 
            "rt_mean": 0., 
            "imdb_mean": 0.
        }, 
        "Hulu": {
            "rt_sum": 0,
            "imdb_sum": 0,
            "rt_count": 0, 
            "imdb_count": 0, 
            "rt_mean": 0., 
            "imdb_mean": 0.
        }, 
        "Prime Video": {
            "rt_sum": 0,
            "imdb_sum": 0,
            "rt_count": 0, 
            "imdb_count": 0,  
            "rt_mean": 0., 
            "imdb_mean": 0.
        }, "Disney+": {
            "rt_sum": 0,
            "imdb_sum": 0,
            "rt_count": 0, 
            "imdb_count": 0, 
            "rt_mean": 0., 
            "imdb_mean": 0.
        }
    }, 
    "Year Produced" : {}
}

def convert_rating(key, row, subkey = None, is_streaming = True):
    """ 
    For each `row` in the CSV, update rating in data given the `key`(s)
    """
    rt_arr = row["Rotten Tomatoes"].split('/')
    imdb_arr = row["IMDb"].split('/')

    if len(rt_arr) == 2:
        r = float(rt_arr[0]) / float(rt_arr[1])
        if subkey is not None and is_streaming == False:
            data["Year Produced"][key][subkey]["rt_count"] += 1
            data["Year Produced"][key][subkey]["rt_sum"] += r
            data["Year Produced"][key][subkey]["rt_mean"] = float(data["Year Produced"][key][subkey]["rt_sum"]) / data["Year Produced"][key][subkey]["rt_count"] * 100
        elif is_streaming:
            data["Streaming Platform"][key]["rt_count"] += 1
            data["Streaming Platform"][key]["rt_sum"] += r
            data["Streaming Platform"][key]["rt_mean"] = float(data["Streaming Platform"][key]["rt_sum"]) / data["Streaming Platform"][key]["rt_count"] * 100
    
    if len(imdb_arr) == 2:
        r = float(imdb_arr[0]) / float(imdb_arr[1])
        if subkey is not None:
            data["Year Produced"][key][subkey]["imdb_count"] += 1
            data["Year Produced"][key][subkey]["imdb_sum"] += r
            data["Year Produced"][key][subkey]["imdb_mean"] = float(data["Year Produced"][key][subkey]["imdb_sum"]) / data["Year Produced"][key][subkey]["imdb_count"] * 10
        else:
            data["Streaming Platform"][key]["imdb_count"] += 1
            data["Streaming Platform"][key]["imdb_sum"] += r
            data["Streaming Platform"][key]["imdb_mean"] = float(data["Streaming Platform"][key]["imdb_sum"]) / data["Streaming Platform"][key]["imdb_count"] * 10
    

def preprocess(file_name):
    """
    Reads CSV with `file_name` and parses the data into the global `data` dictionary.
    """
    with open(file_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if int(row["Hulu"]) == 1:
                convert_rating("Hulu", row)
            if int(row["Netflix"]) == 1:
                convert_rating("Netflix", row)
            if int(row["Disney+"]) == 1:
                convert_rating("Disney+", row)
            if int(row["Prime Video"]) == 1:
                convert_rating("Prime Video", row)

            # If show has no age listed, assume target audience is "all"
            if row["Age"] == "":
                row["Age"] = "all"

            if int(row["Year"]) not in data["Year Produced"]:
                data["Year Produced"][int(row["Year"])] = {}
            if row["Age"] not in data["Year Produced"][int(row["Year"])]:
                data["Year Produced"][int(row["Year"])][row["Age"]] = {
                        "rt_sum": 0,
                        "imdb_sum": 0,
                        "rt_count": 0, 
                        "imdb_count": 0, 
                        "rt_mean": 0., 
                        "imdb_mean": 0.
                    }
            convert_rating(int(row["Year"]), row, row["Age"], False)

    
preprocess(FILE_NAME)

# Clean up data
for key in data:
    if key == "Streaming Platform": 
        for k2 in data[key]: 
            del data[key][k2]["rt_sum"]
            del data[key][k2]["imdb_sum"]
    else:
        for year in data["Year Produced"]:
            for age in data["Year Produced"][year]:
                del data[key][year][age]["rt_sum"]
                del data[key][year][age]["imdb_sum"]

# Writing to data.json          
json_object = json.dumps(data, indent=4)
with open("data.json", "w") as outfile:
    outfile.write(json_object)