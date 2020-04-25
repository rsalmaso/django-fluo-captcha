# Copyright (C) 2007-2020, Raffaele Salmaso <raffaele@salmaso.org>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from .utils import get_new_values, encode
from . import settings


OPERATORS = list(settings.OPERATIONS)


class CaptchaWidget(forms.MultiWidget):
    output = "<span class=\"{question_class}\">{question}</span>{text_input}{hidden_input}"
    values = settings.NUMBERS
    operators = OPERATORS
    question = _("Are you human? What is {x} {operator} {y}? ")
    question_class = "captcha-question"

    def __init__(self, values=None, operators=None, question=None, question_class=None, attrs=None):
        self.values = values or self.values
        self.operators = operators or self.operators
        self.question_class = question_class or self.question_class
        self.question_tmpl = question or self.question
        widget_attrs = {"size": "5"}
        widget_attrs.update(attrs or {})
        widgets = [
            forms.TextInput(attrs=widget_attrs),
            forms.HiddenInput()
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        return [None, None]

    def format_output(self, rendered_widgets):
        text_input, hidden_input = rendered_widgets

        output = self.output.format(
            question_class=self.question_class,
            question=self.question_html,
            text_input=text_input,
            hidden_input=hidden_input,
        )

        return mark_safe(output)

    def render_question(self, x, y, operator):
        operator = "&times;" if operator == "*" else operator
        question = self.question_tmpl.format(
            x=x,
            operator=operator,
            y=y,
        )
        return mark_safe(question)

    def render(self, name, value, attrs=None):
        x, y, operator, answer = get_new_values(self.values, self.operators)
        self.question_html = self.render_question(x, y, operator)
        value = ["", encode(answer)]
        return super().render(name, value, attrs=attrs)
