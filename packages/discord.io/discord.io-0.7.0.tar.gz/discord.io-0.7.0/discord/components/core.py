# -*- coding: utf-8 -*-
# cython: language_level=3
# Copyright (c) 2021-present VincentRPS

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE
import random
import string
import typing

from discord.state import ConnectionState

__all__: typing.List[str] = ["Button"]


class Button:
    def __init__(self, state: ConnectionState):
        self.state = state

    def create(
        self,
        label: str,
        style: typing.Literal[1, 2, 3, 4, 5] = 1,
        custom_id: str = None,
        url: str = None,
    ):
        self.id = (
            custom_id
            if custom_id is not None
            else "".join(
                random.choice(string.ascii_letters)
                for _ in range(random.randint(10, 100))
            )
        )

        ret = {
            "type": 1,
            "components": [
                {
                    "type": 2,
                    "label": label,
                    "style": style,
                    "url": url,
                    "custom_id": custom_id,
                }
            ],
        }

        return [ret]
