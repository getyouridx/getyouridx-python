#!/usr/bin/env python

import getyouridx

idxsearch = getyouridx.IDXSearch('<GETYOURIDX-APIKEY-HERE>')
idxsearch.add_filter(getyouridx.IDXFilter_In('mls_id', ['FHAAR']))
print str(idxsearch.result().toxml())