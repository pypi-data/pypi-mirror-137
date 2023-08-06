#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Реализация графика типа "Шары".
"""

from ..base_graph import BaseGraph

class Balls(BaseGraph):
    """
    Реализация графика типа "Шары".
    """
    def __init__(self, base_bl: 'BusinessLogic', settings: str, grid: str, labels: dict,
                other: dict, common_params: dict, plot_type: str):
        super().__init__(base_bl, settings, grid, labels, other, common_params, plot_type, -1)

    def _get_settings(self) -> dict:
        """
        Получение актуальных настроек по заданному битмапу.
        :return: {
            'title_show': <value>,
            'legend': <value>,
            'axis': <value>,
            'axis_notes': <value>
        }
        """
        return self.get_actual_settings(['title_show', 'legend', 'axis', 'axis_notes'])

    def _get_labels_settings(self) -> dict:
        """
        Получение настроек графика по параметру labels.
        :return: {'OX': <value>, 'OY': <value>, 'OZ': <value>}.
        """
        values_dict = {
            'OX': self.labels.get('OX', 2.5), 'OY': self.labels.get('OY', 2.5), 'OZ': self.labels.get('OZ', 2.5)}
        self.check_frequency_axis_1_10_05(values_dict)
        return values_dict

    def _get_other_settings(self) -> dict:
        """
        Получение прочих настроек графика.
        :return: {'show_shadows': <value>, 'diameter_range': <value>, 'diameter': <value>, 'shadows_color': <value>}.
        """
        # получаем параметры
        show_shadows = self.other.get('show_shadows', True)
        diameter_range = self.other.get('diameter_range', (4, 48))
        diameter = self.other.get('diameter', 4)

        # проверяем значения и возвращаем их
        if not self.check_bool(show_shadows):
            raise ValueError('Param "show_shadows" must be bool type!')
        self.check_range_with_step('diameter_range', diameter_range, (4, 48), 1)
        self.check_interval_with_step('diameter', diameter, (4, 48), 1)
        return {
            "show_shadows": show_shadows,
            "diameter_range": list(diameter_range),
            "diameter": diameter,
            "shadows_color": "#cccccc"
        }

    def draw(self):
        """
        Отрисовка графика. Состоит из нескольких этапов:
        1. Проверка данных для текущего типа графика;
        2. Формирование конфигурации графика;
        3. Вызов команды, отрисовывающей график.
        """
        # проверка данных и получение всех настроек
        self.check_olap_configuration(1, 0, 3, True)
        settings = self._get_settings()
        labels_settings = self._get_labels_settings()
        other_settings = self._get_other_settings()

        # получение базовых настроек и их дополнение на основе заданных пользователем значений
        graph_config = self.get_graph_config().copy()
        base_setting = {
            "titleShow": settings.get('title_show'),
            "legend": settings.get('legend'),
            "axis": settings.get('axis'),
            "axisNotes": settings.get('axis_notes'),
            "axisNotesPeriodX": labels_settings.get('OX'),
            "axisNotesPeriodY": labels_settings.get('OY'),
            "axisNotesPeriodZ": labels_settings.get('OZ'),
            "shadowsColor": other_settings.get('shadows_color')
        }
        spheres_setting = {
            "defaultSize": other_settings.get('diameter'),
            "shadowsVisible": other_settings.get('show_shadows'),
            "size": other_settings.get('diameter_range')
        }
        graph_config['plotData'][self.graph_type]['config'].update({'base': base_setting, 'spheres': spheres_setting})

        # и, наконец, сохраняя настройки, отрисовываем сам график
        self.save_graph_settings(graph_config)
