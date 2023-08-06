#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Модуль обработки ошибок из ответа """

import re
import requests
import datetime
from typing import Dict, Union, Callable
from .common import MONTHS, WEEK_DAYS, datetime_type, FUNCS, LOGIC_FUNCS


def request_asserts(response: Dict, r: requests.models.Response) -> bool:
    """
    Проверка ответов сервера.
    :param response: (dict) ответ сервера в формате json (по сути, это r.json()).
    :param r: <class 'requests.models.Response'>
    :return: True, если все проверки прошли успешно, иначе будет сгенерирован AssertionError.
    """
    # парсинг ответа
    response_queries = response.get("queries")
    assert len(response_queries) > 0, 'No field "queries" in response!'
    resp_queries = next(iter(response_queries))  # [0] element in vector
    resp_command = resp_queries.get("command")
    resp_command_err = resp_command.get("error")

    assert resp_command, str(resp_command_err)
    assert r.status_code == 200, "Response code != 200"

    if "error" in resp_command:
        resp_command_err_code = resp_command_err.get("code")
        resp_command_err_message = resp_command_err.get("message")
        assert resp_command_err_code == 0, "Error in response: {}".format(resp_command_err_message)

    if ("error" in resp_command) and ("status" in resp_command):
        resp_command_status = resp_command.get("status")
        resp_command_status_code = resp_command_status.get("code")
        resp_command_status_message = resp_command_status.get("message")
        assert resp_command_status_code == 0, "Error in response: {}".format(resp_command_status_message)

    if ("error" in resp_command) and ("datasources" in resp_command):
        resp_command_datasources = next(iter(resp_command.get("datasources")))  # [0] element in vector
        datasources_status = resp_command_datasources.get("status")
        datasources_status_code = datasources_status.get("code")
        resp_command_status_message = datasources_status.get("message")
        assert datasources_status_code == 0, "Error in response: {}".format(resp_command_status_message)

    return True


