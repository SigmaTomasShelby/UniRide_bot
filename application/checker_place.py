from operator import truediv

dormitories = [
        "№2 Большакова, 77",
        "№4 Большакова, 71",
        "№5 Малышева, 144",
        "№6 Чапаева, 16а",
        #"№7 Коминтерна, 3",
        "№8 Комсомольская, 70",
        "№9 Фонвизина, 8",
        #"№10 Ленина, 66",
        #"№11 Коминтерна, 5",
        #"№12 Фонвизина, 4",
        #"№13 Комсомольская, 66а",
        #"№14 Коминтерна, 1а"
        "НВК 1",
        "НВК 2",
        "Другое (укажите место в комментарии!)"
    ]

institutions = [
        "Куйбышева, 48",
        "Тургенева, 4",
        "Мира, 19",
        "Другое (укажите место в комментарии!)"
    ]

def __in_dorm__(place):
    return place in dormitories

def __in_institute__(place):
    return place in institutions

class CheckerPlace:
    @staticmethod
    def check_places(departure : str, arrival : str):
        if departure == arrival:
            return False
        if __in_dorm__(departure) and __in_institute__(arrival):
            return True
        if __in_dorm__(arrival) and __in_institute__(departure):
            return True
        return False

