name = "running"
schema = ["date", "distance", "time_total", "description"]


def read_running_data(data):
    data = {
        "activity": data["activity"],
        "date": data["running_date"],
        "description": data["running_description"],
        "distance": data["running_distance"],
        "time_total": data["running_time_total"],
    }

    return {key: data[key] for key in schema}
