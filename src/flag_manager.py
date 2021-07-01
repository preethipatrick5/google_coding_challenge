class FlagManager:
    def __init__(self):
        self.flagged_videos = {}

    def flag_video(self, video, reason):
        if video.video_id in self.flagged_videos.keys():
            return self.flagged_videos[video.video_id], False
        else:
            reason = "Not supplied" if reason == "" else reason
            self.flagged_videos[video.video_id] = reason
            return reason, True

    def allow_video(self, video):
        if video.video_id in self.flagged_videos.keys():
            self.flagged_videos.pop(video.video_id)
            return True
        else:
            return False

    def get_flagged_video_ids(self):
        return list(self.flagged_videos.keys())

    def is_flagged(self, video):
        return video.video_id in self.flagged_videos.keys()

    def get_reason(self, video):
        return self.flagged_videos.get(video.video_id, None)
