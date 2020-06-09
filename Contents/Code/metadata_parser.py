# -*- coding: utf-8 -*-

import json
import os
import unicodedata
import urllib
from .common_function import get_metadata_path, set_multimedia_info, LibraryType
from .content_rating import get_content_rating


def parse_search_metadata(media, lang, results):
    metadata_path = get_metadata_path(media=media, library_type=LibraryType.TV)
    json_data = json.loads(Core.storage.load(metadata_path))
    id, title, year, score = json_data['id'], json_data['title'], json_data['year'], 100
    Log.Debug('From JSON metadata id: %s, title: %s, year: %s' % (id, title, year))
    results.Append(MetadataSearchResult(id=id, name=title, year=year, score=score, lang=lang))


def parse_detail_metadata(media, metadata):
    metadata_path = get_metadata_path(media=media, library_type=LibraryType.TV)
    json_data = json.loads(Core.storage.load(metadata_path))

    # Basic Information
    metadata.title = media.title
    metadata.title_sort = unicodedata.normalize('NFKD', metadata.title[0])[0] + ' ' + metadata.title
    metadata.original_title = json_data['original_title'] if 'original_title' in json_data else media.title
    if 'originally_available_at' in json_data:
        metadata.originally_available_at = Datetime.ParseDate(json_data['originally_available_at']).date()
    if 'studio' in json_data:
        metadata.studio = json_data['studio']
    if 'content_rating' in json_data:
        metadata.content_rating = get_content_rating(json_data['content_rating'], Prefs['content_rating'])
    if 'rating' in json_data and json_data['rating']:
        metadata.rating = float(json_data['rating'])
    if 'summary' in json_data:
        metadata.summary = json_data['summary']

    info_types = [['genres', metadata.genres], ['countries', metadata.countries]]
    for info_type in info_types:
        if info_type[0] in json_data:
            [info_type[1].add(info) for info in json_data[info_type[0]]]

    # Roles
    metadata.roles.clear()
    if 'roles' in json_data:
        for info in json_data['roles']:
            actor = metadata.roles.new()
            actor.name = info['name'] if 'name' in info else None
            actor.photo = info['photo'] if 'photo' in info else None
            actor.role = info['role'] if 'role' in info else None

    # Theme
    if 'themes' in json_data:
        set_multimedia_info(metadata_path, metadata.themes, json_data['themes'], Prefs['max_num_themes'])

    # Poster & Art
    if 'photos' in json_data:
        photo_types = [
            ['posters', Prefs['max_num_posters'], metadata.posters],
            ['art', Prefs['max_num_art'], metadata.art],
            ['banners', Prefs['max_num_banners'], metadata.banners]
        ]

        photos = json_data['photos']
        for photo_type in photo_types:
            if photo_type[0] in photos:
                set_multimedia_info(metadata_path, photo_type[2], photos[photo_type[0]], photo_type[1])

    seasons = []
    for season in media.seasons:
        seasons.append(season)
    seasons.sort(key=int)

    if 'seasons' in json_data:
        for s in seasons:
            if s not in json_data['seasons']:
                continue

            season = metadata.seasons[s]
            season_data = json_data['seasons'][s]
            if 'summary' in season_data:
                season.summary = season_data['summary']
            if 'photos' in season_data:
                photo_types = [
                    ['posters', Prefs['max_num_posters'], season.posters],
                    ['art', Prefs['max_num_art'], season.art]
                ]
                photos = season_data['photos']
                for photo_type in photo_types:
                    if photo_type[0] in photos:
                        set_multimedia_info(metadata_path, photo_type[2], photos[photo_type[0]], photo_type[1])

            episodes = []
            for episode in media.seasons[s].episodes:
                episodes.append(episode)
            episodes.sort(key=int)

            if 'episodes' in season_data:
                for e in episodes:
                    if e not in season_data['episodes']:
                        continue

                    episode = season.episodes[e]
                    episode_data = season_data['episodes'][e]
                    if 'title' in episode_data:
                        episode.title = episode_data['title']
                    if 'summary' in episode_data:
                        episode.summary = episode_data['summary']
                    if 'originally_available_at' in episode_data and episode_data['originally_available_at']:
                        episode.originally_available_at = Datetime.ParseDate(episode_data['originally_available_at']).date()
                    if 'rating' in episode_data:
                        episode.rating = episode_data['rating']

                    # Directors & Producers & Writers
                    person_types = [['directors', episode.directors], ['producers', episode.producers],
                                    ['writers', episode.writers]]

                    for person_type in person_types:
                        if person_type[0] in episode_data:
                            person_type[1].clear()
                            for person in episode_data[person_type[0]]:
                                new_person = person_type[1].new()
                                new_person.name = person['name']
                                new_person.photo = person['photo']



    Log.Debug('Metadata for %s is parsed from JSON' % metadata.title)
