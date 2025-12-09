class CoffeeOrder:
    def __init__(self, base: str, size: str, milk: str = "none", 
                 syrups: tuple = (), sugar: int = 0, 
                 iced: bool = False, price: float = 0.0, desc: str = ""):
        self.base = base
        self.size = size
        self.milk = milk
        self.syrups = syrups
        self.sugar = sugar
        self.iced = iced
        self.price = price
        self.desc = desc
    
    def __str__(self):
        return self.desc


class CoffeeOrderBuilder:
    """
    Строитель заказа кофе.
    
    Правила и ограничения:
    - Обязательные поля: base и size
    - Допустимые базы: ["espresso", "americano", "latte", "cappuccino"]
    - Допустимые размеры: ["small", "medium", "large"]
    - Допустимые виды молока: ["none", "whole", "skim", "oat", "soy"]
    - Максимум сиропов: 4
    - Диапазон сахара: 0-5 ложек
    - Доплата за лед: 0.2 рубля
    """
    
    BASE_PRICES = {"espresso": 200, "americano": 250, "latte": 300, "cappuccino": 320}
    SIZE_MULTS = {"small": 1.0, "medium": 1.2, "large": 1.4}
    MILK_PRICES = {"none": 0, "whole": 30, "skim": 30, "oat": 60, "soy": 50}
    SYRUP_PRICE = 40
    ICE_PRICE = 0.2
    MAX_SUGAR = 5
    MAX_SYRUPS = 4
    
    def __init__(self):
        self.base = None
        self.size = None
        self.milk = "none"
        self.syrups = []
        self.sugar = 0
        self.iced = False
    
    def set_base(self, base: str):
        self.base = base
        return self
    
    def set_size(self, size: str):
        self.size = size
        return self
    
    def set_milk(self, milk: str):
        self.milk = milk
        return self
    
    def add_syrup(self, name: str):
        if name not in self.syrups and len(self.syrups) < self.MAX_SYRUPS:
            self.syrups.append(name)
        return self
    
    def set_sugar(self, teaspoons: int):
        if 0 <= teaspoons <= self.MAX_SUGAR:
            self.sugar = teaspoons
        return self
    
    def set_iced(self, iced: bool = True):
        self.iced = iced
        return self
    
    def clear_extras(self):
        self.milk = "none"
        self.syrups = []
        self.sugar = 0
        self.iced = False
        return self
    
    def build(self):
        if self.base is None or self.size is None:
            raise ValueError("Требуется base и size")
        
        price = self.BASE_PRICES[self.base] * self.SIZE_MULTS[self.size]
        price += self.MILK_PRICES[self.milk]
        price += len(self.syrups) * self.SYRUP_PRICE
        if self.iced:
            price += self.ICE_PRICE
        
        parts = [f"{self.size} {self.base}"]
        if self.milk != "none":
            parts.append(f"with {self.milk} milk")
        if self.syrups:
            parts.append(f"+{', '.join(self.syrups)}")
        if self.iced:
            parts.append("(iced)")
        if self.sugar > 0:
            parts.append(f"{self.sugar} tsp sugar")
        
        order = CoffeeOrder(
            base=self.base,
            size=self.size,
            milk=self.milk,
            syrups=tuple(self.syrups),
            sugar=self.sugar,
            iced=self.iced,
            price=round(price, 1),
            desc=" ".join(parts)
        )
        
        return order


if __name__ == "__main__":

    # Тест 1: Базовый заказ
    builder = CoffeeOrderBuilder()
    order = builder.set_base("latte").set_size("medium").set_milk("oat").add_syrup("vanilla").build()
    assert order.base == "latte"
    assert order.size == "medium"
    assert order.price > 0
    print("Тест 1: Базовый заказ: ПРОЙДЕН!")
    
    # Тест 2: Переиспользование билдера
    builder = CoffeeOrderBuilder()
    order1 = builder.set_base("americano").set_size("large").build()
    order2 = builder.clear_extras().set_base("espresso").set_size("small").build()
    assert order1.base == "americano"
    assert order2.base == "espresso"
    print("Тест 2: Переиспользование билдера: ПРОЙДЕН!")
    
    # Тест 3: Валидация - нет base
    builder = CoffeeOrderBuilder()
    try:
        builder.set_size("medium").build()
        print("Тест 3: Валидация (нет base): ПРОШЕЛ С ОШИБКОЙ!")
        assert False
    except ValueError:
        print("Тест 3: Валидация (нет base): ПРОЙДЕН!")
    
    # Тест 4: Валидация - нет size
    builder = CoffeeOrderBuilder()
    try:
        builder.set_base("latte").build()
        print("Тест 4: Валидация (нет size): ПРОШЕЛ С ОШИБКОЙ!")
        assert False
    except ValueError:
        print("Тест 4: Валидация (нет size): ПРОЙДЕН!")
    
    # Тест 5: Валидация сахара
    builder = CoffeeOrderBuilder()
    try:
        builder.set_sugar(10)
        print("Тест 5: Валидация сахара: ПРОШЕЛ С ОШИБКОЙ!")
        assert False
    except:
        print("Тест 5: Валидация сахара: ПРОЙДЕН!")
    
    # Тест 6: Дубликаты сиропов
    builder = CoffeeOrderBuilder()
    order = builder.set_base("cappuccino").set_size("small").add_syrup("caramel").add_syrup("caramel").build()
    assert len(order.syrups) == 1
    print("Тест 6: Дубликаты сиропов: ПРОЙДЕН!")
    
    # Тест 7: Доплата за лед
    builder1 = CoffeeOrderBuilder()
    order1 = builder1.set_base("latte").set_size("medium").build()
    builder2 = CoffeeOrderBuilder()
    order2 = builder2.set_base("latte").set_size("medium").set_iced(True).build()
    assert order2.price > order1.price
    print("Тест 7: Доплата за лед: ПРОЙДЕН!")
    
    print("ВСЕ ПРАВИЛА И ОГРАНИЧЕНИЯ СОБЛЮДЕНЫ!")
    