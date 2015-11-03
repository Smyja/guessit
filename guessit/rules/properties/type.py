#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
screenSize property
"""
from rebulk.match import Match


def _type(matches, value):
    """
    Define type match with given value.
    :param matches:
    :param value:
    :return:
    """
    matches.append(Match(0, len(matches.input_string), name='type', value=value))


def type_processor(matches):
    """
    Post processor to find file type based on all others found matches.
    :param matches:
    :return:
    """
    episode = matches.named('episodeNumber')
    season = matches.named('season')
    episode_details = matches.named('episodeDetails')

    if episode or season or episode_details:
        _type(matches, 'series')
        return

    film = matches.named('filmNumber')
    if film:
        _type(matches, 'movie')
        return

    year = matches.named('year')
    date = matches.named('date')

    if date and not year:
        _type(matches, 'series')
        return

    bonus = matches.named('bonusNumber')
    if bonus and not year:
        _type(matches, 'series')
        return

    crc32 = matches.named('crc32')
    anime_release_group = matches.named('releaseGroup', lambda match: 'anime' in match.tags)
    if crc32 and anime_release_group:
        _type(matches, 'series')
        return

    _type(matches, 'movie')
