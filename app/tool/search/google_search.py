from typing import List

import requests
from googlesearch import search

from app.config import config
from app.logger import logger
from app.tool.search.base import WebSearchEngine


class GoogleSearchEngine(WebSearchEngine):
    def perform_search(
        self, query: str, num_results: int = 10, *args, **kwargs
    ) -> List[str]:
        """
        Google search engine using the official Google Custom Search API when configured,
        falling back to web scraping if not configured or if the API call fails.

        Args:
            query (str): The search query to submit to the search engine.
            num_results (int, optional): The number of search results to return. Default is 10.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            List[str]: A list of URLs matching the search query.
        """
        # Check for API configuration in the search settings
        search_config = getattr(config, "search_config", None)
        api_key = getattr(search_config, "api_key", None) if search_config else None
        cx = getattr(search_config, "cx", None) if search_config else None
        use_fallback = (
            getattr(search_config, "use_fallback", True) if search_config else True
        )

        # If API is configured, try using the Google Search API
        if api_key and cx:
            try:
                logger.info("Using Google Custom Search API for search")
                return self._api_search(query, api_key, cx, num_results)
            except requests.RequestException as e:
                # More specific error handling for HTTP-related errors
                status_code = (
                    getattr(e.response, "status_code", None)
                    if hasattr(e, "response")
                    else None
                )
                if status_code == 429:
                    logger.warning("Google API rate limit exceeded")
                elif status_code and 400 <= status_code < 500:
                    logger.warning(
                        f"Google API client error: {e} (status code: {status_code})"
                    )
                elif status_code and 500 <= status_code < 600:
                    logger.warning(
                        f"Google API server error: {e} (status code: {status_code})"
                    )
                else:
                    logger.warning(f"Google API request error: {e}")

                if not use_fallback:
                    logger.warning(
                        "Fallback to scraping is disabled. Returning empty results."
                    )
                    return []
                logger.info("Falling back to web scraping search")
            except Exception as e:
                # General error handling for other types of exceptions
                logger.warning(f"Google API error: {e}")
                if not use_fallback:
                    logger.warning(
                        "Fallback to scraping is disabled. Returning empty results."
                    )
                    return []
                logger.info("Falling back to web scraping search")

        # Use web scraping if API is not configured or if API call failed and fallback is enabled
        return self._scraping_search(query, num_results)

    @staticmethod
    def _api_search(
        query: str, api_key: str, cx: str, num_results: int = 10
    ) -> List[str]:
        """
        Perform a search using Google's Custom Search JSON API.

        Args:
            query (str): The search query.
            api_key (str): The API key for Google Custom Search.
            cx (str): The Custom Search Engine ID.
            num_results (int, optional): The number of results to return. Default is 10.

        Returns:
            List[str]: A list of URLs matching the search query.

        Raises:
            requests.RequestException: If there's an issue with the HTTP request.
            ValueError: If the response cannot be parsed as JSON.
        """
        base_url = "https://www.googleapis.com/customsearch/v1"
        results = []

        # API allows max 10 results per request, so we need to paginate
        for start_index in range(
            1, min(num_results + 1, 101), 10
        ):  # Google API limits to 100 results max
            params = {
                "q": query,
                "key": api_key,
                "cx": cx,
                "start": start_index,
                "num": min(
                    10, num_results - len(results)
                ),  # Can't request more than 10 at once
            }

            response = requests.get(base_url, params=params, timeout=10)  # Add timeout
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
            data = response.json()

            if "items" in data:
                for item in data["items"]:
                    if "link" in item:
                        results.append(item["link"])
                        if len(results) >= num_results:
                            return results
            else:
                # No more results or empty result set
                if (
                    "searchInformation" in data
                    and "totalResults" in data["searchInformation"]
                ):
                    logger.info(
                        f"Total results: {data['searchInformation']['totalResults']}"
                    )
                break

        return results

    @staticmethod
    def _scraping_search(query: str, num_results: int = 10) -> List[str]:
        """
        Perform a search using web scraping as a fallback method.

        Args:
            query (str): The search query.
            num_results (int, optional): The number of results to return. Default is 10.

        Returns:
            List[str]: A list of URLs matching the search query.
        """
        try:
            return list(search(query, num_results=num_results))
        except Exception as e:
            logger.warning(f"Web scraping search failed: {e}")
            return []
