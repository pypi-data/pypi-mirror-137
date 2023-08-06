from . import validateCNPJ
from . import validateCPF


from pkg_resources import get_distribution

__version__ = get_distribution('br_registrations').version
