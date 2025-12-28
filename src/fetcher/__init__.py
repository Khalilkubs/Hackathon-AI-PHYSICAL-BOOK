"""
URL Fetcher Module for Document Ingestion and Vector Storage System
Responsible for retrieving content from Docusaurus URLs with error handling
"""

import requests
from typing import Optional
from urllib.parse import urljoin, urlparse
import time
import logging

# Try to import selenium for JavaScript rendering, fall back to requests if not available
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("Selenium not available, falling back to requests only. Install selenium for JavaScript rendering.")

logger = logging.getLogger(__name__)


class URLFetcher:
    """
    Class to fetch content from Docusaurus URLs with proper error handling
    Supports both regular requests and JavaScript rendering via Selenium
    """

    def __init__(self, timeout: int = 30, max_retries: int = 3, use_selenium: bool = True):
        """
        Initialize the URL fetcher with configuration

        Args:
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            use_selenium: Whether to use Selenium for JavaScript rendering (requires selenium installation)
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.use_selenium = use_selenium and SELENIUM_AVAILABLE
        self.session = requests.Session()
        # Set a user agent to avoid being blocked by some sites
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; DocumentIngestor/1.0)'
        })

    def fetch_url(self, url: str) -> Optional[str]:
        """
        Fetch content from a given URL with retry logic
        Uses Selenium for JavaScript rendering if available and requested, otherwise falls back to requests

        Args:
            url: The URL to fetch content from

        Returns:
            The content of the page as a string, or None if failed
        """
        if self.use_selenium:
            return self._fetch_with_selenium(url)
        else:
            return self._fetch_with_requests(url)

    def _fetch_with_requests(self, url: str) -> Optional[str]:
        """Fetch content using requests library"""
        for attempt in range(self.max_retries + 1):
            try:
                response = self.session.get(
                    url,
                    timeout=self.timeout,
                    allow_redirects=True
                )

                # Check if the request was successful
                if response.status_code == 200:
                    logger.info(f"Successfully fetched {len(response.text)} characters from {url} using requests")
                    return response.text
                elif response.status_code == 404:
                    logger.warning(f"URL not found (404): {url}")
                    return None
                elif response.status_code == 429:
                    # Rate limited - wait before retrying
                    wait_time = (2 ** attempt) + 1  # Exponential backoff
                    logger.warning(f"Rate limited (429) for {url}, waiting {wait_time}s before retry {attempt + 1}/{self.max_retries}")
                    time.sleep(wait_time)
                    continue
                elif 400 <= response.status_code < 500:
                    logger.error(f"Client error ({response.status_code}) for URL: {url}")
                    return None
                elif 500 <= response.status_code < 600:
                    logger.warning(f"Server error ({response.status_code}) for URL: {url}, attempt {attempt + 1}/{self.max_retries}")
                    if attempt < self.max_retries:
                        wait_time = (2 ** attempt) + 1  # Exponential backoff
                        time.sleep(wait_time)
                        continue
                    else:
                        return None
                else:
                    logger.warning(f"Unexpected status code ({response.status_code}) for URL: {url}")
                    return None

            except requests.exceptions.Timeout:
                logger.warning(f"Request timeout for URL: {url}, attempt {attempt + 1}/{self.max_retries}")
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    return None

            except requests.exceptions.ConnectionError:
                logger.warning(f"Connection error for URL: {url}, attempt {attempt + 1}/{self.max_retries}")
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    return None

            except requests.exceptions.RequestException as e:
                logger.error(f"Request exception for URL {url}: {str(e)}")
                if attempt < self.max_retries:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                else:
                    return None

        logger.error(f"Failed to fetch URL after {self.max_retries} retries: {url}")
        return None

    def _fetch_with_selenium(self, url: str) -> Optional[str]:
        """Fetch content using Selenium for JavaScript rendering"""
        logger.info(f"Using Selenium to fetch content from {url}")

        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in background
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")

        driver = None
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.set_page_load_timeout(self.timeout)

            logger.info(f"Navigating to {url}")
            driver.get(url)

            # Wait for the main content to load (wait for the main element or article)
            try:
                # Wait for main content area to be present
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "main"))
                )
            except:
                # If main element doesn't appear quickly, try waiting for other content indicators
                try:
                    WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='doc']"))
                    )
                except:
                    # If no specific content found, just wait a bit more for page to load
                    pass

            # Additional wait to ensure dynamic content loads
            time.sleep(3)

            # Get the page source after JavaScript execution
            html_content = driver.page_source

            logger.info(f"Successfully fetched {len(html_content)} characters from {url} using Selenium")
            return html_content

        except Exception as e:
            logger.error(f"Error fetching {url} with Selenium: {e}")
            logger.info("Falling back to requests method")
            return self._fetch_with_requests(url)  # Fallback to requests
        finally:
            if driver:
                driver.quit()

    def is_valid_url(self, url: str) -> bool:
        """
        Validate if the URL is properly formatted

        Args:
            url: The URL to validate

        Returns:
            True if the URL is valid, False otherwise
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    def get_all_page_urls(self, base_url: str) -> list:
        """
        Get all page URLs from a Docusaurus site (simplified approach)
        Note: This is a basic implementation - a full crawler would be more complex

        Args:
            base_url: The base URL of the Docusaurus site

        Returns:
            List of URLs found on the site
        """
        # For now, we'll just return the base URL
        # A more sophisticated implementation would crawl the site to find all pages
        return [base_url]