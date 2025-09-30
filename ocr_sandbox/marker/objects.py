from flair.data import Sentence

class markerObject:
    """A class containing all the pertinent information contained within a retrieved marker object"""


    def __init__(self, identifier: str, coordinates: list[float], text: str = None, obj_type: str = None, chars: list[str] = None,charcoords: list[list[float]] = None) -> None:
        self.identifier = identifier
        self.coords = coordinates
        self.text = text
        self.type = obj_type
        self.chars = chars
        self.charcoords = charcoords

    # define this if you want print to play well in collections of this item
    def __repr__(self):
        if not self.chars:
            return f"<markerObject: id[{self.identifier}] type[{self.type}] text[{self.text}] coords{(self.coords)}>"
        else:
            return f"<markerObject: id[{self.identifier}] type[{self.type}] text[{self.text}] chars[{"".join(self.chars)}] line location {(self.coords)}>"

    def __str__(self):
        if not self.chars:
            return f"ID: {self.identifier}\nType: {self.type}\nText: {self.text}\nCoordinates: {self.coords}"
        else:
            return f"ID: {self.identifier}\nType: {self.type}\nText: {"".join(self.chars)}\nChars: {"".join(self.chars)}\nCoordinates: {self.coords}"
        

    def __len__(self):
        return len(self.text)

    def get_info(self):
        return{self.identifier:(self.coords,self.text,self.type)}
    


class sentenceObject:

    def __init__(self,sentence: Sentence,linked_lines) -> None:
        self.sentence = sentence
        self.linked_lines = linked_lines
