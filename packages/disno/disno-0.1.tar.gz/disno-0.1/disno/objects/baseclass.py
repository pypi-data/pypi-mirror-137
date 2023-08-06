"""
MIT License

Copyright (c) 2021-present Qwire Development Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import types
from typing import Union

class BaseObject:
    def __init__(self, **kwargs):
        attrs = self.__annotations__

        for name, _type in attrs.items():
            obj = kwargs.get(name, None)
            if obj == None:
                if isinstance(_type, bool):
                    setattr(self, name, False)
                elif not self._is_typing_optional(_type):
                    raise TypeError(f"\"{name}\" is a missing parameter.")
                else:
                    setattr(self, name, None)
            else:
                if self._is_typing_optional(_type):
                    raise_if_fail = False
                    _type = _type.__args__[0]
                else:
                    raise_if_fail = True

                if self._is_typing_union(_type):
                    converters = _type.__args__
                else:
                    converters = []

                def convert(_obj, _convs, _rif):
                    for c in _convs:
                        try:
                            if isinstance(_obj, dict):
                                _obj = c(**_obj)
                            else:
                                _obj = c(_obj)
                        except:
                            continue
                        else:
                            break
                    else:
                        if not len(_convs) == 0:
                            if _rif:
                                raise TypeError(f"Converters for \"{name}\" failed.")

                if self._is_typing_list(_type):
                    converted = []
                    for o in obj:
                        o = convert(o, converters, raise_if_fail)
                        converted.append(o)
                    setattr(self, name, converted)
                else:
                    o = convert(o, converters, raise_if_fail)
                    setattr(self, name, o)

    def _is_typing_union(self, annotation):
        return (
            getattr(annotation, '__origin__', None) is Union
            or type(annotation) is getattr(types, "UnionType", Union)
        )

    def _is_typing_optional(self, annotation):
        return self._is_typing_union(annotation) and type(None) in annotation.__args__

    def _is_typing_list(self, annotation):
        return getattr(annotation, '_name', None) == 'List'

    def to_json(self):
        payload = {}
        for name in dir(self):
            if not name.startswith("_"):
                attr = getattr(self, name)
                if issubclass(attr, BaseObject):
                    payload[name] = attr.to_json()
                elif isinstance(attr, list):
                    items = []
                    for i in attr:
                        if issubclass(i, BaseObject):
                            items.append(i.to_json())
                        else:
                            items.append(i)
                    payload[name] = items
                else:
                    payload[name] = attr
        return payload
