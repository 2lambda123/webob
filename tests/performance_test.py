#!/usr/bin/env python
from webob.response import Response


def make_middleware(app):
    from repoze.profile.profiler import AccumulatingProfileMiddleware

    return AccumulatingProfileMiddleware(
        app,
        log_filename="/tmp/profile.log",
        discard_first_request=True,
        flush_at_shutdown=True,
        path="/__profile__",
    )


def simple_app(environ, start_response):
    resp = Response("Hello world!")
    return resp(environ, start_response)


if __name__ == "__main__":
    import os
    import signal
    import sys

    if sys.argv[1:]:
        arg = sys.argv[1]
    else:
        arg = None
    if arg in ["open", "run"]:
        import subprocess
        import time
        import webbrowser

        os.environ["SHOW_OUTPUT"] = "0"
        proc = subprocess.Popen([sys.executable, __file__])
        time.sleep(1)
        subprocess.call(["ab", "-n", "1000", "http://localhost:8080/"])
        if arg == "open":
            webbrowser.open("http://localhost:8080/__profile__")
        print("Hit ^C to end")
        try:
            while 1:
                input()
        finally:
            os.kill(proc.pid, signal.SIGKILL)
    else:
        from paste.httpserver import serve

        if os.environ.get("SHOW_OUTPUT") != "0":
            print("Note you can also use:)")
            print(f"  {sys.executable} {__file__} open")
            print('to run ab and open a browser (or "run" to just run ab)')
            print("Now do:")
            print("ab -n 1000 http://localhost:8080/")
            print("wget -O - http://localhost:8080/__profile__")
        serve(make_middleware(simple_app))
