from model import UrlShortener, Base
from db_manager import DbManager, ORMHelper
from urllib.parse import urlparse
from constants import CHARACTERS, BASE


class ApiExecutor:
    def __init__(self):
        self.db_manager = DbManager()
        self.db_manager.db_init()
        self.session = self.db_manager.get_session()

    def _get_domain_name(self, url):
        domain_name = urlparse(url).netloc
        domain_name_list = domain_name.split(".")
        if "www" in domain_name:
            final_domain_name_list = domain_name_list[1:-1]
        else:
            final_domain_name_list = domain_name_list[:-1]
        final_domain_name = ".".join(final_domain_name_list)
        return final_domain_name

    def create_url_shortener(self, url):
        ## check if url is already in table
        results = self.get_short_url(url)
        if len(results) > 0:
            for result in results:
                shorten_url = result.short_url
                if shorten_url:
                    return shorten_url

        ## Generate and add short url to table
        domain_name = self._get_domain_name(url)
        entries = {
            "original_url": url,
            "domain_name": domain_name
                }
        ORMHelper().add(UrlShortener, **entries)
        post_results = ORMHelper().get(UrlShortener, **entries)
        for post_result in post_results:
            short_url = self._generate_short_url(post_result.id)
            entries.update({"short_url": short_url})
            ORMHelper().add(UrlShortener, **entries)
        return self.get_short_url(url)


    def _generate_short_url(self, unique_id):
        """Encodes a number into a Base62 string."""
        if unique_id == 0:
            return CHARACTERS[0]
        encoded = []
        while unique_id:
            remainder = unique_id % BASE
            encoded.append(CHARACTERS[remainder])
            unique_id //= BASE
        return ''.join(encoded[::-1])

    def get_short_url(self,url):
        query_filter = {"original_url": url}
        result = ORMHelper().get(UrlShortener, **query_filter)
        return result