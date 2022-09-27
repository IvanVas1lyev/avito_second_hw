import json


class ColorizeMixin:
    repr_color_code = 33

    def __str__(self):
        return f'\033[1;{self.repr_color_code};40m {self.__repr__()}'


class JsonToPyObject(object):
    def set_attributes(self, data):
        for key, val in data.items():
            setattr(self, key, self.check_attr_value(val))

    def check_attr_value(self, value):
        if type(value) is list:
            return [self.check_attr_value(x) for x in value]
        elif type(value) is dict:
            return self.set_attributes(value)
        else:
            return value


class Advert(ColorizeMixin, JsonToPyObject):
    def __init__(self, data_str):
        data = json.loads(data_str)

        if 'price' in data:
            self.price = data['price']
            data.pop('price')
        else:
            self.price = 0

        self.set_attributes(data)

    def __repr__(self):
        return f'{self.title} | {self.price} ₽'

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):

        if new_price < 0:
            raise ValueError('Price must be >= 0')

        self._price = new_price


data_str = """{
    "title": "python", "price": 0,
    "location": {
        "address": "город Москва, Лесная, 7",
        "metro_stations": ["Белорусская"]
    }
}"""

new_advert = Advert(data_str)
print(new_advert)
