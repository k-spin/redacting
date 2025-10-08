from flair.data import Sentence
from syntok.tokenizer import Token

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

class spanObject:

    def __init__(self, identifier: int, tokens: list[Token], tag: str, linked_lines: list[str]) -> None:
        self.idx = identifier
        self.tokens = tokens
        self.tag = tag
        self.linked_lines = linked_lines
        # add tracking of parent object (sentence)

    def __repr__(self):
        return f"<<spanObject: ID {self.idx}|| Tokens {self.tokens} | Type [{self.tag}] | Lines {self.linked_lines}>>"
        
    def __str__(self):
        return f"<<spanObject: ID {self.idx}\nTokens [{self.tokens}]\nType [{self.tag}]\nLines {self.linked_lines} >>"


class sentenceObject:

    def __init__(self, text: str,start_position: int, end_position: int, spans: list[spanObject]) -> None:
        self.text = text
        self.startpos = start_position
        self.endpos = end_position
        self.spans = spans
    
    def __repr__(self):
        return f"<<sentenceObject: Interval [{self.startpos},{self.endpos}] | Spans {self.spans}>>"
        
    def __str__(self):
        return f"<<sentenceObject: Interval [{self.startpos},{self.endpos}]\nSpans {self.spans}\nText [{self.text}] >>"
