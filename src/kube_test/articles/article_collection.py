class ArticleCollection:
    def __init__(self):
        self._articles = []

    def add(self, article):
        self._articles.append(article)

    def __len__(self):
        return len(self._articles)

    def __iter__(self):
        return ArticleCollectionIterator(self)

    def get_all_articles_tups(self):
        return [article.return_as_tup() for article in self._articles]

    def to_list(self):
        result = []
        for article in self._articles:
            result.append(
                {u"publish_time": str(article.publish_time), u"headline": article.headline, u"category": article.category}
            )
        return result
class ArticleCollectionIterator:
    def __init__(self, article_collection):
        # Team object reference
        self._article_collection = article_collection
        # member variable to keep track of current index
        self._index = 0

    def __next__(self):
        if self._index < len(self._article_collection._articles):
            result = self._article_collection._articles[self._index]
            self._index += 1
            return result
        raise StopIteration
