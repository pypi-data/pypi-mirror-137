# generated by datamodel-codegen:
#   filename:  data.json
#   timestamp: 2021-01-27T04:42:01+00:00

from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class Stream(BaseModel):
    id: str
    type: str
    video_codec: Optional[str] = None
    video_codec_level: Optional[str] = None
    video_bitrate: Optional[str] = None
    video_bit_depth: Optional[str] = None
    video_chroma_subsampling: Optional[str] = None
    video_color_primaries: Optional[str] = None
    video_color_range: Optional[str] = None
    video_color_space: Optional[str] = None
    video_color_trc: Optional[str] = None
    video_frame_rate: Optional[str] = None
    video_ref_frames: Optional[str] = None
    video_height: Optional[str] = None
    video_width: Optional[str] = None
    video_language: Optional[str] = None
    video_language_code: Optional[str] = None
    video_profile: Optional[str] = None
    video_scan_type: Optional[str] = None
    selected: int
    audio_codec: Optional[str] = None
    audio_bitrate: Optional[str] = None
    audio_bitrate_mode: Optional[str] = None
    audio_channels: Optional[str] = None
    audio_channel_layout: Optional[str] = None
    audio_sample_rate: Optional[str] = None
    audio_language: Optional[str] = None
    audio_language_code: Optional[str] = None
    audio_profile: Optional[str] = None


class Part(BaseModel):
    id: str
    file: str
    file_size: str
    indexes: int
    streams: List[Stream]
    selected: int


class MediaInfoItem(BaseModel):
    id: str
    container: str
    bitrate: str
    height: str
    width: str
    aspect_ratio: str
    video_codec: str
    video_resolution: str
    video_full_resolution: str
    video_framerate: str
    video_profile: str
    audio_codec: str
    audio_channels: str
    audio_channel_layout: str
    audio_profile: str
    optimized_version: int
    channel_call_sign: str
    channel_identifier: str
    channel_thumb: str
    parts: List[Part]


class Data(BaseModel):
    media_type: str
    section_id: str
    library_name: str
    rating_key: str
    parent_rating_key: str
    grandparent_rating_key: str
    title: str
    parent_title: str
    grandparent_title: str
    original_title: str
    sort_title: str
    media_index: str
    parent_media_index: str
    studio: str
    content_rating: str
    summary: str
    tagline: str
    rating: str
    rating_image: str
    audience_rating: str
    audience_rating_image: str
    user_rating: str
    duration: str
    year: str
    thumb: str
    parent_thumb: str
    grandparent_thumb: str
    art: str
    banner: str
    originally_available_at: str
    added_at: str
    updated_at: str
    last_viewed_at: str
    guid: str
    parent_guid: str
    grandparent_guid: str
    directors: List[str]
    writers: List[str]
    actors: List[str]
    genres: List[str]
    labels: List
    collections: List
    guids: List[str]
    full_title: str
    children_count: int
    live: int
    media_info: List[MediaInfoItem]


class Response(BaseModel):
    result: str
    message: Any
    data: Data


class Model(BaseModel):
    response: Response
