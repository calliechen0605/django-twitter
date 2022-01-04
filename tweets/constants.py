class TweetPhotoStatus:
    PENDING = 0
    APPROVED = 1
    REJECTED = 2

# will show up in admin
TWEET_PHOTO_STATUS_CHOICES = (
    (TweetPhotoStatus.PENDING, 'Pending'),
    (TweetPhotoStatus.PENDING, 'Approved'),
    (TweetPhotoStatus.PENDING, 'Rejected'),
)

TWEET_PHOTO_UPLOAD_LIMIT = 9