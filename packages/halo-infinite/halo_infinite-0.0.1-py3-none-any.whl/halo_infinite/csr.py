
class CSR:
    def __init__(self, json_response):
        data = json_response.get('data', None)
        if data is None:
            return
        if not isinstance(data, list):
            return
        self.playlists = {}
        for entry in data:
            new_entry = CSREntry(entry)
            self.playlists[new_entry.input] = new_entry
        if len(self.playlists) < 1:
            return


class CSREntry:
    def __init__(self, entry):
        self.queue = entry.get('queue')
        self.input = entry.get('input')
        response = entry.get('response')
        if response is None:
            return
        current_data = response.get('current', {})
        season_data = response.get('season', {})
        all_time_data = response.get('all_time', {})
        self.current_value = current_data.get('value', None)
        self.current_image_url = current_data.get('tier_image_url', None)
        self.season_value = season_data.get('value', None)
        self.season_image_url = season_data.get('tier_image_url', None)
        self.all_time_value = all_time_data.get('value', None)
        self.all_time_image_url = all_time_data.get('tier_image_url', None)