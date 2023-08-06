#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Реализация графика типа "Области".
"""

from ..base_graph import BaseGraph

class Areas(BaseGraph):
    """
    Реализация графика типа "Области".
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
            'axis_notes': <value>,
            'vertical_right_axix': <value>
        }
        """
        return self.get_actual_settings(['title_show', 'legend', 'axis', 'axis_notes', 'vertical_right_axix'])

    def _get_labels_settings(self) -> dict:
        """
        Получение настроек графика по параметру labels.
        :return: {'OX': <value>, 'OY': <value>, 'short_format': <value>}.
        """
        values_dict = {'OX': self.labels.get('OX', 10), 'OY': self.labels.get('OY', 10)}
        self.check_frequency_axis_5_30_5(values_dict)
        short_format = self.labels.get('short_format', False)
        if not self.check_bool(short_format):
            raise ValueError('Param "short_format" must be bool type!')
        values_dict.update({'short_format': short_format})
        return values_dict

    def draw(self):
        """
        Отрисовка графика. Состоит из нескольких этапов:
        1. Проверка данных для текущего типа графика;
        2. Формирование конфигурации графика;
        3. Вызов команды, отрисовывающей график.
        """
        # проверка данных и получение всех настроек
        self.check_olap_configuration(1, 0, 1, None)
        settings = self._get_settings()
        labels_settings = self._get_labels_settings()

        # получение базовых настроек и их дополнение на основе заданных пользователем значений
        graph_config = self.get_graph_config().copy()
        base_setting = {
            "titleShow": settings.get('title_show'),
            "legend": settings.get('legend'),
            "axis": settings.get('axis'),
            "axisNotes": settings.get('axis_notes'),
            "axisPosition": settings.get('vertical_right_axix'),
            "wireShow": self.grid,
            "axisNotesPeriodX": labels_settings.get('OX'),
            "axisNotesPeriodY": labels_settings.get('OY'),
            "axisXShortFormat": labels_settings.get('short_format')
        }
        graph_config['plotData'][self.graph_type]['config'].update({'base': base_setting})

        # и, наконец, сохраняя настройки, отрисовываем сам график
        self.save_graph_settings(graph_config)
