import xml.sax.saxutils as saxutils
from typing import Any


class Local:
    def __init__(self, id="", street="", number="", city="", suburb="", state="",
                 country="BR", postcode="", name="", building=False,
                 landuse="", amenity="", phone="", email=""):
        self._id = id
        self._street = street
        self._number = number
        self._city = city
        self._suburb = suburb
        self._state = state
        self._country = country
        self._postcode = postcode
        self._name = name
        self._building = building
        self._landuse = landuse
        self._amenity = amenity
        self._phone = phone
        self._email = email

    @property
    def suburb(self):
        return saxutils.unescape(self._suburb).upper()

    @suburb.setter
    def suburb(self, value):
        self._suburb = saxutils.unescape(value).upper()

    @property
    def email(self):
        return saxutils.unescape(self._email).upper()

    @email.setter
    def email(self, value):
        self._email = saxutils.unescape(value).upper()

    @property
    def landuse(self):
        return saxutils.unescape(self._landuse).upper()

    @landuse.setter
    def landuse(self, value):
        self._landuse = saxutils.unescape(value).upper()

    @property
    def phone(self):
        return saxutils.unescape(self._phone)

    @phone.setter
    def phone(self, value):
        self._phone = saxutils.unescape(value)

    @property
    def amenity(self):
        return saxutils.unescape(self._amenity).upper()

    @amenity.setter
    def amenity(self, value):
        self._amenity = saxutils.unescape(value).upper()

    @property
    def name(self):
        return saxutils.unescape(self._name).upper()

    @name.setter
    def name(self, value):
        self._name = saxutils.unescape(value).upper()

    @property
    def city(self): return saxutils.unescape(self._city).upper()

    @city.setter
    def city(self, value): self._city = saxutils.unescape(value).upper()

    @property
    def street(self): return saxutils.unescape(self._street).upper()

    @street.setter
    def street(self, value): self._street = saxutils.unescape(value).upper()

    @property
    def postcode(self): return saxutils.unescape(self._postcode)

    @postcode.setter
    def postcode(self, value):
        self._postcode = \
            saxutils.unescape(value[:5] + '-' + value[5:] if (('-' not in value) and len(value) == 8) else value)

    def clean(self):
        self._id = ""
        self._street = ""
        self._number = ""
        self._city = ""
        self._suburb = ""
        self._state = ""
        self._country = ""
        self._postcode = ""
        self._name = ""
        self._building = False
        self._landuse = ""
        self._amenity = ""
        self._phone = ""
        self._email = ""

    def to_row(self):
        return {"_id": self._id,
                "_name": self.name,
                "_street": self.street,
                "_number": self._number,
                "_city": self.city,
                "_suburb": self.suburb,
                "_state": self._state,
                "_country": self._country,
                "_postcode": self.postcode,
                "_landuse": self.landuse,
                "_amenity": self.amenity,
                "_phone": self.phone,
                "_email": self.email,
                "_building": self._building
                }
