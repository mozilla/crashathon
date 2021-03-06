# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Crashathon -- a Firefox crash collator

# <codecell>

import os
import datetime
import ujson as json
from moztelemetry import get_pings

# <headingcell level=2>

# Some configuration variables

# <codecell>

#: Number of days to fetch crash pings for
DAYS = 30

#: Fraction of pings to fetch
FRACTION = 1

#: The build channels to fetch and store crash pings for
CHANNELS = [
    'nightly',
    'aurora',
    'beta',
    'release',
]

#: The time is now
NOW = datetime.datetime.now()


def get_crash_pings(channel, start_date, end_date, fraction):
    pings = get_pings(
        sc,  # noqa
        app='Firefox',
        channel=channel,
        submission_date=(start_date, end_date),
        build_id=('20100101000000', '99999999999999'),
        doc_type='crash',
        fraction=fraction,
    )
    return pings

# <markdowncell>

# For the given build channel, start and end date and a fraction, gets
# crash data, does some filtering and transformations and writes
# an anonymized JSON file with the number of crashes and some metadata.

# <codecell>

def store_crashes(channel, start_date, end_date, fraction):
    # get the raw crash data first
    crash_pings = get_crash_pings(
        channel,
        start_date=start_date.strftime("%Y%m%d"),
        end_date=end_date.strftime("%Y%m%d"),
        fraction=fraction,
    )
    # drop crash data that doesn't have client IDs
    non_empty_pings = crash_pings.filter(
        lambda ping: ping.get('clientId') is not None,
    )
    # group by the client ID so we can build a list of occurences per client ID
    grouped_pings = non_empty_pings.groupBy(
        lambda ping: ping.get('clientId')
    )
    # get a list of crash occurences
    crash_numbers = grouped_pings.map(
        lambda data: len(data[1]),
    )
    # order by number to be nice to the people reading the file
    ordered_numbers = crash_numbers.sortBy(lambda count: -count)

    # build the data to write to the json data
    data = {
        'channel': channel,
        'count': ordered_numbers.count(),
        'crashes': ordered_numbers.collect(),
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
    }
    # write the data
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = os.path.join(output_dir, 'crashes_%s.json' % channel)
    with open(output_path, 'w') as json_file:
        json.dump(data, json_file)

# <headingcell level=2>

# Store the aggregated crashes to disk for all configured channels

# <codecell>

for channel in CHANNELS:
    start_date = (NOW - datetime.timedelta(days=DAYS)).date()
    end_date = NOW.date()
    print 'getting crashes for channel', channel
    print 'starting', start_date, 'ending', end_date
    print 'for a fraction of ', FRACTION
    store_crashes(
        channel,
        start_date=start_date,
        end_date=end_date,
        fraction=FRACTION,
    )
