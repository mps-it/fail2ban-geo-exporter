import geoip2.database

class DBIP:

    def __init__(self, conf):
        self.db_path = conf['geo']['dbip']['db_path']
        self.on_error = conf['geo']['dbip'].get('on_error', '')

    def annotate(self, ip):
        reader = geoip2.database.Reader(self.db_path)
        try:
            lookup = reader.city(ip)
            entry = {
                    'city': str(lookup.city.name),
                    'country': str(lookup.country.name),
                    'latitude': str(lookup.location.latitude),
                    'longitude': str(lookup.location.longitude)
                    }
        except:
            if not self.on_error:
                entry = {}
            else:
                entry = {
                    'city': self.on_error.get('city', 'not set'),
		            'country': self.on_error.get('country', 'not set'),
                    'latitude': self.on_error.get('latitude', '0'),
                    'longitude': self.on_error.get('longitude', '0')
                }
        finally:
            reader.close()

        return entry

    def get_labels(self):
        return ['city', 'country', 'latitude', 'longitude']
