"""Test retrieving pollen data from Met Office forecasts.

Replacing Bendadryl-sponsored service queried by pypollen module, as
that's proved unreliable in practice (just stops providing responses),
with no error.
"""

# Register with Met Office DataPoint service:
# https://www.metoffice.gov.uk/datapoint

from clientsecrets import metkey

# Oh, nuts: pollen count isn't included in the site data. Ugh.

