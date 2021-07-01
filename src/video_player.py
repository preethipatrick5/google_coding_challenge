"""A video player class."""
import random

from .flag_manager import FlagManager
from .video_library import VideoLibrary
from .video_playlist import PlaylistManager


class PlayerState:
    def __init__(self):
        self.current_video = None
        self.paused = False


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._playlist_manager = PlaylistManager()
        self._flag_manager = FlagManager()
        self.state = PlayerState()

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        print("Here's a list of all available videos:")
        for video in sorted(self._video_library.get_all_videos(), key=lambda v: v.title):
            print(self._print_video(video))

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        video = self._video_library.get_video(video_id)
        if video is None:
            print("Cannot play video: Video does not exist")
        else:
            reason = self._flag_manager.get_reason(video)
            if reason:
                print(f"Cannot play video: Video is currently flagged (reason: {reason})")
            else:
                if self.state.current_video is not None:
                    self.stop_video()
                self.state.current_video = video
                print(f"Playing video: {video.title}")

    def stop_video(self):
        """Stops the current video."""
        if self.state.current_video is None:
            print("Cannot stop video: No video is currently playing")
        else:
            print(f"Stopping video: {self.state.current_video.title}")
            self.state.current_video = None
            self.state.paused = False

    def play_random_video(self):
        """Plays a random video from the video library."""
        flagged_videos = self._flag_manager.get_flagged_video_ids()
        videos = self._video_library.get_videos_not_in_ids(flagged_videos)
        if videos:
            rand_video = random.choice(videos)
            self.play_video(video_id=rand_video.video_id)
        else:
            print("No videos available")

    def pause_video(self):
        """Pauses the current video."""
        if self.state.current_video is not None and not self.state.paused:
            self.state.paused = True
            print(f"Pausing video: {self.state.current_video.title}")
        elif self.state.current_video is not None and self.state.paused:
            print(f"Video already paused: {self.state.current_video}")
        else:
            print("Cannot pause video: No video is currently playing")

    def continue_video(self):
        """Resumes playing the current video."""
        if self.state.current_video is not None and not self.state.paused:
            print("Cannot continue video: Video is not paused")
        elif self.state.current_video is not None and self.state.paused:
            self.state.paused = False
            print(f"Continuing video: {self.state.current_video}")
        else:
            print("Cannot continue video: No video is currently playing")

    def show_playing(self):
        """Displays video currently playing."""
        if self.state.current_video is None:
            print("No video is currently playing")
        if self.state.current_video is not None:
            message = f"Currently playing: {self.state.current_video}"
            if self.state.paused:
                message = f"{message} - PAUSED"
            print(message)

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist, new = self._playlist_manager.create_new_playlist(playlist_name)
        if new:
            print(f"Successfully created new playlist: {playlist.name}")
        else:
            print("Cannot create playlist: A playlist with the same name already exists")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        playlist = self._playlist_manager.get_playlist(playlist_name)
        video = self._video_library.get_video(video_id)
        if playlist:
            if video:
                reason = self._flag_manager.get_reason(video)
                if reason:
                    print(f"Cannot add video to {playlist_name}: Video is currently flagged (reason: {reason})")
                else:
                    added = playlist.add_video(video)
                    if added:
                        print(f"Added video to {playlist_name}: {video.title}")
                    else:
                        print(f"Cannot add video to {playlist_name}: Video already added")
            else:
                print(f"Cannot add video to {playlist_name}: Video does not exist")
        else:
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")

    def show_all_playlists(self):
        """Display all playlists."""
        playlists = self._playlist_manager.get_all_playlists()
        if playlists:
            print("Showing all playlists:")
            for playlist in sorted(playlists, key=lambda p: p.name):
                print(f"{playlist.name}")
        else:
            print("No playlists exist yet")

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self._playlist_manager.get_playlist(playlist_name)
        if playlist:
            print(f"Showing playlist: {playlist_name}")
            videos = playlist.get_all_videos()
            if videos:
                for video in videos:
                    print(self._print_video(video))
            else:
                print("No videos here yet")
        else:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        playlist = self._playlist_manager.get_playlist(playlist_name)
        video = self._video_library.get_video(video_id)
        if playlist:
            if video:
                removed = playlist.remove_video(video)
                if removed:
                    print(f"Removed video from {playlist_name}: {video.title}")
                else:
                    print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
            else:
                print(f"Cannot remove video from {playlist_name}: Video does not exist")
        else:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = self._playlist_manager.get_playlist(playlist_name)
        if playlist:
            playlist.clear_playlist()
            print(f"Successfully removed all videos from {playlist_name}")
        else:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        deleted = self._playlist_manager.delete_playlist(playlist_name)
        if deleted:
            print(f"Deleted playlist: {playlist_name}")
        else:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        flagged_video_ids = self._flag_manager.get_flagged_video_ids()
        videos = self._video_library.get_videos_not_in_ids(flagged_video_ids)
        filtered_videos = list(filter(lambda video: search_term.upper() in video.title.upper(), videos))
        if filtered_videos:
            print(f"Here are the results for {search_term}:")
            videos = sorted(filtered_videos, key=lambda video: video.title)
            for index, video in enumerate(videos):
                print(f"{index + 1}) {video}")
            try:
                print("Would you like to play any of the above? If yes, specify the number of the video. ")
                print("If your answer is not a valid number, we will assume it's a no.")
                video_index = int(input())
                video_index = video_index - 1
                if 0 < video_index < len(filtered_videos):
                    self.play_video(filtered_videos[video_index].video_id)
            except:
                pass
        else:
            print(f"No search results for {search_term}")

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        flagged_video_ids = self._flag_manager.get_flagged_video_ids()
        videos = self._video_library.get_videos_not_in_ids(flagged_video_ids)
        filtered_videos = list(filter(lambda video: video_tag.lower() in video.tags, videos))
        if filtered_videos:
            print(f"Here are the results for {video_tag}:")
            videos = sorted(filtered_videos, key=lambda video: video.title)
            for index, video in enumerate(videos):
                print(f"{index + 1}) {video}")
            try:
                print("Would you like to play any of the above? If yes, specify the number of the video. ")
                print("If your answer is not a valid number, we will assume it's a no.")
                video_index = int(input())
                video_index = video_index - 1
                if 0 <= video_index < len(filtered_videos):
                    self.play_video(filtered_videos[video_index].video_id)
            except:
                pass
        else:
            print(f"No search results for {video_tag}")

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        video = self._video_library.get_video(video_id)
        if video:
            if self.state.current_video:
                if self.state.current_video.video_id == video.video_id:
                    self.stop_video()
            reason, flagged = self._flag_manager.flag_video(video, flag_reason)
            if flagged:
                print(f"Successfully flagged video: {video.title} (reason: {reason})")
            else:
                print("Cannot flag video: Video is already flagged")
        else:
            print("Cannot flag video: Video does not exist")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        video = self._video_library.get_video(video_id)
        if video:
            allowed = self._flag_manager.allow_video(video)
            if allowed:
                print(f"Successfully removed flag from video: {video.title}")
            else:
                print("Cannot remove flag from video: Video is not flagged")
        else:
            print("Cannot remove flag from video: Video does not exist")

    def _print_video(self, video):
        reason = self._flag_manager.get_reason(video)
        message = f"{video}"
        if reason:
            message = f"{message} - FLAGGED (reason: {reason})"
        return message

    def _print_video_title(self, video):
        reason = self._flag_manager.get_reason(video)
        message = f"{video.title}"
        if reason:
            message = f"{message} - FLAGGED (reason: {reason})"
        return message
