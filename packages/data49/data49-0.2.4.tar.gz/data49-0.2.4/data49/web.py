import contextlib
import enum
import functools
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Union, ContextManager
import importlib

from requests import get, post  # As for API
import selenium.common.exceptions as selenium_exceptions
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.remote import webdriver, webelement
from selenium.webdriver.support import expected_conditions  # As for API
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from . import internal


__all__ = [
    "get_browser",
    "Browser",
    "BrowserType",
    "BrowserContext",
    "Element",
    "expected_conditions",
    "get",
    "post",
]


class BrowserType(enum.Enum):
    """An enumeration of popular, supported browsers for browser automation"""

    CHROME = "Chrome"
    SAFARI = "Safari"
    FIREFOX = "Firefox"


def get_browser(
    priority=(BrowserType.CHROME, BrowserType.FIREFOX, BrowserType.SAFARI)
) -> str:
    def _(browser_name: BrowserType):
        try:
            getattr(
                importlib.import_module(".webdriver", "selenium"),
                browser_name.value,
            )().close()
        except selenium_exceptions.WebDriverException:
            return None
        else:
            return browser_name

    found = functools.reduce(lambda x, y: x or y, map(_, priority))
    if found is None:
        # TODO: Download geckodriver and use it
        raise RuntimeError("Could not find any browser")
    return found


@internal.add_typo_safety
@dataclass
class Element:
    """Represents a DOM element.

    Should not be instantiated directly but instead with methods like :meth:`BrowserContext.query_selector`
    """

    item: webelement.WebElement

    def soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.item.get_attribute("innerHTML"))

    def __getitem__(self, attr: str) -> Optional[Any]:
        return self.item.get_attribute(attr)

    def click(self) -> None:
        self.item.click()

    def send_keys(self, keys) -> None:
        self.item.send_keys(keys)


@internal.add_typo_safety
@dataclass
class BrowserContext:
    url: str
    driver: webdriver.WebDriver
    _waits: Dict[float, WebDriverWait] = field(default_factory=dict)

    def query_selector(self, css_selector: str) -> Element:
        return Element(self.driver.find_element(By.CSS_SELECTOR, css_selector))

    def query_selector_all(self, css_selector: str) -> List[Element]:
        return list(
            map(Element, self.driver.find_elements(By.CSS_SELECTOR, css_selector))
        )

    def js(self, javascript: str) -> Any:
        return self.driver.execute_script(javascript)

    def _get_wait_up_to(self, seconds: float) -> WebDriverWait:
        if seconds not in self._waits:
            self._waits[seconds] = WebDriverWait(self.driver, seconds)
        return self._waits[seconds]

    def wait(
        self,
        until: Callable[[webdriver.WebDriver], Union[webelement.WebElement, bool]],
        up_to: float = 10.0,
    ) -> Element:
        """Wait until an element is located.

        Returns that `Element` if found under `up_to`, the time limit in seconds.

        Raises `TimeoutError` if the element is not found in time.

        Args:
            until (Callable[[webdriver.WebDriver], Union[webelement.WebElement, bool]]):
                        An object that when `__call__` is called,
                        return `False` indicating that the element was not found
                        or the `selenium.webdriver.remote` when found.
                        You may use Selenium's `expected_conditions`.
            up_to (float): The time limit in seconds. Defaults to 10.0.

        Returns:
            Element: The element that was found

        Raises:
            TimeoutError: The element was not found in time.

        """
        try:
            return Element(self._get_wait_up_to(up_to).until(until))
        except selenium_exceptions.TimeoutException as error:
            raise TimeoutError(
                f"Could not find element under {up_to} seconds"
            ) from error

    # def wait_until  # Recieves a function that returns boolean as parameter. Polls.

    # Aliases


@internal.add_typo_safety
@dataclass
class Browser(contextlib.AbstractContextManager):
    url: str
    start_browser: Optional[webdriver.WebDriver] = None

    def open(self) -> BrowserContext:
        self.driver = self.start_browser()
        self.driver.get(self.url)
        return BrowserContext(self.url, self.driver)

    def close(self) -> None:
        self.driver.close()

    def __post_init__(self) -> None:
        if self.start_browser is None:
            self.start_browser = getattr(webdriver, get_browser())

    def __enter__(self) -> BrowserContext:
        return self.open()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
