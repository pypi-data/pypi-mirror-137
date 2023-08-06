# imports go here


class CrawlerException(Exception):
    message = "Something went wrong while working on {}"

    def __init__(self, profile_name="", message=""):
        self.profile_name = profile_name
        self.message = message or self.message
        self.message = self.message.format(profile_name)
        super(CrawlerException, self).__init__(message)


class ProfileNotDownloadedError(CrawlerException):
    message = "Could not download Profile.pdf for linkedin.com/in/{}"


class ResumeParserError(CrawlerException):
    message = "Parsed JSON for {} not properly formatted"


class UnclickableButtonError(CrawlerException):
    message = "Could not download Profile.pdf for {} as button " \
              "couldn't be clicked"


class CannotSolveGoogleChallenge(CrawlerException):
    message = "Could not complete search as Google challenge " \
              "could not be automatically solved"
