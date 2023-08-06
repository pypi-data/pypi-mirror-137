# Copyright (c) 2021 Cisco Systems, Inc. and its affiliates
# All rights reserved.

import pathlib

from launchpadlib.launchpad import Launchpad

from soufi import exceptions, finder


class UbuntuFinder(finder.SourceFinder):
    """Find Ubuntu source files."""

    distro = finder.Distro.ubuntu.value

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lp_archive = self.get_archive()

    def _find(self):
        build = self.get_build()
        source = self.get_source_from_build(build)
        urls = tuple(sorted(source.sourceFileUrls()))
        return UbuntuDiscoveredSource(urls, timeout=self.timeout)

    def get_archive(self):
        """Retrieve, and cache, the LP distro main archive object."""

        def inner():
            cachedir = pathlib.Path.home().joinpath(".launchpadlib", "cache")
            lp = Launchpad.login_anonymously(
                "soufi",
                "production",
                cachedir,
                version="devel",
                timeout=self.timeout,
            )
            distribution = lp.distributions[self.distro]
            return distribution.main_archive

        return self._cache.get_or_create('get_archive', inner)

    def get_build(self):
        bins = self.lp_archive.getPublishedBinaries(
            exact_match=True, binary_name=self.name, version=self.version
        )
        try:
            return bins[0].build
        except IndexError:
            raise exceptions.SourceNotFound

    def get_source_from_build(self, build):
        name = build.source_package_name
        ver = build.source_package_version
        sources = self.lp_archive.getPublishedSources(
            exact_match=True, source_name=name, version=ver
        )
        # TODO index error? Can't have a build without a source so this
        # should never fail.
        return sources[0]


class UbuntuDiscoveredSource(finder.DiscoveredSource):
    """A discovered Ubuntu source package."""

    def populate_archive(self, temp_dir, tar):
        # The file name is the last segment of the URL path.
        names = [url.rsplit('/', 1)[-1] for url in self.urls]
        for name, url in zip(names, self.urls):
            arcfile_name = self.download_file(temp_dir, name, url)
            tar.add(arcfile_name, arcname=name, filter=self.reset_tarinfo)

    def __repr__(self):
        return "\n".join(self.urls)
