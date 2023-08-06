import json
import importlib.resources
from random import randint
from . enums import CountryCode, Gender
from . import data

with importlib.resources.open_text(data, "mail_domains.json") as g_file:
    _mail_domains = json.load(g_file)

_passchars = list(r"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijkl" +
                  r"mnopqrstuvwxyz0123456789*_.,!?&%$=()[]}{\/")

class Person:
    def __init__(self, firstname, lastname, mailaddress, password, street, hsnr, plz, city):
        self.firstname = firstname
        self.lastname = lastname
        self.mailaddress = mailaddress
        self.password = password
        self.street = street
        self.hsnr = hsnr
        self.plz = plz
        self.city = city

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return self.firstname + " " + self.lastname

    def get_full_address(self):
        return self.street + " " + self.hsnr + ", " + self.plz + " " + self.city


def random_person(countrycode: CountryCode = CountryCode.US, gender: Gender = Gender.RANDOM):
    if gender == Gender.RANDOM:
        with importlib.resources.open_text(data, "first_names_" + countrycode.value + "_m.json", encoding="UTF-8") as file:
            _first_names_m = json.load(file)
        with importlib.resources.open_text(data, "first_names_" + countrycode.value + "_f.json", encoding="UTF-8") as file:
            _first_names_f = json.load(file)

        _first_names = _first_names_f + _first_names_m

    else:
        with importlib.resources.open_text(data, "first_names_" + countrycode.value + "_" + gender.value + ".json", encoding="UTF-8") as file:
            _first_names = json.load(file)

    with importlib.resources.open_text(data, "last_names_" + countrycode.value + ".json", encoding="UTF-8") as file:
        _last_names = json.load(file)

    with importlib.resources.open_text(data, "street_names_" + countrycode.value + ".json", encoding="UTF-8") as file:
        _street_names = json.load(file)

    with importlib.resources.open_text(data, "city_names_" + countrycode.value + ".json", encoding="UTF-8") as file:
        _city_names = json.load(file)

    firstname = _first_names[randint(0, len(_first_names) - 1)]
    lastname = _last_names[randint(0, len(_last_names) - 1)]
    maildomain = _mail_domains[randint(0, len(_mail_domains) - 1)]
    mailaddress = firstname + "." + lastname + "@" + maildomain
    password = ""
    street = _street_names[randint(0, len(_street_names) - 1)]
    hsnr = str(randint(1,512))
    plz = str(randint(10000, 99999))
    city = _city_names[randint(0, len(_city_names) - 1)]

    for _ in range(randint(5,12)):
        password += _passchars[randint(0,len(_passchars) - 1)]

    return Person(firstname, lastname, mailaddress, password, street, hsnr, plz, city)
