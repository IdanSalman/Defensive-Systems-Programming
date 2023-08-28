class User:
    def __init__(self, name: str, profession: str) -> None:
        self.name = name
        self.profession = profession


class Engineer(User):
    def __init__(self, name: str, profession: str) -> None:
        super().__init__(name, profession)


class Technitian(User):
    def __init__(self, name: str, profession: str) -> None:
        super().__init__(name, profession)


class Barber(User):
    def __init__(self, name: str, profession: str) -> None:
        super().__init__(name, profession)


class Polititian(User):
    def __init__(self, name: str, profession: str) -> None:
        super().__init__(name, profession)


class ElectricEngineer(Engineer):
    def __init__(self, name: str, profession: str) -> None:
        super().__init__(name, profession)


class ComputerEngineer(Engineer):
    def __init__(self, name: str, profession: str) -> None:
        super().__init__(name, profession)


class MachineryEngineer(Engineer):
    def __init__(self, name: str, profession: str) -> None:
        super().__init__(name, profession)


new_class_name = input("Please enter the name of new class: ")
base_class_name = input("Please enter name of base class (blank if none): ")
base_class_name = ""
new_method_name = input(f"Please enter name of new method for class {new_class_name}: ")
new_attribute = input(
    f"Please enter name of new attribute for class {new_class_name}: "
)

class_creation_string = f"class {new_class_name}({base_class_name}):\n\t{new_attribute}=None\n\tdef {new_method_name}(): pass"

exec(class_creation_string)

class_name = eval(f"{new_class_name}.__name__")
class_dict = eval(f"{new_class_name}.__dict__")

print(f"Class __name__ is: {class_name}")
print(f"Class __dict__ is: {class_dict}")
