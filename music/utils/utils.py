from datetime import datetime


class DateUtils:
    @staticmethod
    def convert_date(date_str):
        """
        Converts the release date from ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ) to YYYY-MM-DD.
        If the input is None, returns None.
        """
        if date_str is None:
            return None

        try:
            # Convert the ISO 8601 date string to YYYY-MM-DD
            return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ").date()
        except ValueError:
            # If the format is invalid, return None or handle it appropriately
            return None
