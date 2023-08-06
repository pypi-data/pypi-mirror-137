"""A wrapper for the generic CloudVolume class.

Returns a separate wrapper for each registered CloudVolume front end.

Typical usage:
    import cirrusvolume as cv

    cv.CloudVolume(cloudpath, ...)
"""
from __future__ import annotations

from typing import Optional, Type

import cloudvolume as cv
import provenancetoolbox as ptb

from . import rules


REGISTERED_PLUGINS = dict()


def register_plugin(key: Type[cv.CloudVolume],
                    creation_function:
                        Callable[[Type[cv.CloudVolume]],
                                 Callable[[cv.CloudVolume], CloudVolume]]
                    ) -> None:
    """Connects CloudVolume classes to CirrusVolume wrappers.

    Args:
        key: A type of CloudVolume.
        creation_function: A CirrusVolume wrapper class.
    """
    REGISTERED_PLUGINS[key] = creation_function


class CloudVolume(cv.CloudVolume):
    """A CirrusVolume wrapper class for CloudVolumes.

    See cloudvolume.CloudVolume for original functionality. The CirrusVolume
    wrapper enforces rules for documentation before it allows data writing or
    modification.

    Additional attributes:
        sources: A list of cloudpaths or freeform sources.
        motivation: A reason why this CloudVolume was created.
        process: A processing step.
    """
    def __new__(cls,
                *args,
                sources: Optional[list[str]] = None,
                motivation: Optional[str] = None,
                process: Optional[ptb.Process] = None,
                **kwargs):
        cloudvolume = cv.CloudVolume(*args, **kwargs)

        return REGISTERED_PLUGINS[type(cloudvolume)](
                   cloudvolume, sources, motivation, process)

    # need to re-define this here bc it automatically writes
    @classmethod
    def from_numpy(cls,
                   *args,
                   sources: Optional[list[str]] = None,
                   motivation: Optional[str] = None,
                   process: ptb.Process = None,
                   **kwargs):
        """Create a new dataset from a numpy array.

        See cloudvolume.Cloudvolume for more information. Also enforces
        documentation rules before writing data.

        Additional args:
            sources: A list of cloudpaths or freeform sources.
            motivation: A reason why this CloudVolume was created.
            process: A processing step.
        """
        rules.check_writing_rules(sources, motivation, process)

        cloudvolume = super().from_numpy(cls, *args, **kwargs)

        rules.add_sources(cloudvolume, sources)
        rules.add_motivation(cloudvolume, motivation)
        rules.add_process(cloudvolume, process)

        return REGISTERED_PLUGINS[type(cloudvolume)](
                   cloudvolume, sources, motivation, process)
