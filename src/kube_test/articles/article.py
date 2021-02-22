class Article:
    def __init__(self, headline=None, category=None, publish_time=None):
        self.headline = headline
        self.category = category
        self.publish_time = publish_time

    def __str__(self):
        return f"publish time: {self.publish_time} - headline: {self.headline} - category: {self.category}"

    def return_as_tup(self):
        return self.publish_time, self.headline, self.category
