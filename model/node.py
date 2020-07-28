import xml.sax.saxutils as saxutils
from typing import Any
import numbers

from model.local import Local


# Representa elementos com coordenadas lat, lon
class Node(Local):
    def __init__(self, _lat: str, _lon: str, _id="", _street="", _number="", _city="", _suburb="", _state="",
                 _country="BR", _postcode="", _building=False, _name="", _landuse="", _amenity="", _phone="",
                 _email=""):
        super().__init__(_id, _street, _number, _city, _suburb, _state, _country, _postcode, _name, _building, _landuse,
                         _amenity, _phone, _email)
        self.__lat = float(_lat)
        self.__lon = float(_lon)

    @property
    def lon(self): return self.__lon

    @lon.setter
    def lon(self, value): self.validate_coords(value)

    @property
    def lat(self): return self.__lat

    @lat.setter
    def lat(self, value): self.validate_coords(value)

    def validate_coords(self, value):
        if isinstance(value, (str, numbers.Number)):
            try:
                self.__lat = float(value)
            except ValueError:
                self.__lat = float(value.replace(',', '.', 1))

    def clean(self):
        super().clean()
        self.__lat = ''
        self.__lon = ''

    def to_row(self):
        d = super().to_row()
        d.update({
            "_lat": self.lat,
            "_lon": self.lon
        })
        return d


if __name__ == '__main__':
    pass
# from model.node import Node
# nd = Node("-23.1892673", "-46.8807240", "367115360",
#     "SERVIÇOS OFERECIDOS:&lt;br&gt;1 – Acolhimento;&lt;br&gt;2 – Pré-natal e Puericultura;&lt;br&gt;3 – Consulta Médica e de Enfermagem;&lt;br&gt;4 – Consulta e Acompanhamento Odontológico;&lt;br&gt;5 – Procedimentos de Enfermagem (curativos, nebulização, sondagem);&lt;br&gt;6",
#     "820", "Jundiaí", "Maria Alberta", "SP", "BR", "03364-050", False",
#     "Igreja Universal do Reino de Deus",
#     "religious mission", "place_of_worship", "+(55) 11 94869-1313", "iurd@iurd.com.br")
