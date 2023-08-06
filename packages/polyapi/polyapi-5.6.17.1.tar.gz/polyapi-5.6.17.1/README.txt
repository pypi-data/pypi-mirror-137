Библиотека предназначенна для работы с Polymatica API.

Основным модулем бизнес-логики является файл `business_scenarios.py``, импортировать который можно с помощью команды ``from polyapi import business_scenarios as sc``.

Модуль предоставляет два класса для работы с Полиматикой - ``BusinessLogic`` и ``GetDataChunk``. Методы этих классов можно посмотреть при помощи стандартной функции ``dir()``.

Аргументы функций и прочую docstring-документацию модуля и функций можно посмотреть при помощи стандартной функции ``help()``.

Инициализация нового клиентского подключения: ``client = sc.BusinessLogic(login="your_login", password="your_password", url="polymatica_server_url", **args)``
