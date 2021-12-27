from testing.testcases import TestCase


class CommentModelTests(TestCase):

    def test_comment(self):
        user = self.create_user('linghu', 'linghu@gmail.com')
        tweet = self.create_tweet(user)
        comment = self.create_comment(user, tweet)
        print(comment)
        self.assertEqual(comment.__str__(), None)
