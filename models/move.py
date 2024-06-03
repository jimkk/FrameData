class Move:
    properties = {}
    image_link = None
    url = None
    name = None

    def __init__(self, name) -> None:
        self.name = name
        self.properties = {}
        self.url = None
        self.image_link = None

    def add_image_link(self, image_link):
        self.image_link = image_link

    def add_source(self, url):
        self.url = url
    
    def add_property(self, key, value):
        self.properties[key] = value

    