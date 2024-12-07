from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

is_on = True
while is_on:
    options = Menu().get_items()
    choice = input(f"What would you like? ({options}): ")
    if choice == 'off':
        is_on = False
    elif choice == 'report':
        CoffeeMaker().report()
        MoneyMachine().report()
    else:
        drink = Menu().find_drink(choice)
        if CoffeeMaker().is_resource_sufficient(drink) and MoneyMachine().make_payment(drink.cost):
            CoffeeMaker().make_coffee(drink)


