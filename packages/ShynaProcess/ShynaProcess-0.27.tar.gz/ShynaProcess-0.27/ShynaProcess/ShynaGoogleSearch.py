from googlesearch import search


class ShynaGoogleSearch:
    """
    perform google search and return the result in form of link.
    define search string as class property.

    Two functions:
    search_google_with_top_result -  Return only one link result
    search_google_with_limit_result - ask for number of result needed and return result in form of link.
    """
    search_string = ''

    def search_google_with_top_result(self):
        return search(term=self.search_string, num_results=0)

    def search_google_with_limit_result(self, result_number):
        return search(term=self.search_string, num_results=result_number)
