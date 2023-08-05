'''
rules.py

A library of functions for enforcing and enacting the documentation rules.

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
'''
from __future__ import annotations

import warnings
from typing import Optional

import cloudvolume as cv
import provenancetoolbox as ptb


def check_writing_rules(sources: Optional[list[str]] = None,
                        motivation: Optional[str] = None,
                        process: Optional[ptb.Process] = None
                        ) -> None:
    '''
    Checks whether the provided fields are sufficient to allow writing
    to a volume.
    '''
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
    '''Documents the sources of a CloudVolume if they don't already exist'''
    currentsources = set(cloudvolume.provenance.sources)

    newsources = currentsources.union(sources)

    if len(newsources) > len(currentsources):
        cloudvolume.provenance.sources = list(newsources)
        cloudvolume.commit_provenance()


def add_motivation(cloudvolume: cv.CloudVolume,
                   motivation: Optional[str] = None
                   ) -> None:
    '''Documents the motivation of a CloudVolume if it doesn't already exist'''
    if pt.note_absent(cloudvolume, motivation, pt.MOTIVATION):
        pt.add_motivation(cloudvolume, motivation)


def add_process(cloudvolume: cv.CloudVolume,
                process: Optional[ptb.Process] = None
                ) -> None:
    '''
    Adds the current process to the CloudVolume documentation if it doesn't
    already exist
    '''
    if pt.process_absent(cloudvolume, process.description):
        pt.log_process(cloudvolume, process)
    else:
        warnings.warn('Process with the same description already logged.'
                      ' Skipping')


def documentvolume(cloudvolume: cv.CloudVolume,
                   sources: Optional[list[str]] = None,
                   motivation: Optional[str] = None,
                   process: Optional[ptb.Process] = None
                   ) -> None:
    'A single function to perform default documentation of a volume'
    add_sources(cloudvolume, sources)
    add_motivation(cloudvolume, motivation)
    add_process(cloudvolume, process)
