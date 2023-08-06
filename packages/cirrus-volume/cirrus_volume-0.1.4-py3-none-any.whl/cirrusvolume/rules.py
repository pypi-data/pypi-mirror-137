"""A library of functions for enforcing and enacting the documentation rules.

THE RULES
You cannot write to a CirrusVolume unless you've passed it:
(1) A set of sources from which this was created (e.g., another CloudVolume
path or a freeform justification like "tracer annotation"). This must be
formatted as a list[str], and any sources that haven't been logged previously
will be added to the current sources field of the provenance file

(2) The motivation for creating the volume (str) has been logged and you've
included that motivation when instantiating the object. A volume can have
multiple motivation notes, and your motivation only need match one of them.

(3) You've passed a Process (a code environment & parameters) to the class.
The process will be logged unless another process with the same task
description has already been logged. These are defined by provenance-tools.
"""
from __future__ import annotations

import warnings
from typing import Optional

import cloudvolume as cv
import provenancetoolbox as ptb


def check_writing_rules(sources: Optional[list[str]] = None,
                        motivation: Optional[str] = None,
                        process: Optional[ptb.Process] = None
                        ) -> None:
    """Checks the rules for write-access to a CloudVolume.

    Checks whether the provided fields are sufficient to allow writing
    to a volume.

    Args:
        sources: A list of descriptions for where this volume came from.
        motivation: The motivation for creating this volume.
        process: The process that describes the volume's creation.

    Raises:
        AssertionError: One of the write rules has been violated.
    """
    assert all(v is not None for v in [sources, motivation, process]
               ), (""
                   "Need to define sources, motivation and process in order"
                   " to write to this volume")

    # Checking sources
    assert isinstance(sources, list)
    assert all(isinstance(v, str) for v in sources)

    # Checking motivation
    assert isinstance(motivation, str)

    # Checking process
    assert isinstance(process, ptb.Process)


def add_sources(cloudvolume: cv.CloudVolume,
                sources: Optional[list[str]] = None
                ) -> None:
    """Logs sources in a CloudVolume if they don't already exist.

    Args:
        cloudvolume: A CloudVolume.
        sources: A list of cloudpaths or freeform sources.
    """
    currentsources = set(cloudvolume.provenance.sources)

    newsources = currentsources.union(sources)

    if len(newsources) > len(currentsources):
        cloudvolume.provenance.sources = list(newsources)
        cloudvolume.commit_provenance()


def add_motivation(cloudvolume: cv.CloudVolume,
                   motivation: Optional[str] = None
                   ) -> None:
    """Logs a motivation in a CloudVolume if it doesn't already exist.

    Args:
        cloudvolume: A CloudVolume.
        motivation: A reason why this CloudVolume was created.
    """
    if ptb.note_absent(cloudvolume, motivation, ptb.NoteType.MOTIVATION):
        ptb.addmotivation(cloudvolume, motivation)


def add_process(cloudvolume: cv.CloudVolume,
                process: Optional[ptb.Process] = None
                ) -> None:
    
    """Logs a ptb.Process in a CloudVolume if not already logged.

    Args:
        cloudvolume: A CloudVolume.
        process: A processing step.
    """
    if ptb.process_absent(cloudvolume, process):
        ptb.logprocess(cloudvolume, process)
    else:
        warnings.warn('Process with the same description already logged.'
                      ' Skipping')


def documentvolume(cloudvolume: cv.CloudVolume,
                   sources: Optional[list[str]] = None,
                   motivation: Optional[str] = None,
                   process: Optional[ptb.Process] = None
                   ) -> None:
    """Logs all required fields for writing to a CirrusVolume.

    Args:
        cloudvolume: A CloudVolume.
        sources: A list of cloudpaths or freeform sources.
        motivation: A reason why this CloudVolume was created.
        process: A processing step.
    """
    add_sources(cloudvolume, sources)
    add_motivation(cloudvolume, motivation)
    add_process(cloudvolume, process)
