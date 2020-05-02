# -*- coding: utf-8 -*-

from .common_function import is_search_metadata_available, LibraryType
from .metadata_parser import parse_search_metadata, parse_detail_metadata


def Start():
    Log.Info('Local TV Agent started.')
    HTTP.CacheTime = CACHE_1DAY
    HTTP.Headers['Accept'] = 'text/html, application/json'


class LocalTVAgent(Agent.TV_Shows):
    name = 'Local TV Agent'
    languages = [Locale.Language.Korean]
    primary_provider = True
    accepts_from = ['com.plexapp.agents.localmedia']

    def search(self, results, media, lang):
        metadata_exists = is_search_metadata_available(media=media, library_type=LibraryType.TV)
        if metadata_exists:
            parse_search_metadata(media=media, lang=lang, results=results)
        else:
            pass


    def update(self, metadata, media, lang):
        metadata_exists = is_search_metadata_available(media=media, library_type=LibraryType.TV)
        if metadata_exists:
            parse_detail_metadata(media=media, metadata=metadata)
        else:
            pass
