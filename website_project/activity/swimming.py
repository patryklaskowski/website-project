def read_swimming_data(data):
    return {
        "activity": data["activity"],
        "date": data["swimming_date"],
        "description": data["swimming_description"],
        "distance": data["swimming_distance"],
        "time_total": data["swimming_time_total"],
    }
