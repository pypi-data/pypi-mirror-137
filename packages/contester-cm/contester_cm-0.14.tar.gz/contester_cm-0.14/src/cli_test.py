import os
import shutil


# удалить все тесты
def cleartests(task):
    tests_catalog = os.path.join(task, 'tests')

    ans = input('Я надеюсь, Вы знаете, что делаете? (Y/n)')
    if ans == 'n':
        print('Ок, тесты не удалены.')
        return

    if os.path.exists(tests_catalog):
        shutil.rmtree(tests_catalog)
        print('Все тесты успешно удалены.')
    else:
        print('Не найден каталог с тестами.')
        return 1

    os.mkdir(tests_catalog)


# добавить amount тестов
def addtest(task, amount):
    if not os.path.exists(task):
        print('ERROR addtest: не найдена задача с названием ' + task)
        print('\nДля дополнительной информации: https://pypi.org/project/contester-cm/')
        return 1

    tests_catalog = os.path.join(task, 'tests')

    if not os.path.exists(tests_catalog):
        print('ERROR addtest: не найден каталог для файлов тестов')
        print('\nДля дополнительной информации: https://pypi.org/project/contester-cm/')
        return 1

    # определение количества уже созданных тестов
    inputs = 0
    outputs = 0

    files = os.listdir(tests_catalog)
    for file in files:
        if file.endswith('.a'):
            outputs += 1
        else:
            inputs += 1

    already = max(inputs, outputs)

    # создание пустых тестов
    for i in range(already + 1, already + amount + 1, 1):

        preffix = ""
        if i < 10:
            preffix = "0"

        with open(os.path.join(tests_catalog, preffix + str(i) + ''), 'w', encoding='utf-8') as file:
            file.write('')

        with open(os.path.join(tests_catalog, preffix + str(i) + '.a'), 'w', encoding='utf-8') as file:
            file.write('')

    print('Добавлено ' + str(amount) + ' тестов.')
