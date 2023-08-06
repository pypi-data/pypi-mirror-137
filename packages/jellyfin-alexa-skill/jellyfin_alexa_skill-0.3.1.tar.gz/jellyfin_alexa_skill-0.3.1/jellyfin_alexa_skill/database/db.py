from pathlib import Path
from typing import List, Optional, Union

from peewee import DoesNotExist

from jellyfin_alexa_skill.alexa.util import set_shuffle_queue_idxs
from jellyfin_alexa_skill.database.model.base import db
from jellyfin_alexa_skill.database.model.playback import Playback, PlaybackItem
from jellyfin_alexa_skill.database.model.user import User


def connect_db(path: Union[Path, str]) -> None:
    db.init(str(path))
    db.connect()

    db.create_tables([Playback, User])


def get_playback(user_id: str) -> Optional[Playback]:
    try:
        return Playback.get(Playback.user_id == user_id)
    except DoesNotExist:
        playback = Playback.create(user_id=user_id)
        playback.save()
        return playback


def get_current_played_item(user_id: str) -> Optional[PlaybackItem]:
    try:
        playback = Playback.get(Playback.user_id == user_id)
        if playback.playing:
            if playback.shuffle:
                item = playback.queue[playback.shuffle_idxs[playback.current_idx]]
            else:
                item = playback.queue[playback.current_idx]

            return item
        else:
            return None
    except DoesNotExist:
        return None


def set_playback_queue(user_id: str, queue: List[PlaybackItem], reset: bool = False) -> Playback:
    playback = get_playback(user_id)
    playback.queue = queue
    playback.current_idx = 0

    if reset:
        playback.loop_single = False
        playback.loop_all = False
        playback.shuffle = False

    if playback.shuffle:
        set_shuffle_queue_idxs(playback)

    playback.save()

    return playback
