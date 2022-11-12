% example from https://www.erlang.org/faq/getting_started.html
-module(hello).
-export([hello_world/0]).

hello_world() -> io:fwrite("hello, world\n").