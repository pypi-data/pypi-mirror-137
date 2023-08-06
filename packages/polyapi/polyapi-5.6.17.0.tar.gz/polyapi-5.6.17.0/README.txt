Библиотека предназначенна для работы с Polymatica API.

Первым шагом необходимо импортировать модуль бизнес-логики командой ``from polyapi import business_scenarios as sc``

Далее нужно инициализировать класс бизнес-логики.
Если используется механизм беспарольной авторизации, то password указывать не нужно.

``sc = sc.BusinessLogic(login="your_login", password="your_password", url="polymatica_server_url")``

Скрипты запускаются при помощи методов, находящихся в файле ``business_scenarios.py``

Методы класса ``BusinessLogic`` можно посмотреть при помощи стандартной функции Python: ``dir()``

Аргументы функций, их смысл, а также прочую docstring-документацию модуля и функций можно посмотреть при помощи стандартной функции Python: ``help()``

В модуле ``business_scenarios`` есть функции ``execute_olap_command()`` и ``execute_manager_command()``.
``execute_olap_command()`` должна запускать любые выбранные команды модуля Olap.
``execute_manager_command()`` должна запускать любые выбранные команды модуля Manager.
