class PlaylistManager:
    def __init__(self):
        self.playlists = {}

    def create_new_playlist(self, name: str):
        """Creates a new playlist object if one does not already exists.

        Args:
            name: The name of the playlist.

        Returns:
            The Playlist object and a boolean value which can be used to check
             if the playlist was newly created or not.
        """
        case_insensitive_name = name.upper()
        if case_insensitive_name in self.playlists.keys():
            return self.playlists[case_insensitive_name], False
        else:
            self.playlists[case_insensitive_name] = Playlist(name)
            return self.playlists[case_insensitive_name], True

    def get_playlist(self, name):
        return self.playlists.get(name.upper())

    def get_all_playlists(self):
        return list(self.playlists.values())

    def delete_playlist(self, name):
        case_insensitive_name = name.upper()
        if case_insensitive_name in self.playlists.keys():
            self.playlists.pop(case_insensitive_name)
            return True
        else:
            return False


"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""

    def __init__(self, name):
        self.name = name
        self.videos = {}

    def add_video(self, video):
        if video.video_id in self.videos.keys():
            return False
        else:
            self.videos[video.video_id] = video
            return True

    def remove_video(self, video):
        if video.video_id in self.videos.keys():
            self.videos.pop(video.video_id)
            return True
        else:
            return False

    def get_all_videos(self):
        return list(self.videos.values())

    def clear_playlist(self):
        self.videos = {}
