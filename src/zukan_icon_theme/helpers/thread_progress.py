"""
Copied from:

https://github.com/tbfisher/sublimetext-Pandoc/blob/master/thread_progress.py
https://github.com/wbond/package_control/blob/master/package_control/thread_progress.py

with the following licence:


Copyright (c) 2011-2016 Will Bond <will@wbond.net>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import sublime


class ThreadProgress:
    """
    Animates an indicator in the status area while a thread runs

    Parameters:
    thread (str) -- the thread to track for activity
    message (str) -- the message to display next to the activity indicator
    success_message (str) -- the message to display once the thread is complete
    dialog_message (Optional[str]) -- the message to display in a dialog once the
    thread is complete. Default is None.
    """

    def __init__(
        self,
        thread: str,
        message: str,
        success_message: str,
        dialog_message: str = None,
    ):
        self.thread = thread
        self.message = message
        self.success_message = success_message
        self.dialog_message = dialog_message
        self.addend = 1
        self.size = 3
        self.last_view = None
        self.window = None
        sublime.set_timeout(lambda: self.run(0), 100)

    def run(self, i):
        if self.window is None:
            self.window = sublime.active_window()
        active_view = self.window.active_view()

        if self.last_view is not None and active_view != self.last_view:
            self.last_view.erase_status('_zukan')
            self.last_view = None

        if not self.thread.is_alive():

            def cleanup():
                active_view.erase_status('_zukan')

            if hasattr(self.thread, 'result') and not self.thread.result:
                cleanup()
                return
            active_view.set_status('_zukan', self.success_message)
            sublime.set_timeout(cleanup, 1000)
            if self.dialog_message is not None:
                sublime.message_dialog(self.dialog_message)
            return

        before = i % self.size
        after = (self.size - 1) - before

        active_view.set_status(
            '_zukan',
            '%s %s ⦿ %s' % (self.message, ' ⦾ ' * before, ' ⦾ ' * after),
            # '%s %s ◍ %s' % (self.message, ' ၀ ' * before, ' ၀ ' * after)
            # '%s [%s=%s]' % (self.message, ' ' * before, ' ' * after)
        )
        if self.last_view is None:
            self.last_view = active_view

        if not after:
            self.addend = -1
        if not before:
            self.addend = 1
        i += self.addend

        sublime.set_timeout(lambda: self.run(i), 400)
