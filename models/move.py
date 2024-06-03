import json

class Move:
    properties = {}
    image_link = None
    url = None
    name = None

    def __init__(self, name=None, data=None) -> None:
        if data is None:
            self.name = name
            self.properties = {}
            self.url = None
            self.image_link = None
        else:
            data = json.loads(data)
            self.name = data['name']
            self.properties = data['properties']
            self.url = data['url']
            self.image_link = data['image_link']

    def add_image_link(self, image_link):
        self.image_link = image_link

    def add_source(self, url):
        self.url = url
    
    def add_property(self, key, value):
        self.properties[key] = value

    def toJSON(self):
        return json.dumps(
            self,
            default=lambda x: x.__dict__,
            sort_keys=True,
            indent=4
        )