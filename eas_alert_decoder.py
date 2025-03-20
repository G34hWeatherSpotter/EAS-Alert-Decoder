import re

class EASAlertDecoder:
    def __init__(self):
        self.alert_pattern = re.compile(
            r'\xABZCZ-\d{6}-(?P<originator>[A-Z]{3})-(?P<event>[A-Z0-9]{3})-(?P<location>[A-Z0-9]{6})-(?P<start>[0-9]{10})-(?P<duration>[0-9]{4})-(?P<station_id>[A-Z0-9]{8})-')

    def decode(self, eas_message):
        match = self.alert_pattern.search(eas_message)
        if not match:
            raise ValueError("Invalid EAS message format")

        decoded_message = match.groupdict()
        decoded_message['start'] = self.decode_time(decoded_message['start'])
        decoded_message['duration'] = self.decode_duration(decoded_message['duration'])
        return decoded_message

    def decode_time(self, time_str):
        # Decode the time format
        year = time_str[:4]
        day_of_year = int(time_str[4:7])
        hour = time_str[7:9]
        minute = time_str[9:]
        return f"{year}-Day{day_of_year} {hour}:{minute} UTC"

    def decode_duration(self, duration_str):
        hours = int(duration_str[:2])
        minutes = int(duration_str[2:])
        return f"{hours} hour(s) and {minutes} minute(s)"

if __name__ == "__main__":
    decoder = EASAlertDecoder()
    example_message = '\xABZCZ-123456-EAS-RWT-012345-202510201230-0030-WXYZTV12-'
    decoded = decoder.decode(example_message)
    print(decoded)
