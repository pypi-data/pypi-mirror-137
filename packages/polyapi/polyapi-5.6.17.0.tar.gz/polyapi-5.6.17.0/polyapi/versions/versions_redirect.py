#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Описание класса, вызывающего те или иные реализации методов бизнес-сценариев Полиматики в зависимости от версии """

from .polymatica_57 import Polymatica57


class VersionRedirect():
    def __init__(self, base_bs):
        self.current_version = base_bs.polymatica_version
        self.polymatica_56_bs = base_bs
        self.polymatica_57_bs = Polymatica57(base_bs)

    def _prepare_method_name(self, method_name):
        """
        Т.к. бывают внутренние методы, их названия начинаются с нижнего подчёркивания.
        Для версий Полиматики, отличных от 5.6, обрезаем у имён методов это нижнее подчёркивание, если оно есть.
        """
        if self.current_version == '5.6':
            return method_name
        return method_name[1:] if method_name[0] == '_' else method_name

    def invoke_method(self, method, *args, **kwargs):
        """ Вызов определённой реализации заданного метода в зависимости от версии Полиматики """
        method_name = self._prepare_method_name(method)
        if self.current_version == '5.7':
            result = getattr(self.polymatica_57_bs, method_name)(*args, **kwargs)
        else:
            result = getattr(self.polymatica_56_bs, method_name)(*args, **kwargs)
        return result
