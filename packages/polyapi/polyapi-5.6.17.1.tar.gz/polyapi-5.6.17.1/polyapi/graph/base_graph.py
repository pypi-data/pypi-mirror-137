#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Описание базового класса работы с графиками.
"""

import re
from typing import Union, Any, Callable
from ..common import business_logic

class BaseGraph():
    """
    Класс, являющийся общим предком для всех типов графиков. Содержит обобщённые методы работы с графиками.
    """
    def __init__(self, base_bl: business_logic, settings: str, grid: str, labels: dict, other: dict,
                common_params: dict, graph_type: str, int_type: int):
        # экземпляр класса BusinessLogic
        self._base_bl = base_bl
        # битмап настроек
        self._settings = settings
        # настройки сетки
        self._grid = grid
        # настройки подписи на графиках
        self._labels = labels
        # прочие настройки, зависящие от графиков
        self._other = other
        # идентификатор OLAP-модуля, идентификатор модуля графиков, конфигурация OLAP-модуля и размеры окна графиков
        # содержит поля: "olap_module_id", "graph_module_id", "olap_config" и "module_size"
        self._common_params = common_params
        # тип графика (строковый), используется при формировании общего конфига
        self._graph_type = graph_type
        # целочисленный тип графика, определён Полиматикой в server-codes.json (если не задан, то используется -1)
        self._int_type = int_type
        # название графика
        self._graph_name = other.get('name', False)

    @property
    def base_bl(self) -> business_logic:
        return self._base_bl

    @property
    def settings(self) -> str:
        return self._settings

    @property
    def grid(self) -> str:
        return self._grid

    @property
    def labels(self) -> dict:
        return self._labels

    @property
    def other(self) -> dict:
        return self._other

    @property
    def common_params(self) -> dict:
        return self._common_params

    @property
    def graph_type(self) -> str:
        return self._graph_type

    @property
    def int_type(self) -> int:
        return self._int_type

    @property
    def graph_name(self) -> str:
        return self._graph_name

    @property
    def default_color(self) -> str:
        return '#00afd7'

    def _check_frequency_impl(self, check_func: Callable, axis_values: dict, start: int, end: int, step: int):
        """
        Реализация проверки значения частоты подписей по осям. Если проверка не пройдена - сгенерируется исключение.
        :param check_func: проверяющая функция, которая возвращает True, если проверка не пройдена.
        :param axis_values: данные частоты подписей по осям.
        :param start: начало диапазона.
        :param end: конец диапазона.
        :param step: шаг.
        """
        for axis in axis_values:
            axis_value = axis_values.get(axis)
            if not isinstance(axis_value, (int, float)):
                raise ValueError("Axis value must be int or float type!")
            if check_func(axis_value):
                params = [axis, start, end, step]
                raise ValueError("Axis {} frequency must be set in interval [{}, {}] with step {}!".format(*params))

    def check_olap_configuration(self, left_dims_count: int, top_dims_count: int, fact_count: int, marked: bool):
        """
        Сверка текущей конфигурации OLAP-модуля на соответствие заданному типу графика.
        :param left_dims_count: минимальное количество левых размерностей, требующихся для построения графика.
            Т.е. в мультисфере количество левых размерностей должно быть больше или равно заданному значению.
        :param top_dims_count: минимальное количество верхних размерностей, требующихся для построения графика.
            Т.е. в мультисфере количество верхних размерностей должно быть больше или равно заданному значению.
        :param fact_count: минимальное количество фактов, требующихся для построения графика.
            Т.е. в мультисфере количество фактов должно быть больше или равно заданному значению.
        :param marked: должны ли быть отметки фактов (выделения строк) в OLAP-модуле.
            Отметки фактов в обязательном порядке требуются для построения некоторых типов графиков. В этом случае
            значение параметра должно быть True/False.
            Для остальных типов графиков отметка не обязательна - она может как быть, так и не быть (графики построятся
            в любом случае). В этом случае значение параметра должно быть None.
        """
        # olap_config имеет поля: 'top_dim_count', 'left_dim_count', 'fact_count', 'marked'
        olap_config = self.common_params.get('olap_config')
        if olap_config.get('left_dim_count') < left_dims_count or olap_config.get('top_dim_count') < top_dims_count or \
            olap_config.get('fact_count') < fact_count or marked is not None and olap_config.get('marked') != marked:
            raise ValueError('Graph cannot be draw with current OLAP configuration!')

    def get_actual_settings(self, field_names: list) -> dict:
        """
        Преобразование (по типу "0" -> False, "1" -> True) битмапа настроек в реальные настройки графиков.
        :param field_names: названия полей, в которые нужно преобразовать настройки из битмапа.
        :return: словарь, содержащий реальные настройки.
        :example: bitmap="1101", field_names=['arg1', 'arg2', 'arg3', 'arfg4'] ->
            {'arg1': True, 'arg2': True, 'arg3': False, 'arg4': True}
        """
        # если передано неверное число настроек - бросаем ошибку
        if len(self.settings) != len(field_names):
            raise ValueError("Settings length can only equals {} for this graph type!".format(len(field_names)))
        return {field: bool(int(self.settings[i])) for i, field in enumerate(field_names)}

    def check_frequency_axis_5_30_5(self, axis_values: dict):
        """
        Реализация проверки значения частоты подписей по осям.
        Паттерн проверки: значения могут быть от 5 до 30 с шагом 5.
        :param axis_values: данные частоты подписей по осям.
        """
        self._check_frequency_impl(lambda item: item % 5 != 0 or item < 5 or item > 30, axis_values, 5, 30, 5)

    def check_frequency_axis_1_10_05(self, axis_values: dict):
        """
        Реализация проверки значения частоты подписей по осям.
        Паттерн проверки: значения могут быть от 1 до 10 с шагом 0.5.
        :param axis_values: данные частоты подписей по осям.
        """
        self._check_frequency_impl(
            lambda item: round(item * 10) % 5 != 0 or item < 1 or item > 10, axis_values, 1, 10, 0.5)

    def check_bool(self, value: Any) -> bool:
        """
        Проверка значения на булевский тип.
        :param value: проверяемое значение.
        """
        return isinstance(value, bool)

    def check_str(self, value: Any) -> bool:
        """
        Проверка значения на строковый тип.
        :param value: проверяемое значение.
        """
        return isinstance(value, str)

    def check_dict(self, value: Any) -> bool:
        """
        Проверка значения на словарь.
        :param value: проверяемое значение.
        """
        return isinstance(value, dict)

    def check_list(self, value: Any) -> bool:
        """
        Проверка значения на список.
        :param value: проверяемое значение.
        """
        return isinstance(value, list)

    def check_interval_with_step(self, name: str, value: Union[int, float], interval: tuple, step: Union[int, float]):
        """
        Проверка заданного значения на вхождение в интервал с заданным шагом.
        Ничего не возвращает, но может сгенерировать исключение.
        :param name: название параметра
        :param value: значение параметра (может быть как целочисленным, так и нет)
        :param interval: интервал, в который должно входить значение; имеет вид (a, b)
        :param step: шаг значений на интервале (может быть как целочисленным, так и нет)
        """
        # определяем проверяющую функцию, которая возвращает True, если значение не подходит под заданный паттерн
        if interval == (0, 1) and step == 0.01:
            check_func = lambda item: item * 100 not in range(0, 101) or item < 0 or item > 1
        elif interval == (0, 1) and step == 0.05:
            check_func = lambda item: round(item * 100) % 5 != 0 or item < 0 or item > 1
        elif interval == (1, 20) and step == 0.5:
            check_func = lambda item: round(item * 10) % 5 != 0 or item < 1 or item > 20
        elif interval == (0.5, 5) and step == 0.1:
            check_func = lambda item: item * 10 not in range(5, 51) or item < 0.5 or item > 5
        elif interval == (1, 5) and step == 0.1:
            check_func = lambda item: item * 10 not in range(10, 51) or item < 1 or item > 5
        elif interval == (1, 10) and step == 0.1:
            check_func = lambda item: item * 10 not in range(10, 101) or item < 1 or item > 10
        elif interval == (5, 10) and step == 0.1:
            check_func = lambda item: item * 10 not in range(50, 101) or item < 5 or item > 10
        elif interval == (5, 15) and step == 0.1:
            check_func = lambda item: item * 10 not in range(50, 151) or item < 5 or item > 15
        elif interval == (0, 5) and step == 1:
            check_func = lambda item: item not in range(0, 6)
        elif interval == (1, 50) and step == 1:
            check_func = lambda item: item not in range(1, 51)
        elif interval == (0, 100) and step == 1:
            check_func = lambda item: item not in range(0, 101)
        elif interval == (7, 15) and step == 1:
            check_func = lambda item: item not in range(7, 16)
        elif interval == (4, 48) and step == 1:
            check_func = lambda item: item not in range(4, 49)
        else:
            return
        # если проверка пройдена - генерируем ошибку
        if check_func(value):
            msg = 'Param "{}" must be set in interval [{}, {}] with step {}!'.format(
                name, interval[0], interval[1], step)
            raise ValueError(msg)

    def check_range_with_step(self, name: str, value: tuple, interval: tuple, step: Union[int, float]):
        """
        Проверка заданного диапазона. Суть проверки:
            1. Нижняя граница диапазона должна быть меньше или равна верхней границе.
            2. И нижняя, и верхняя граница входят в диапазон, заданный в параметрах min_value и max_value соотв.
        Ничего не возвращает, но может сгенерировать исключение.
        :param name: название параметра
        :param value: значение параметра
        :param interval: интервал, в который должно входить значение верхней и нижней границы; имеет вид (a, b)
        :param step: шаг значений на интервале (может быть как целочисленным, так и нет)
        """
        error_msg = str()
        min_value, max_value = value[0], value[1]
        if max_value < min_value:
            error_msg = 'top range border should not be less than the bottom range border!'
        try:
            self.check_interval_with_step(name, min_value, interval, step)
            self.check_interval_with_step(name, max_value, interval, step)
        except ValueError:
            error_msg = 'borders must be set in interval [{}, {}] with step {}!'.format(interval[0], interval[1], step)
        if error_msg:
            raise ValueError('Wrong param "{}": {}'.format(name, error_msg))

    def check_color(self, color: str):
        """
        Проверка соответствия цвета шаблону "#rrggbb".
        Ничего не возвращает, но может сгенерировать исключение вследствие провалившейся проверки.
        """
        color_reg = re.compile(r'^#[0-9a-fA-F]{6}$')
        if not color_reg.match(color):
            raise ValueError('Wrong color: "{}"! Color pattern: "#RRGGBB"!'.format(color))

    def save_graph_settings(self, graph_config: dict):
        """
        Сохранение настроек графика посредством вызова команды ("user_iface", "save_settings").
        """
        self.base_bl.execute_manager_command(
            command_name="user_iface",
            state="save_settings",
            module_id=self.common_params.get('graph_module_id'),
            settings=graph_config
        )

    def get_graph_config(self) -> dict:
        """
        Возвращает основную часть настроек графика (то есть ту часть, которая не параметризуется пользователем).
        :return: Основная часть конфигурации графика.
        """
        module_size = self.common_params.get('module_size')
        graph_settings = {
            # строковый идентификатор графика
            "plotName": self.graph_type,
            # размеры окна
            "geometry": {"width": module_size.get('width'), "height": module_size.get('height')},
            # конфигурация графика
            "plotData": {
                self.graph_type: {
                    # тут будет прописан конфиг, сформированный на основе настроек, заданных пользователем
                    "config": {
                    },
                    # в этом блоке задаём имя графику; остальное неизвестно, для чего, но нужно
                    "state": {
                        "colors": {
                            "facts": {}
                        },
                        "title": self.graph_name,
                        "zoom": {
                            "k": 1,
                            "x": 0,
                            "y": 0,
                            "z": 0
                        }
                    },
                    # для некоторых типов графиков указывается информация об отображаемом множестве верхних размерностей
                    "query": {}
                }
            }
        }
        return graph_settings
