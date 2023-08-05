'''
graphene.py

A wrapper for CloudVolumeGraphene
NOT IMPLEMENTED YET
'''
from __future__ import annotations

import warnings
from typing import Optional

import cloudvolume as cv
import provenancetoolbox as ptb
from cloudvolume.frontends.graphene import CloudVolumeGraphene

from . import rules
from .volume import register_plugin



def register():
    register_plugin(CloudVolumeGraphene, CirrusVolumeGraphene)


class CirrusVolumeGraphene(CloudVolumeGraphene):

    def __new__(self,
                cloudvolume: CloudVolume,
                sources: Optional[list[str]] = None,
                motivation: Optional[str] = None,
                process: Optional[ptb.Process] = None
                ):
        warnings.warn("CirrusVolumeGraphene not implemented yet!"
                      " Passing you a normal CloudVolumeGraphene")
        return cloudvolume