def checks(self, func_name: str, *args):
    """
    Реализация проверок различных функций.
    :param self: экземпляр класса BusinessLogic.
    :param func_name: название функции.
    :param args: прочие параметры, необходимые для проверки.
    """
    if func_name == "rename_group":
        group_uuid = args[0]
        group_name = args[1]
        new_name = args[2]
        if not group_uuid:
            raise ValueError('No such group: {}'.format(group_name))
        if not new_name:
            raise ValueError('New group name cannot be empty!')
        return True
    if func_name == "move_dimension":
        if self.multisphere_module_id == "":
            raise ValueError("First create cube and get data from it!")
        # определяем числовое значение позиции
        position, level = args[0], args[1]
        num_position = {'left': 1, 'up': 2, 'out': 0}.get(position, -1)
        # если осталось значение по-умолчанию - значит передана несуществующая позиция
        if num_position == -1:
            raise ValueError('Position "{}" does not exist! It can only be "up", "left" or "out"!'.format(position))
        # при выносе размерности влево/вверх уровень должен быть явно задан
        if num_position in [1, 2] and level is None:
            raise ValueError('При выносе размерности влево/вверх должен быть явно задан параметр "level"!')
        # вернём числовую позицию
        return num_position
    elif func_name == "polymatica_health_check_multisphere_updates":
        cubes_list = args[0]
        cube_name = args[1]
        for cube in cubes_list:
            if cube["name"] == cube_name:
                return True
        raise ValueError("No such cube in cubes list: %s" % cube_name)
    elif func_name == "rename_dimension":
        dim_name = args[0]
        if not isinstance(dim_name, str):
            raise ValueError('Dimension name "{}" is not valid. It should have "string" type'.format(dim_name))
        return True
    elif func_name == "select_unselect_impl":
        left_dims, top_dims, position = args[0], args[1], args[2]
        if position not in ["left", "top"]:
            raise ValueError('Param "position" must be either "left" or "top"!')
        if position == 'left' and not left_dims:
            raise ValueError("Left dimensions required!")
        if position == 'top' and not top_dims:
            raise ValueError("Top dimensions required!")
        return 1 if position == "left" else 2
    elif func_name == "set_measure_visibility":
        is_visible = args[0]
        if not isinstance(is_visible, bool):
            raise ValueError("is_visible param can only be boolean: True / False")
        return True
    elif func_name == "sort_measure":
        is_visible = args[0]
        if is_visible not in ("ascending", "descending", "off"):
            raise ValueError('Param "sort_type" can only equals "ascending" or "descending" or "off"!')
        return True
    elif func_name == "unfold_all_dims":
        position, level = args[0], args[1]
        # проверка позиции
        if position not in ["left", "up"]:
            raise ValueError('Param "position" must be either "left" or "up"!')
        # проверка значения уровня
        if level < 0:
            raise ValueError('Param "level" can be only positive!')
        return 1 if position == "left" else 2
    elif func_name == "set_width_columns":
        measures, measures_list, left_dims, left_dims_data = args[0], args[1], args[2], args[3]
        error_msg = str()
        if len(measures) != len(measures_list):
            error_msg = 'Длина списка в параметре "measures" должна совпадать с ' \
                'количеством нескрытых фактов мультисферы!'
        if len(left_dims) != len(left_dims_data):
            error_msg = 'Длина списка в параметре "left_dims" должна совпадать с ' \
                'количеством левых размерностей мультисферы!'
        if error_msg:
            raise ValueError(error_msg)
        return True
    elif func_name == "delete_dim_filter":
        dim_name, filter_name, num_row = args[0], args[1], args[2]
        if not isinstance(dim_name, str):
            raise ValueError('Param "dim_name" must be "str" type!')
        if not isinstance(num_row, int):
            raise ValueError('Param "num_row" must be "int" type!')
        if not isinstance(filter_name, (str, list, set, tuple)):
            raise ValueError('Param "filter_name" must be one of following types: ["str", "list", "set", "tuple"]!')
        if not filter_name:
            raise ValueError('Param "filter_name" cannot be empty!')
        return [filter_name] if isinstance(filter_name, str) else filter_name
    elif func_name == "put_dim_filter":
        filter_name, start_date, end_date, filter_field_format = args[0], args[1], args[2], args[3]
        if (filter_name is None) and (start_date is None and end_date is None):
            raise ValueError("If you don't filter one value by param filter_name,"
                             " please assign value to args start_date AND end_date!")
        elif (filter_name is not None) and (start_date is not None and end_date is not None):
            raise ValueError("Please, fill in arg filter_name for filtering one value OR:\n"
                             "args start_date AND end_date for filtering date interval!")

        # список для заполнения данными
        dates_list = []

        # Заполнение списка dates_list в зависимости от содержания параметров filter_name, start_date, end_date
        # заполнить список для недельного интервала
        if (filter_name is None) and (start_date is not None and end_date is not None):
            # заполнение списка недельного интервала
            if (start_date in WEEK_DAYS) and (end_date in WEEK_DAYS):
                start_ind = WEEK_DAYS.index(start_date)
                end_ind = WEEK_DAYS.index(end_date)
                if start_ind > end_ind:
                    raise ValueError("Start week day can not be more than the end week day!")
                dates_list = WEEK_DAYS[start_ind:end_ind + 1]
            # заполнение списка месячного интервала
            elif (start_date in MONTHS) and (end_date in MONTHS):
                start_ind = MONTHS.index(start_date)
                end_ind = MONTHS.index(end_date)
                if start_ind > end_ind:
                    raise ValueError("Start month can not be more than the end month!")
                dates_list = MONTHS[start_ind:end_ind + 1]
            # заполнение списка с интервалом числовых дат
            elif isinstance(start_date, int) and isinstance(end_date, int):
                if start_date > end_date:
                    raise ValueError("Start date can not be more than the end date!")
                end_date += 1
                dates_list = [str(x) for x in range(start_date, end_date)]
            # заполнение списка в одном из форматов (год и день недели можно менять местами):
            # "ДД.ММ.ГГГГ"
            # "ДД-ММ-ГГГГ"
            # "ДД.ММ.ГГГГ ЧЧ:ММ:СС"
            # "ДД-ММ-ГГГГ ЧЧ:ММ:СС"
            elif isinstance(start_date, str) and isinstance(end_date, str):
                def get_start_end_date(start: str, end: str) -> Callable:
                    """
                    Возвращает функцию получения начальной и конечной даты (по сути, является обёрткой над функцией).
                    """
                    start_date, end_date = start, end
                    def get_date_range(pattern: str, current_format: str) -> Union[datetime_type, None]:
                        """
                        Получение начальной и конечной даты по заданному шаблону (паттерну) и формату.
                        Генерирует ошибку, если начальная дата больше конечной.
                        Если заданные даты начала и конца не подходят под шаблон - вернётся None, None.
                        ВАЖНО: подразумевается, что формат начальной и конечной даты одинаков.
                        :param pattern: шаблон для регулярного выражения
                        :param current_format: формат даты в Полиматике
                        """
                        reg = re.compile(pattern)
                        if reg.match(start_date) and reg.match(end_date):
                            try:
                                start = datetime.datetime.strptime(start_date, current_format)
                                end = datetime.datetime.strptime(end_date, current_format)
                            except Exception:
                                error_msg = 'Could not convert string to datetime format! ' \
                                    'start_date: {}, end_date: {}'.format(start_date, end_date)
                                raise ValueError(error_msg)
                            if start > end:
                                raise ValueError('Start date can not be more than the end date!')
                            return start, end
                        return None, None
                    return get_date_range

                # функция генерирования начальной и конечной даты
                date_range_func = get_start_end_date(start_date, end_date)

                # описание паттернов и форматов
                # FIXME Внимание, говнокод (говнорегулярки)! Подумать, как можно сделать лучше.
                patterns = (
                    (
                        r'^([0]?[1-9]{1}|1[0-9]{1}|2[0-9]{1}|3[0-1]{1})\.([0]?[1-9]{1}|1[0-2]{1})\.[1-9]{1}[0-9]{3}$',
                        '%d.%m.%Y'
                    ),
                    (
                        r'^[1-9]{1}[0-9]{3}\.([0]?[1-9]{1}|1[0-2]{1})\.([0]?[1-9]{1}|1[0-9]{1}|2[0-9]{1}|3[0-1]{1})$',
                        '%Y.%m.%d'
                    ),
                    (
                        r'^([0]?[1-9]{1}|1[0-9]{1}|2[0-9]{1}|3[0-1]{1})\-([0]?[1-9]{1}|1[0-2]{1})\-[1-9]{1}[0-9]{3}$',
                        '%d-%m-%Y'
                    ),
                    (
                        r'^[1-9]{1}[0-9]{3}\-([0]?[1-9]{1}|1[0-2]{1})\-([0]?[1-9]{1}|1[0-9]{1}|2[0-9]{1}|3[0-1]{1})$',
                        '%Y-%m-%d'
                    ),
                    (
                        r'^([0]?[1-9]{1}|1[0-9]{1}|2[0-9]{1}|3[0-1]{1})\.([0]?[1-9]{1}|1[0-2]{1})\.[1-9]{1}[0-9]{3} ([0]?[0-9]{1}|1[0-9]{1}|2[0-3]{1})\:([0]?[0-9]{1}|1[0-9]{1}|2[0-9]{1}|3[0-9]{1}|4[0-9]{1}|5[0-9]{1})\:([0]?[0-9]{1}|1[0-9]{1}|2[0-9]{1}|3[0-9]{1}|4[0-9]{1}|5[0-9]{1})',
                        '%d.%m.%Y %H:%M:%S'
                    ),
                    (
                        r'^[1-9]{1}[0-9]{3}\.([0]?[1-9]{1}|1[0-2]{1})\.([0]?[1-9]{1}|1[0-9]{1}|2[0-9]{1}|3[0-1]{1}) ([0]?[0-9]{1}|1[0-9]{1}|2[0-3]{1})\:([0]?[0-9]{1}|1[0-9]{1}|2[0-9]{1}|3[0-9]{1}|4[0-9]{1}|5[0-9]{1})\:([0]?[0-9]{1}|1[0-9]{1}|2[0-9]{1}|3[0-9]{1}|4[0-9]{1}|5[0-9]{1})',
                        '%Y.%m.%d %H:%M:%S'
                    ),
                    (
                        r'^([0]?[1-9]{1}|1[0-9]{1}|2[0-9]{1}|3[0-1]{1})\-([0]?[1-9]{1}|1[0-2]{1})\-[1-9]{1}[0-9]{3} ([0]?[0-9]{1}|1[0-9]{1}|2[0-3]{1})\:([0]?[0-9]{1}|1[0-9]{1}|2[0-9]{1}|3[0-9]{1}|4[0-9]{1}|5[0-9]{1})\:([0]?[0-9]{1}|1[0-9]{1}|2[0-9]{1}|3[0-9]{1}|4[0-9]{1}|5[0-9]{1})',
                        '%d-%m-%Y %H:%M:%S'
                    ),
                    (
                        r'^[1-9]{1}[0-9]{3}\-([0]?[1-9]{1}|1[0-2]{1})\-([0]?[1-9]{1}|1[0-9]{1}|2[0-9]{1}|3[0-1]{1}) ([0]?[0-9]{1}|1[0-9]{1}|2[0-3]{1})\:([0]?[0-9]{1}|1[0-9]{1}|2[0-9]{1}|3[0-9]{1}|4[0-9]{1}|5[0-9]{1})\:([0]?[0-9]{1}|1[0-9]{1}|2[0-9]{1}|3[0-9]{1}|4[0-9]{1}|5[0-9]{1})',
                        '%Y-%m-%d %H:%M:%S'
                    )
                )

                # определяем подходящий формат
                start, end = None, None
                for pattern in patterns:
                    current_start, current_end = date_range_func(pattern[0], pattern[1])
                    if current_start and current_end:
                        start, end = current_start, current_end
                        break
                else:
                    raise ValueError("Unknown date format! start_date: {}, end_date: {}".format(start_date, end_date))

                # получаем формат хранения дат в Полиматике, если он не задан пользователем
                date_format_pattern = filter_field_format or self.get_current_datetime_format()

                # заполняем dates_list
                step = datetime.timedelta(days=1)
                while start <= end:
                    dates_list.append(start.strftime(date_format_pattern))
                    start += step
            else:
                raise ValueError("Unknown date format! start_date: {}, end_date: {}".format(start_date, end_date))
        return dates_list
    elif func_name == "export":
        file_format, file_path = args[0], args[1]
        if file_format not in ["csv", "xls", "json"]:
            raise ValueError('Wrong file format: "{}". Only .csv, .xls, .json formats allowed!'.format(file_format))
        if not file_path:
            raise ValueError('Empty file path!')
        return True
    elif func_name == "run_scenario":
        scenario_id, scenario_name = args[0], args[1]
        if (scenario_id is None) and (scenario_name is None):
            raise ValueError("Нужно ввести либо uuid, либо название сценария!")
        return True
    elif func_name == "set_measure_precision":
        measure_names, precision = args[0], args[1]
        if len(measure_names) != len(precision):
            raise ValueError("Длина списка с названиями фактов (%s) != длине списка с размерностями (%s)!" %
                             (len(measure_names), len(precision)))
        return True
    elif func_name == "create_sphere":
        if len(args) == 1:
            i = args[0]
            # проверка есть ли в названиях размерностей и фактов метка порядка байтов U + FEFF Byte Order МАРК (BOM)
            if "\ufeff" in i["name"]:
                raise ValueError("Измените кодировку исходного файла на UTF-8 без BOM!")
            if "\ufeff" in i["db_field"]:
                raise ValueError("Измените кодировку исходного файла на UTF-8 без BOM!")
            return True

        update_params, updates, file_type, sql_params, user_interval, interval, period, week, time_zones, source_name,\
            cube_name = args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8], args[9],\
            args[10]

        # проверка, что создается мультисфера с уникальным названием
        if "not found" not in self.get_cube_without_creating_module(cube_name):
            raise ValueError("Multisphere %s already exists!" % cube_name)

        if len(cube_name) < 5:
            raise ValueError("Название мультисферы должно состоять из 5 и более символов!")

        # проверка заданного вида обновления
        if update_params["type"] not in updates:
            raise ValueError("Обновление '%s' не существует!" % update_params["type"])

        # проверка корректности параметров в словаре sql_params
        if (file_type != "excel") and (file_type != "csv"):
            if sql_params is None:
                raise ValueError("If your sourse is sql: fill in param sql_params!\n\n"
                                 "In other cases: it is wrong param file_type: %s\n\nIt can be only:\n"
                                 "excel OR csv" % file_type)
            if ("server" not in sql_params) or ("login" not in sql_params) or ("passwd" not in sql_params) \
                    or ("sql_query" not in sql_params):
                raise ValueError(
                    "Please check the following params names in sql_params:\n-server\n-login\n-passwd\n-sql_query")

        if user_interval not in interval:
            raise ValueError("No such interval: %s" % user_interval)

        # проверка длины и отствия пробелов в имени источника
        if len(source_name) < 5:
            raise ValueError("Имя источника должно состоять из 5 и более символов!")
        if " " in source_name:
            raise ValueError("Знак <ПРОБЕЛ> не должен быть в Имени источника!")

        if update_params["type"] != "ручное":
            # проверка корректности введенной часовой зоны
            if update_params["schedule"]["time_zone"] not in time_zones:
                raise ValueError("Time zone %s does not exist!" % update_params["schedule"]["time_zone"])
            # проверка периода, дня недели:
            if update_params["schedule"]["type"] not in period:
                raise ValueError("Нет периода: %s !" % update_params["schedule"]["type"])
            if "week_day" in update_params["schedule"]:
                if update_params["schedule"]["week_day"] not in week:
                    raise ValueError("Неверный день недели: %s !" % update_params["schedule"]["week_day"])
            if "day" in update_params["schedule"]:
                if update_params["schedule"]["day"] > 31:
                    raise ValueError("Неверный день месяца: %s !" % update_params["schedule"]["day"])
        self.func_name = 'create_sphere'
        return True
    elif func_name == "execute_olap_command":
        if self.multisphere_module_id == "":
            raise ValueError("First create cube and get data from it!")
        return True
    elif func_name == 'load_sphere_chunk':
        units, convert_type, convert_empty_values = args[0], args[1], args[2]
        is_int = False
        error_msg = 'Param "units" must be a positive integer number!'
        try:
            is_int = int(units) == float(units)
        except ValueError:
            raise ValueError(error_msg)
        if not is_int or int(units) <= 0:
            raise ValueError(error_msg)
        if not isinstance(convert_type, bool):
            raise ValueError('Param "convert_type" can only be boolean: True / False!')
        if not isinstance(convert_empty_values, bool):
            raise ValueError('Param "convert_empty_values" can only be boolean: True / False!')
    elif func_name == 'set_measure_level':
        level, left_dims_count = args[0], args[1]
        error_msg = str()
        if left_dims_count < 3:
            error_msg = '3 or more dimensions must be take out!'
        elif level <= 0:
            error_msg = 'Param "level" must be positive!'
        elif level > left_dims_count - 1:
            error_msg = 'Invalid "level" param! Max allowable value: {}'.format(left_dims_count - 1)
        if error_msg:
            raise ValueError(error_msg)
    elif func_name == 'set_measure_select':
        measure_id, measure_name = args[0], args[1]
        if not measure_id and not measure_name:
            raise ValueError('Need to specify either measure identifier or measure name!')
    elif func_name == 'set_all_measure_visibility':
        is_visible = args[0]
        if not isinstance(is_visible, bool):
            raise ValueError('Param "is_visible" can only be boolean: True / False')
        return True
    elif func_name == 'set_measure_direction':
        is_horizontal = args[0]
        if is_horizontal not in [True, False]:
            raise ValueError('Param "is_horizontal" must be "True" or "False"!')
    elif func_name == 'get_scenario_metadata':
        script_id = args[0]
        if not isinstance(script_id, str):
            raise ValueError('Param "script_id" must be string type!')
        if not script_id:
            raise ValueError('Param "script_id" not set!')
    elif func_name == 'reset_filters':
        dimensions = args[0]
        if isinstance(dimensions, str):
            return [dimensions] if dimensions else []
        elif isinstance(dimensions, (list, tuple)):
            return dimensions
        else:
            raise ValueError('Param "dimensions" must be "str", "list" or "tuple" type!')
    elif func_name == 'get_cube_info':
        cube = args[0]
        if not isinstance(cube, str):
            raise ValueError('Param "cube" must be "str" type!')
    elif func_name == 'clone_olap_module':
        module, set_focus_on_copied_module, copied_module_name = args[0], args[1], args[2]
        if not isinstance(module, str):
            raise ValueError('Param "module" must be "str" type!')
        if not isinstance(set_focus_on_copied_module, bool):
            raise ValueError('Param "set_focus_on_copied_module" must be "bool" type!')
        if not isinstance(copied_module_name, str):
            raise ValueError('Param "copied_module_name" must be "str" type!')
    elif func_name == 'create_calculated_measure':
        measure_name, formula = args[0], args[1]
        def check_type_and_value(param_value: str, param_name: str):
            """
            Проверка типа и значения заданного параметра.
            Ничего не возвращает, но бросается ошибками.
            """
            if not isinstance(param_value, str):
                raise ValueError('Param "{}" must be "str" type!'.format(param_name))
            if not param_value:
                raise ValueError('Param "{}" has empty value!'.format(param_name))
        def check_new_name_param(measure_name: str):
            """
            Проверка имени создаваемого вычислимого факта на соответствие с названиями функций и логических операндов.
            Ничего не возвращает, но бросается ошибками.
            """
            lower_measure_name = measure_name.lower()
            if lower_measure_name in FUNCS or lower_measure_name in LOGIC_FUNCS or lower_measure_name == 'if':
                raise ValueError('Value "{}" of "new_name" parameter is invalid!'.format(measure_name))
        check_type_and_value(measure_name, 'new_name')
        check_type_and_value(formula, 'formula')
        check_new_name_param(measure_name)
    elif func_name == 'group_dimensions':
        group_name, items, position = args[0], args[1], args[2]
        # check "group_name" param
        if not isinstance(group_name, str):
            raise ValueError('Param "group_name" must be "str" type!')
        if not group_name:
            raise ValueError('Group name cannot be empty (param "group_name")!')
        # check items
        if not isinstance(items, (list, set, tuple)):
            raise ValueError('Param "dim_items" must be "list", "set" or "tuple" type!')
        # check position
        if position not in ["left", "top"]:
            raise ValueError('Param "position" must be either "left" or "top"!')
    elif func_name == 'wait_cube_loading':
        cube_name, time_sleep, max_attempt = args[0], args[1], args[2]
        # check cube_name
        if not isinstance(cube_name, str):
            raise ValueError('Param "cube_name" must be "str" type!')
        # check time_sleep
        if not isinstance(time_sleep, int):
            raise ValueError('Param "time_sleep" must be "int" type!')
        if time_sleep < 1:
            raise ValueError('Value of "time_sleep" param must be greater than 0!')
        # check max_attempt
        if max_attempt is not None and not isinstance(max_attempt, int):
            raise ValueError('Param "max_attempt" must be "int" type or None!')
        if isinstance(max_attempt, int) and max_attempt < 1:
            raise ValueError('Value of "max_attempt" param must be greater than 0!')
    else:
        raise ValueError("No function to check: {}".format(func_name))
