def read_running_data(data):
    return {
        "activity": data["activity"],
        "date": data["running_date"],
        "description": data["running_description"],
        "distance": data["running_distance"],
        "time_total": data["running_time_total"],
    }
