"""
A small tool to collect and print out unannotated weather maps from NOAA's SPC.

Sample invocation:
python3 wxbrief --print /usr/bin/lpr --levels 300,500,850

Copyright 2024 Markus Broecker

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the “Software”), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from absl import app
from absl import flags

from typing import Sequence

import datetime
import logging
import requests
import subprocess
import tempfile


_VALID_MB_MAP_LEVELS = ("sfc", "925", "850", "700", "500", "300", "250")

_ZULU = flags.DEFINE_enum('zulu', '12Z', ('00Z', '12Z'), 
													'Which report to grab,either 12Z or 00Z.')

_LEVELS = flags.DEFINE_list(
	'levels', ['500', '850', 'sfc'], 
	'Which mb level maps should we download? These must be one of the following: '
	+ ','.join(_VALID_MB_MAP_LEVELS))

_PRINT_COMMAND = flags.DEFINE_string(
	'print', '', 'Which print command to use to print files? E.g. on Linux it '
	'should be /usr/bin/lpr. This will print the downloaded maps on the default '
	'printer using CUPS. If left empty, no maps will be printed.')


def make_spc_map_url(date: datetime.datetime, level: str) -> str:
	"""Creates a url to download an unannotated wx map from https://www.spc.noaa.gov/obswx/maps/"""
	if level not in _VALID_MB_MAP_LEVELS:
		raise ValueError('Invalid mb level %s.', level)
	zulu = _ZULU.value.rstrip('Z')
	if zulu not in ('00', '12'):
		raise ValueError('Invalid analysis hour, expected 00 or 12.')
	datestr = date.strftime('%y%m%d')
	return f'https://www.spc.noaa.gov/obswx/maps/{level}_{datestr}_{zulu}.pdf'


def main(argv: Sequence[str]):
	# Validate mb flags.
	for mb_value in _LEVELS.value:
		logging.info(mb_value)
		if mb_value not in _VALID_MB_MAP_LEVELS:
			raise app.UsageError(f'Invalid --upper_air value {mb_value}; expected one of {",".join(_VALID_MB_MAP_LEVELS)}.')

	now = datetime.datetime.now()
	with tempfile.TemporaryDirectory(prefix='wxbrief.') as temp:
		for level in _LEVELS.value:
			logging.info('Downloading level %s ... ', (level + 'mb' if level != 'sfc' else 'sfc'))
			url = make_spc_map_url(now, level)
			target = f'{temp}/{level}.pdf'

			response = requests.get(url, stream=True)
			if not response or not response.status_code == 200:
				logging.error('Unable to download %s from %s; error: %s', target, url, response.error)

			with open(f'{temp}/{level}.pdf', 'wb') as pdf:
				pdf.write(response.content)

			if _PRINT_COMMAND.value:
				logging.info('Printing %s', target)
				subprocess.run([_PRINT_COMMAND.value, target], check=True)

if __name__ == '__main__':
	app.run(main)