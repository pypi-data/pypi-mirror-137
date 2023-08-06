#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Описание интерфейсного класса, предназначенного для внешних вызовов.
"""
from typing import Any, List, Union
from ..common import GRAPH_ID, business_logic, graph
from .types import Lines, Cylinders, CumulativeCylinders, Point, PointSeries, Chord, Sankey, \
    Circles, CirclesSeries, Radar, Pools, Pools3D, Balls, Areas, CumulativeAreas, Pies, Graph, Surface, Corridors


class IGraph():
    """Класс, реализующий интерфейс взаимодействия пользователя с графиками"""
    def __init__(self, base_bl: business_logic, graph_type: Union[int, str], settings: str, grid: int,
                labels: dict, other: dict, current_id: str, m_size: dict):
        # экземпляр класса BusinessLogic
        self._base_bl = base_bl
        # тип графика (в виде строки), задающийся пользователем; если заданного типа не существует -
        # будет сгенерирована ошибка; является общим параметром для всех типов графиков
        self._graph_type = self._get_graph_type(graph_type)
        # проверка заданного типа графика на принадлежность заданной версии Полиматики
        self._check_polymatica_version()
        # тип строящегося графика, принимаемый Полиматикой
        self._plot_type = self._get_plot_type()
        # битмап настроек;
        # конкретные настройки для каждого типа графика извлекаются непосредственно в соответствующих классах
        settings = settings or self._get_default_settings()
        self._check_setting_bitmap(settings)
        self._settings = settings
        # настройки сетки; общий параметр для всех типов графиков
        self._grid = self._get_grid(grid)
        # настройки подписи на графиках;
        # конкретные настройки для каждого типа графика извлекаются непосредственно в соотв. классах
        self._check_type(labels, dict, 'labels')
        self._labels = labels
        # прочие настройки; конкретные настройки для каждого типа графика извлекаются непосредственно в соотв. классах
        self._check_type(other, dict, 'other')
        self._other = other
        # идентификатор мультисферы (если график создаётся) или идентификатор графика (если график изменяется)
        self._current_id = current_id
        # настройки ширины/высоты окна
        self._check_type(m_size, dict, 'm_size')
        self._m_size = m_size

    def _get_graph_type(self, graph_type: Union[int, str]) -> str:
        """
        Проверка типа графика. Возвращает тип графика в виде строки.
        """
        int_type_map = {
            1: 'lines',
            2: 'cylinders',
            3: 'cumulative_cylinders',
            4: 'areas',
            5: 'cumulative_areas',
            6: 'pies',
            7: 'radar',
            8: 'circles',
            9: 'circles_series',
            10: 'balls',
            11: 'pools',
            12: '3d_pools',
            13: 'corridors',
            14: 'surface',
            15: 'graph',
            16: 'sankey',
            17: 'chord',
            18: 'point',
            19: 'point_series'
        }
        if isinstance(graph_type, int):
            if graph_type not in int_type_map:
                raise ValueError('Graph type "{}" does not exists!'.format(graph_type))
            return int_type_map.get(graph_type)
        elif isinstance(graph_type, str):
            if graph_type not in list(int_type_map.values()):
                raise ValueError('Graph type "{}" does not exists!'.format(graph_type))
            return graph_type
        else:
            raise ValueError('Param "g_type" must be string or int!')

    def _check_polymatica_version(self):
        """
        Проверка заданного типа графики на совместимость с версией Полиматики.
        Некоторые типы графиков на определённых версиях Полиматики могут быть не доступны.
        """
        not_supported_types_by_versions = {
            '5.7': ('circles_series', 'point_series')
        }
        for poly_version in not_supported_types_by_versions:
            if self._base_bl.polymatica_version == poly_version and \
                self._graph_type in not_supported_types_by_versions.get(poly_version):
                raise ValueError(
                    'Type "{}" of graph is not supported on Polymatica {}!'.format(self._graph_type, poly_version))

    def _get_plot_type(self) -> str:
        """
        Возвращает тип графика, принимаемый Полиматикой. Как правило, названия таких типов начинаются с "plot-".
        """
        # мапа типов для Полиматики версии 5.6
        _5_6_types_map = {
            'lines': 'plot-2d-lines',
            'cylinders': 'plot-cylinder',
            'cumulative_cylinders': 'plot-stacked-bars',
            'areas': 'plot-area',
            'cumulative_areas': 'plot-stacked-area',
            'pies': 'plot-pies',
            'radar': 'plot-radar',
            'circles': 'plot-bubbles',
            'circles_series': 'plot-bubbles-multiple',
            'balls': 'plot-spheres',
            'pools': 'plot-pools',
            '3d_pools': 'plot-pools-3d',
            'corridors': 'plot-2d-tubes',
            'surface': 'plot-surface',
            'graph': 'plot-graph',
            'sankey': 'plot-sankey',
            'chord': 'plot-chord',
            'point': 'plot-scatter-single',
            'point_series': 'plot-scatter'
        }

        # мапа типов для Полиматики версии 5.6
        _5_7_types_map = _5_6_types_map.copy()
        del _5_7_types_map['circles_series']
        del _5_7_types_map['point_series']
        _5_7_types_map.update({'point': 'plot-scatter'})

        # получаем нужный тип графика
        version_plot_map = {
            '5.6': _5_6_types_map,
            '5.7': _5_7_types_map
        }
        return version_plot_map.get(self._base_bl.polymatica_version).get(self._graph_type)

    def _get_graph_instance(self) -> graph:
        """
        Возвращает необходимый класс в зависимости от типа графика.
        """
        class_map = {
            'lines': Lines,
            'cylinders': Cylinders,
            'cumulative_cylinders': CumulativeCylinders,
            'areas': Areas,
            'cumulative_areas': CumulativeAreas,
            'pies': Pies,
            'radar': Radar,
            'circles': Circles,
            'circles_series': CirclesSeries,
            'balls': Balls,
            'pools': Pools,
            '3d_pools': Pools3D,
            'corridors': Corridors,
            'surface': Surface,
            'graph': Graph,
            'sankey': Sankey,
            'chord': Chord,
            'point': Point,
            'point_series': PointSeries
        }
        return class_map.get(self._graph_type)

    def _get_default_settings(self) -> str:
        """
        Возвращает настройки графиков по-умолчанию в зависимости от типа графика.
        """
        settings_map = {
            'lines': "11110",
            'cylinders': "11110",
            'cumulative_cylinders': "11110",
            'areas': "11110",
            'cumulative_areas': "11110",
            'pies': "111",
            'radar': "1111",
            'circles': "11110",
            'circles_series': "11110",
            'balls': "1111",
            'pools': "11110",
            '3d_pools': "1111",
            'corridors': "11110",
            'surface': "111",
            'graph': "11",
            'sankey': "1",
            'chord': "11",
            'point': "11110",
            'point_series': "11110"
        }
        return settings_map.get(self._graph_type)

    def _check_setting_bitmap(self, settings_bitmap: str):
        """
        Проверка правильности задания настроек.
        """
        try:
            int(settings_bitmap, 2)
        except ValueError:
            raise ValueError("Settings string can only contain 0 or 1!")

    def _get_grid(self, grid: int) -> str:
        """
        Получение значения сетки (если это поддерживается заданным типом графика).
        """
        # для указанных типов графиков не нужно задавать значение сетки - пропускаем их
        # пропустить параметр означает не отобразить его в итоговой конфигурации графика
        if self._graph_type in ['pies', 'radar', 'balls', '3d_pools', 'surface', 'graph', 'sankey', 'chord']:
            return str()

        # интерпретируем значение для использования в графиках
        grids = {
            0: "all",  # Все линии
            1: "h",    # Горизонтальные линии
            2: "v",    # Вертикальные линии
            3: "none"  # Без сетки
        }
        if grid not in grids:
            raise ValueError("Grid value can only be Integer and be in range [0, 3]!")
        return grids.get(grid)

    def _check_type(self, value: Any, type_: Union[dict, tuple, list], param_name: str):
        """
        Проверка значения на заданный тип. Возвращает ошибку, если проверка не пройдена.
        :param value: произвольное значение.
        :param type_: допустимый тип.
        :param param_name: название параметра, передаваемого в value.
        """
        if not isinstance(value, type_):
            type_map = {
                dict: 'dict',
                tuple: 'tuple',
                list: 'list'
            }
            raise ValueError('Param "{}" can only be {}!'.format(param_name, type_map.get(type_)))

    def _get_olap_module_config(self, module_id: str) -> dict:
        """
        Получение конфигурации заданного OLAP-модуля.
        :param module_id: идентификатор OLAP-модуля.
        :return: конфигурация в виде {'top_dim_count': <>, 'left_dim_count': <>, 'fact_count': <>, 'marked': <>}.
        """
        config = {'top_dim_count': 0, 'left_dim_count': 0, 'fact_count': 0, 'marked': False}

        # т.к. заданный пользователем OLAP-модуль может отличаться от текущего активного OLAP-модуля,
        # то делаем временную подмену для получения актуальных данных
        old_ms_module_id = self._base_bl.multisphere_module_id
        self._base_bl._set_multisphere_module_id(module_id)
        result = self._base_bl.get_multisphere_data()
        self._base_bl._set_multisphere_module_id(old_ms_module_id)

        # данные по размерностям обоих уровней
        for item in result.get('dimensions'):
            position = item.get('position')
            if position == 1:
                config['left_dim_count'] += 1
            if position == 2:
                config['top_dim_count'] += 1

        # данные по фактам
        for item in result.get('facts'):
            if item.get('visible'):
                config['fact_count'] += 1

        # данные по меткам (в данном случае неважно, сколько их; важно, чтобы была хотя бы одна)
        mark_result = self._base_bl.execute_olap_command(
            command_name="view", state="get", from_col=0, from_row=0, num_col=100, num_row=100)
        mark_result_data = self._base_bl.h.parse_result(mark_result, 'left')
        for item in mark_result_data:
            if len(item) > 0 and item[0].get('flags', 0) != 0:
                config['marked'] = True
                break
        return config

    def _get_size_param(self, fields: List, min_value: int, default: int) -> int:
        """
        Проверка значения заданной размерности на соответствие минимальному значению. Если проверка не пройдена -
        будет сгенерирована ошибка.
        :param fields: (list) список ключей, по которым можно извлечь необходимую размерность;
            гарантированно содержит только два элемента: на первом месте - полное наименование параметра (height/width),
            на втором - сокращённое (h/w).
        :param min_value: (int) минимальное значение заданной размерности.
        :param default: (int) значение по-умолчанию, если заданная размерность не указана.
        :return: (int) размер окна для заданной размерности (высота, ширина).
        """
        size_value = self._m_size.get(fields[0], self._m_size.get(fields[1], default))
        if size_value < min_value:
            raise ValueError('Value of parameter "{}" is below the minimum ({})!'.format(fields[0], min_value))
        return size_value

    def create(self) -> str:
        """
        Создание нового графика с заданными параметрами.
        """
        # получаем идентификатор слоя и OLAP-модуля
        layer_id, olap_module_id = self._base_bl._find_olap_module(self._current_id)
        if not olap_module_id:
            if self._current_id:
                error_msg = 'OLAP module "{}" not found!'.format(self._current_id)
            else:
                error_msg = 'OLAP module not exists!'
            raise ValueError(error_msg)

        # создаём новое окно, сохраняем идентификатор модуля графиков
        res = self._base_bl.execute_manager_command(
            command_name="user_iface",
            state="create_module",
            module_id=olap_module_id,
            module_type=GRAPH_ID,
            layer_id=layer_id,
            after_module_id=olap_module_id
        )
        graph_module_uuid = self._base_bl.h.parse_result(res, 'module_desc', 'uuid')

        # определяем тип конкретного графика
        graph = self._get_graph_instance()
        try:
            # запаковываем в словарь все необходимые данные, в т.ч. конфигурацию OLAP-модуля
            common_params = {
                'olap_module_id': olap_module_id,
                'graph_module_id': graph_module_uuid,
                'olap_config': self._get_olap_module_config(olap_module_id),
                'module_size': {
                    'height': self._get_size_param(['height', 'h'], 240, 540),
                    'width': self._get_size_param(['width', 'w'], 840, 840)
                }
            }

            # отрисовываем график на созданном окне
            graph(
                self._base_bl,
                self._settings,
                self._grid,
                self._labels,
                self._other,
                common_params,
                self._plot_type
            ).draw()
        except Exception:
            # если не удалось отрисовать график с заданными параметрами - закрываем созданное окно графиков
            self._base_bl.execute_manager_command(
                command_name='user_iface', state='close_module', module_id=graph_module_uuid)
            raise
        return graph_module_uuid

    def update(self) -> str:
        """
        Изменение уже существующего графика по заданным параметрам.
        """
        # проверка, существует ли график с заданным идентификатором
        layer_id, graph_module_id = self._base_bl._find_graph_module(self._current_id)
        if not graph_module_id:
            if self._current_id:
                error_msg = 'Graph "{}" not found!'.format(self._current_id)
            else:
                error_msg = 'Graph module not exists!'
            raise ValueError(error_msg)

        # получаем идентификатор OLAP-модуля, на основе которого построен график
        layer_settings = self._base_bl.execute_manager_command(
            command_name="user_layer", state="get_layer", layer_id=layer_id)
        layer_modules = self._base_bl.h.parse_result(
            result=layer_settings, key="layer", nested_key="module_descs") or list()
        olap_module_id = str()
        for module in layer_modules:
            if module.get('uuid') == graph_module_id:
                olap_module_id = module.get('parent')
                break
        if not olap_module_id:
            raise ValueError('OLAP module for graph "{}" not found!'.format(graph_module_id))

        # определяем тип конкретного графика
        graph = self._get_graph_instance()
        try:
            # запаковываем в словарь все необходимые данные, в т.ч. конфигурацию OLAP-модуля
            common_params = {
                'olap_module_id': olap_module_id,
                'graph_module_id': graph_module_id,
                'olap_config': self._get_olap_module_config(olap_module_id),
                'module_size': {
                    'height': self._get_size_param(['height', 'h'], 240, 540),
                    'width': self._get_size_param(['width', 'w'], 840, 840)
                }
            }

            # отрисовываем график на созданном окне
            graph(
                self._base_bl,
                self._settings,
                self._grid,
                self._labels,
                self._other,
                common_params,
                self._plot_type
            ).draw()
        except Exception:
            # если не удалось отрисовать график с заданными параметрами - закрывать созданное окно графиков не нужно,
            # т.к. оно уже было создано ранее (не в этом методе)
            raise
        return graph_module_id
