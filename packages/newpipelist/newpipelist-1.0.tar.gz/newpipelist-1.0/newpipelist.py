#!/usr/bin/env python3
'''
A utility to convert playlists in a NewPipe database export to M3U files.
'''

from typing import List, Dict
import argparse
import os
import re
import sqlite3


def get_playlist_list(cur: sqlite3.Cursor) -> List[Dict]:
	'Get a list of available playlists.'
	cur.execute('SELECT uid, name FROM playlists')
	return [{'id': p[0], 'name': p[1]} for p in cur.fetchall()]


def get_playlist(cur: sqlite3.Cursor, playlist_id: str) -> List[Dict]:
	'Get videos in playlist.'
	cur.execute(
		'''SELECT title, uploader, url, duration
		FROM playlist_stream_join p
		JOIN streams s ON p.stream_id = s.uid
		WHERE p.playlist_id = ?''',
		(playlist_id,)
	)
	return [{
		'title': v[0],
		'uploader': v[1],
		'url': v[2],
		'duration': v[3],
	} for v in cur.fetchall()]


def playlist_to_m3u(playlist: List[Dict]) -> str:
	'Convert a list of videos to an M3U string.'
	m3u = '#EXTM3U\n'
	for video in playlist:
		m3u += '#EXTINF:%s,%s\n#EXTART:%s\n%s\n' % (
			video['duration'],
			video['title'],
			video['uploader'],
			video['url']
		)
	return m3u


def main() -> None:
	'Run the command-line interface.'
	parser = argparse.ArgumentParser(
		description='A utility to convert playlists in a NewPipe database export to M3U files.',
	)
	parser.add_argument(
		'file',
		help='input file to read from (e.g. newpipe.db).',
	)
	parser.add_argument(
		'-p',
		'--playlist',
		help='ID of specific playlist to get.',
		type=int,
	)
	parser.add_argument(
		'-l',
		'--list',
		help='Print a list of playlists by ID.',
		action='store_true',
	)
	parser.add_argument(
		'-d',
		'--directory',
		help='Export all playlists to this directory.',
	)
	args = parser.parse_args()

	db = sqlite3.connect(args.file)
	cur = db.cursor()

	if not (args.list or args.playlist or args.directory):
		parser.error('You must give an option.')
	elif args.list:
		for playlist in get_playlist_list(cur):
			print('%s: %s' % (playlist['id'], playlist['name']))
	elif args.playlist is not None:
		print(playlist_to_m3u(get_playlist(cur, args.playlist)), end='')
	elif args.directory is not None:
		if not os.path.exists(args.directory):
			os.mkdir(args.directory)
		for playlist in get_playlist_list(cur):
			m3u = playlist_to_m3u(get_playlist(cur, playlist['id']))
			filename = '%s/%s.m3u' % (
				args.directory,
				re.sub('[/\0]', '_', playlist['name'])
			)
			with open(filename, 'w') as f:
				f.write(m3u)


if __name__ == '__main__':
	main()
