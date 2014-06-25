from flask import g


def active_time_mode(time_mode):
    if g.time_mode == time_mode:
        return 'class=active'


