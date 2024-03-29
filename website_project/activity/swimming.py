name = "swimming"
schema = ["date", "distance", "time_total", "description", ]


def read_swimming_data(data):
    data = {
        "activity": data["activity"],
        "date": data["swimming_date"],
        "description": data["swimming_description"],
        "distance": data["swimming_distance"],
        "time_total": data["swimming_time_total"],
    }

    return {key: data[key] for key in schema}
