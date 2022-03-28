
__author__ = 'Chintalagiri Shashank <shashank.chintalagiri@gmail.com>'

from pkg_resources import get_distribution, DistributionNotFound
try:
    __version__ = get_distribution('kivy_garden.ebs.cefkivy').version
except DistributionNotFound:
    # package is not installed
    from setuptools_scm import get_version
    __version__ = get_version(root='../../../', relative_to=__file__)
