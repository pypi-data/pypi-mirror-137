"""A wrapper for CloudVolumePrecomputed."""
from __future__ import annotations

from typing import Optional

import cloudvolume as cv
from cloudvolume.frontends.precomputed import CloudVolumePrecomputed
import provenancetoolbox as ptb

from . import rules
from .volume import register_plugin


def register():
    """Registration function for CirrusVolumePrecomputed.

    See volume.register_plugin for more information.
    """
    register_plugin(CloudVolumePrecomputed, CirrusVolumePrecomputed)


class CirrusVolumePrecomputed(CloudVolumePrecomputed):

    def __init__(self,
                 cloudvolume: cv.CloudVolume,
                 sources: Optional[list[str]] = None,
                 motivation: Optional[str] = None,
                 process: Optional[ptb.Process] = None
                 ):
        # Copying the CloudVolume attributes
        self.config = cloudvolume.config
        self.cache = cloudvolume.cache
        self.meta = cloudvolume.meta

        self.image = cloudvolume.image
        self.mesh = cloudvolume.mesh
        self.skeleton = cloudvolume.skeleton

        self.green_threads = cloudvolume.green_threads

        self.mip = cloudvolume.mip
        self.pid = cloudvolume.pid

        # CirrusVolume-specific atrributes
        self.sources = sources
        self.motivation = motivation
        self.process = process

    # Overriding all methods that allow writing to the image
    # with versions that check the rules first
    def __setitem__(self, slices, img):
        rules.check_writing_rules(self.sources, self.motivation, self.process)

        rules.documentvolume(self, self.sources,
                             self.motivation, self.process)

        super().__setitem__(slices, img)

    def upload_from_shared_memory(self,
                                  location,
                                  bbox,
                                  order='F',
                                  cutout_bbox=None) -> None:
        rules.check_writing_rules(self.sources, self.motivation, self.process)

        rules.documentvolume(self, self.sources,
                             self.motivation, self.process)

        super().upload_from_shared_memory(location, bbox,
                                          order=order, cutout_bbox=cutout_bbox)

    def upload_from_file(self,
                         location, bbox, order='F', cutout_bbox=None) -> None:
        rules.check_writing_rules(self.sources, self.motivation, self.process)

        rules.documentvolume(self, self.sources,
                             self.motivation, self.process)

        super().upload_from_file(location, bbox,
                                 order=order, cutout_bbox=cutout_bbox)
