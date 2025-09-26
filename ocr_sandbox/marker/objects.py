

class markerObject:
    """A class containing all the pertinent information contained within a retrieved marker object"""


    def __init__(self, identifier: str, coordinates: list[float], text: str = None, obj_type: str = None, chars: list[str] = None,charcoords: list[list[float]] = None) -> None:
        self.identifier = identifier
        self.coords = coordinates
        self.txt = text
        self.type = obj_type
        self.chars = chars
        self.charcoords = charcoords

    # define this if you want print to play well in collections of this item
    def __repr__(self):
        if not self.chars:
            return f"<markerObject: id[{self.identifier}] type[{self.type}] text[{self.txt}] coords{(self.coords)}>"
        else:
            return f"<markerObject: id[{self.identifier}] type[{self.type}] text[{self.txt}] chars[{"".join(self.chars)}] line location {(self.coords)}>"

    def __str__(self):
        if not self.chars:
            return f"ID: {self.identifier}\nType: {self.type}\nText: {self.txt}\nCoordinates: {self.coords}"
        else:
            return f"ID: {self.identifier}\nType: {self.type}\nText: {"".join(self.chars)}\nChars: {"".join(self.chars)}\nCoordinates: {self.coords}"
        

    def get_info(self):
        return{self.identifier:(self.coords,self.txt,self.type)}
    


class sentenceObject:

    def __init__(self,sentence,tokens,linked_lines) -> None:
        pass