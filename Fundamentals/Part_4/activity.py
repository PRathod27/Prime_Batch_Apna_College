class Product:

    count = 0

    def __init__(self,name,price):
        self.name = name
        self.price = price
        Product.count += 1

    def get_info(self):
        print(f"product is {self.name} and price is {self.price}")

    @classmethod
    def get_count(cls):
        print(f"Total products are {cls.count}")

    @staticmethod
    def calc_discount(price, discount):
        print(f"discounted price is {price - (price * discount / 100)}")

p1 = Product('shoes',10_000)

p1.get_info()
Product.get_count()
p1.calc_discount(p1.price, 12)