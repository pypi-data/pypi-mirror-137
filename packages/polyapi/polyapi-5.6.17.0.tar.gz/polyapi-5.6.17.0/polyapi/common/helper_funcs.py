#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Содержит набор вспомогательных классов и функций, использующихся в PPL.
"""

import logging
import time
from datetime import date, datetime
from typing import Any, Union, Callable
from .consts import TYPES_MAP, business_logic, time_type
from ..exceptions import *


class TypeConverter():
    """
    Реализация преобразования типов, определённых Полиматикой, к Python-типам.
    """
    def __init__(self, sc: business_logic, default_value: Any = None, convert_empty_values: bool = True):
        """
        Конструктор класса.
        :param sc: экземпляр класса BusinessLogic.
        :param default_value: (Any) дефолтное значение, использующееся в случае,
            если не удалось преобразовать исходные данные к нужному типу.
        :param convert_empty_values: (bool) нужно ли преобразовывать строки формата "(Пустой)"/"(Empty)"
            к дефолтному значению (см. default_value); по-умолчанию нужно.
        """
        self.sc = sc
        self.default_value = default_value
        self.convert_empty_values = convert_empty_values
        self.datetime_format = sc.get_current_datetime_format()

    def _convert_to_int(self, value: Any) -> Union[int, Any]:
        """
        Преобразование исходных данных в целочисленный тип.
        Если преобразование не удалось - вернутся данные в исходном виде.
        :param value: (Any) исходные данные.
        :return: (int) исходные данные в целочисленном типе.
        """
        try:
            result = int(value)
        except ValueError:
            result = self.default_value
        return result

    def _convert_to_float(self, value: Any) -> Union[float, Any]:
        """
        Преобразование исходных данных в тип дробных чисел.
        Если преобразование не удалось - вернутся данные в исходном виде.
        :param value: (Any) исходные данные.
        :return: (float) исходные данные в виде дробного числа.
        """
        try:
            result = float(value)
        except ValueError:
            result = self.default_value
        return result

    def _convert_to_string(self, value: Any) -> Union[str, Any]:
        """
        Преобразование исходных данных в строковый тип.
        Если преобразование не удалось - вернутся данные в исходном виде.
        :param value: (Any) исходные данные.
        :return: (float) исходные данные в строковом типе.
        """
        try:
            result = str(value)
        except ValueError:
            result = self.default_value
        return result

    def _convert_to_date(self, value: Any) -> Union[date, Any]:
        """
        Преобразование исходных данных в формат даты.
        Если преобразование не удалось - вернутся данные в исходном виде.
        :param value: (Any) исходные данные.
        :return: (int) исходные данные в формате даты.
        """
        # немного костыльный способ, но пока ничего лучше не придумал; если упадёт где-нибудь - будем разбираться
        date_format = self.datetime_format.split(' ')[0]
        try:
            result = datetime.strptime(value, date_format).date()
        except ValueError:
            result = self.default_value
        return result

    def _convert_to_time(self, value: Any) -> Union[time_type, Any]:
        """
        Преобразование исходных данных в формат времени.
        Если преобразование не удалось - вернутся данные в исходном виде.
        :param value: (Any) исходные данные.
        :return: (int) исходные данные в формате времени.
        """
        # немного костыльный способ, но пока ничего лучше не придумал; если упадёт где-нибудь - будем разбираться
        time_format = self.datetime_format.split(' ')[1]
        try:
            result = datetime.strptime(value, time_format).time()
        except ValueError:
            result = self.default_value
        return result

    def _convert_to_datetime(self, value: Any) -> Union[datetime, Any]:
        """
        Преобразование исходных данных в формат дата-время.
        Если преобразование не удалось - вернутся данные в исходном виде.
        :param value: (Any) исходные данные.
        :return: (int) исходные данные в формате дата-время.
        """
        try:
            result = datetime.strptime(value, self.datetime_format)
        except ValueError:
            result = self.default_value
        return result

    def convert_data_types(self, types: list, data: list) -> list:
        """
        Непосредственно функция преобразования типов, определённых Полиматикой, к Python-типам.
        :param types: (list) список используемых типов.
        :param data: (list) набор начальных данных.
        :return: (list) начальные данные, преобразованные к нужному типу.
        """
        convert_funcs_map = {
            'integer': self._convert_to_int,
            'float': self._convert_to_float,
            'string': self._convert_to_string,
            'date': self._convert_to_date,
            'time': self._convert_to_time,
            'datetime': self._convert_to_datetime
        }

        # по идее, в нормальной ситуации длина списков должна совпадать (длина списка типов равна количеству колонок, а
        # количество колонок должно совпадать с количеством данных); поэтому, если это не так - сгенерируем ошибку
        if len(types) != len(data):
            exception_func = raise_exception(self.sc)
            exception_func(
                PolymaticaException, 'Length of column list does not match length of data list!', with_traceback=False)

        # преобразовываем данные
        result = list()
        not_converted_values = [float('-inf'), float('inf')]
        empty_string_values = ['(пустой)', '(empty)']
        for item in tuple(zip(data, types)):
            # значение текущего поля
            item_value = item[0]

            # если встретился неконвертируемый тип данных - никаких преобразований делать не нужно, добавляем как есть
            if item_value in not_converted_values:
                result.append(item_value)
                continue

            # если встретилась одна из "пустых" строк и параметром задано, что нужно преобразовать - преобразовываем
            # строку, состоящую только из пробелов, также считаем пустой
            if self.convert_empty_values:
                str_item_value = str(item_value)
                if str_item_value.lower() in empty_string_values or str_item_value.strip() == str():
                    result.append(self.default_value)
                    continue

            # всё остальное конвертируем в нужные типы
            convert_func = convert_funcs_map.get(TYPES_MAP.get(item[1]))
            result.append(convert_func(item_value))
        return result


class JSONDecoder():
    """
    Изменение кодировки JSON-подобных структур. Используется при парсинге ответа от сервера (для обработки кириллицы).
    Конвертация происходит из кодировки, указанной в параметре "from_encoding" в кодировку, указанную в "to_encoding".
    """
    def __init__(self, from_encoding: str='latin1', to_encoding: str='utf8'):
        self._from_enc = from_encoding
        self._to_enc = to_encoding
        self._ord_list = self._get_ord_list()

    @property
    def from_enc(self) -> str:
        return self._from_enc

    @property
    def to_enc(self) -> str:
        return self._to_enc

    @property
    def char_order_list(self) -> list:
        return self._ord_list

    def _get_ord_list(self) -> list:
        """
        Получить числовые представления всех человеко-читаемых символов.
        """
        eng_symbols, rus_symbols = 'abcdefghijklmnopqrstuvwxyz', 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        digits = '0123456789'
        spec_symbols = ' .,+-*/<>()[]&^%$#@!"№;:=_?|\{\}\'\t\n\r\b\\'
        common_str = eng_symbols + eng_symbols.upper() + rus_symbols + rus_symbols.upper() + digits + spec_symbols
        return [ord(char) for char in common_str]

    def _need_to_decode(self, text: str) -> bool:
        """
        Определяем, нужно ли конвертировать строку из одной кодировки в другую.
        """
        for char in text:
            if ord(char) not in self.char_order_list:
                return True
        return False

    def _latin_to_utf8_decode(self, text: str) -> str:
        """
        Непосредственно само преобразование кодировок.
        """
        return text.encode(self.from_enc).decode(self.to_enc)

    def _decode_list(self, current_list: list):
        """
        Рекурсивная обработка списков.
        """
        for index, current_item in enumerate(current_list):
            if not current_item:
                continue
            if isinstance(current_item, str) and self._need_to_decode(current_item):
                current_list[index] = self._latin_to_utf8_decode(current_item)
            elif isinstance(current_item, (list, set)):
                self._decode_list(current_item)
            elif isinstance(current_item, dict):
                self._decode_dict(current_item)

    def _decode_dict(self, current_dict: dict):
        """
        Рекурсивная обработка словарей.
        """
        for key in list(current_dict.keys()):
            current_item = current_dict[key]
            if not current_item:
                continue
            if isinstance(current_item, str) and self._need_to_decode(current_item):
                current_dict[key] = self._latin_to_utf8_decode(current_item)
            elif isinstance(current_item, (list, set)):
                self._decode_list(current_item)
            elif isinstance(current_item, dict):
                self._decode_dict(current_item)

    def decode(self, current_json: Union[dict, list]):
        if isinstance(current_json, dict):
            self._decode_dict(current_json)
        elif isinstance(current_json, list):
            self._decode_list(current_json)
        else:
            raise DecodeError('Wrong JSON! Expected dict/list, JSON: {}'.format(current_json))


def timing(func: Callable) -> Callable:
    """
    Используется как декоратор функций класса BusinessLogic для профилирования времени работы.
    :param func: декорируемая функция.
    """
    def timing_wrap(self, *args, **kwargs) -> Any:
        """
        Непосредственно функция-декоратор.
        :param self: экземпляр класса BusinessLogic.
        """
        self.func_name = func.__name__
        try:
            logging.info('Exec func "{}"'.format(self.func_name))
            start_time = time.time()
            result = func(self, *args, **kwargs)
            end_time = time.time()
            self.func_timing = 'func "{}" exec time: {:.2f} sec'.format(self.func_name, (end_time - start_time))
            logging.info(self.func_timing)
            return result
        except SystemExit:
            logging.critical('Func "{}" failure with SystemExit exception!'.format(self.func_name))
            raise
    return timing_wrap


def raise_exception(bl_instance: business_logic):
    """
    Обёртка над функцией-генератором исключений.
    Сделано для того, чтобы каждый раз не передавать в функцию экземпляр класса "BusinessLogic".
    :param bl_instance: экземпляр класса BusinessLogic.
    """
    def wrap(exception: Exception, message: str, extend_message: str = '', code: int = 0, with_traceback: bool = True):
        """
        Непосредственно функция, генерирующая пользовательские исключения с заданным сообщением.

        :param exception: вид исключения, которое нужно сгенерировать. Например, ValueError, PolymaticaException...
        :param message: сообщение об ошибке.
        :param extend_message: расширенное сообщение об ошибке (не обязательно).
        :param code: код ошибки (не обязательно).
        :param with_traceback: нужно ли показывать traceback ошибки (по-умолчанию True).
            True актуально только в случае, если функция, генерирующая исключение, вызывается в блоке Except.
            В любом другом случае для корректности отображения ошибки необходимо задавать параметр False.
        :return: (str) сообщение об ошибке, если работа с API происходит через Jupyter Notebook;
            в противном случае генерируется ошибка.
        """
        bl_instance.current_exception = message

        # записываем сообщение в логи
        # logging.error(msg, exc_info=True) аналогичен вызову logging.exception(msg) - вывод с трассировкой ошибки
        # logging.error(msg, exc_info=False) аналогичен вызову logging.error(msg) - вывод без трассировки ошибки
        logging.error(message, exc_info=with_traceback)
        logging.info("APPLICATION STOPPED")

        # если работа с API происходит через Jupyter Notebook, то выведем просто сообщение об ошибке
        if bl_instance.jupiter:
            return message

        # если текущее исключение является наследником класса PolymaticaException, то генерируем ошибку Полиматики
        if issubclass(exception, PolymaticaException):
            raise exception(message, extend_message, code)

        # прочие (стандартные) исключения, по типу ValueError, IndexError и тд
        raise exception(message)
    return wrap


def log(message: str, level: str = 'info'):
    """
    Запись сообщения в логи.
    :param message: сообщение, записываемое в логи.
    :param level: уровень логирования; возможны варианты: 'debug', 'info', 'warning', 'error', 'critical'.
        По-умолчанию 'info'.
    """
    level = level.lower()
    if level not in ['debug', 'info', 'warning', 'error', 'critical']:
        level = 'info'
    if level == 'debug':
        logging.debug(message)
    elif level == 'info':
        logging.info(message)
    elif level == 'warning':
        logging.warning(message)
    elif level == 'error':
        logging.error(message)
    elif level == 'critical':
        logging.critical(message)
