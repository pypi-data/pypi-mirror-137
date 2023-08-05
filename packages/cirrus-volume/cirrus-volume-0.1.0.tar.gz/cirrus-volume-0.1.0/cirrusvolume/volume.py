'''
volume.py

A wrapper for the generic CloudVolume class. Returns a separate wrapper for
each registered CloudVolume front end.
'''
from __future__ import annotations

from typing import Optional

import cloudvolume as cv
import provenancetoolbox as ptb

from . import rules


REGISTERED_PLUGINS = dict()


def register_plugin(key, creation_function):
    REGISTERED_PLUGINS[key] = creation_function


class CloudVolume(cv.CloudVolume):
    def __new__(cls,
                *args,
                sources: Optional[list[str]] = None,
                motivation: Optional[str] = None,
                process: Optional[ptb.Process] = None,
                **kwargs):
        cloudvolume = cv.CloudVolume(*args, **kwargs)

        return REGISTERED_PLUGINS[type(cloudvolume)](
                   cloudvolume, sources, motivation, process)

    # need to re-define this bc it automatically writes
    @classmethod
    def from_numpy(cls,
                   *args,
                   sources: Optional[List[str]] = None,
                   motivation: Optional[str] = None,
                   process: ptb.Process = None,
                   **kwargs):
        rules.check_writing_rules(sources, motivation, process)

        cloudvolume = super().from_numpy(cls, *args, **kwargs)

        rules.add_sources(cloudvolume, sources)
        rules.add_motivation(cloudvolume, motivation)
        rules.add_process(cloudvolume, process)

        return REGISTERED_PLUGINS[type(cloudvolume)](
                   cloudvolume, sources, motivation, process)
