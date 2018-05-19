# -*- coding: utf-8 -*-
# vim:tw=0:ts=4:sw=4:et

from readchar import key
from .base import BaseConsoleRender
from inquirer import errors


CTRL_RIGHT_SEQ = ['\x1b[1', ';', '3', 'C']

CTRL_LEFT_SEQ = ['\x1b[1', ';', '5', 'C']


class Checkbox(BaseConsoleRender):
    def __init__(self, *args, **kwargs):
#
        import pdb;pdb.set_trace()

        super(Checkbox, self).__init__(*args, **kwargs)
        self.selection = [k for (k, v) in enumerate(self.question.choices)
                          if v in (self.question.default or [])]
        self.current = 0
        self.key_state = []

    def get_options(self):
        for n in range(len(self.question.choices)):
            choice = self.question.choices[n]
            if n in self.selection:
                symbol = self.theme.Checkbox.selected_icon
                color = self.theme.Checkbox.selected_color
            else:
                symbol = self.theme.Checkbox.unselected_icon
                color = self.theme.Checkbox.unselected_color
            selector = ' '
            if n == self.current:
                selector = self.theme.Checkbox.selection_icon
                color = self.theme.Checkbox.selection_color
            yield choice, selector + ' ' + symbol, color

    def process_input(self, pressed):
        if pressed == key.UP:
            self.current = max(0, self.current - 1)
            return
        elif pressed == key.DOWN:
            self.current = min(len(self.question.choices) - 1,
                               self.current + 1)
            return
        elif pressed == key.SPACE:
            if self.current in self.selection:
                self.selection.remove(self.current)
            else:
                self.selection.append(self.current)
        elif pressed == key.LEFT:
            if self.current in self.selection:
                self.selection.remove(self.current)
        elif pressed == key.RIGHT:
            if self.current not in self.selection:
                self.selection.append(self.current)
        elif pressed == key.ENTER:
            result = []
            for x in self.selection:
                value = self.question.choices[x]
                result.append(getattr(value, 'value', value))
            raise errors.EndOfInput(result)
        elif pressed == key.CTRL_C:
            self.key_state = []
            raise KeyboardInterrupt()
        else:
            self.process_input_combo(pressed)
            return
        self.key_state = []

    def process_input_combo(self, pressed):
        if not self.key_state:
            self.key_state.append(pressed)
        else:
            match_len = self.match_state(CTRL_RIGHT_SEQ)
            if match_len == len(CTRL_RIGHT_SEQ):
                # FIXME: Implement
                pass
            elif match_len > 0:
                return

            match_len = self.match_state(CTRL_LEFT_SEQ)
            if match_len == len(CTRL_LEFT_SEQ):
                # FIXME: Implement
                pass
            elif match_len > 0:
                return

    def match_state(self, known_seq):
        match_len = 0
        for posit in range(len(self.key_state)):
            if self.key_state[posit] == known_seq[posit]:
                match_len += 1
            else:
                match_len = 0
                break
        return match_len

