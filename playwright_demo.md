# Playwright Demo

Just some notes for the Thursday playwright code demo. Playwright documentation
for python can be found at <https://playwright.dev/python/>. Start by linking to
the web pages.

## Fun notes

- Has multiple APIs: python, Node.js, java, .NET

## Installing

<https://playwright.dev/python/docs/intro#installation>

```bash
pip install --upgrade pip
# Installs the playwright package and pytest plugin
pip install playwright
# This step downloads and installs browser binaries for Chromium, Firefox and WebKit
playwright install
# Installs a 3rd party pytest plugin for saving and comparing playwright screenshots
pip install pytest-playwright-visual
```

## Locators

<https://playwright.dev/python/docs/next/api/class-locator>

Locators represent a way to find elements on the page. They use selectors which
look a lot like javascript JQuery selectors. A locator can find one or more elements
on the page. You can chain calls off of locators to fine-tune what you're looking for.
For instance you could locate all the tables, then chain a filter call to get one specific
table from the bunch. Once you have a locator you like, you can make calls off of it
to manipulate that element or get information about that element. For instance
there is a `.click()` method to mouse-click the middle of that locator or a `.count()`
method to get how many elements are found by that locator. Note that if more than
one element was found with the locator, the `.click()` method would throw an error.

## Assertions

<https://playwright.dev/python/docs/test-assertions>

There is an `expect()` object in playwright that can be used to make assertions.
It's useful because it will wait and retry an assertion until the desired condition
is met or a timeout is reached. You can assert on a wide range of things.

## codegen

<https://playwright.dev/python/docs/codegen>

```bash
# e.g. playwright codegen localhost:8080/playground
playwright codegen WEBPAGE
```

This command opens a web browser to the specified page and a text document.
It records all of the actions you take on the page to the text document as
a playwright script that you can copy and run to reproduce what you did during the
`codegen` session. It is especially useful for identifying `locator`s to use
in a pytest.

## pytest

For the pytest section work interactively by running my demo tests and running
the flags in the command line.

<https://playwright.dev/python/docs/test-runners#cli-arguments>

```bash
pytest LOCATION
```

Playwright comes with a built in pytest extension and can be further extended with
`pytest-playwright-visual` to do visual comparisons of browser screenshots taken
during tests.

### Flags

<https://playwright.dev/python/docs/test-runners#cli-arguments>

- `--headed`: Run tests in headed mode so you can see the browser (defaults to headless).
- `--slowmo=MS`: Add `MS` pauses in milliseconds between commands to make it so you can see what's happening.
- `--browser=BROWSER`: Run tests in a different browser chromium, firefox, or webkit. It can be specified multiple times (default: all browsers).
- `--screenshot=only-on-failure`: retain a screenshot of the end browser state on failure.
- `--video=retain-on-failure`: retain a video of the browser during the test on failure.

### debugger

<https://playwright.dev/python/docs/debug#run-in-debug-mode>

```bash
PWDEBUG=1 pytest playwright_demo/test_dre.py -k test_playground_basic
```

With the debugger tool you can step through a test in headed mode, one line
at a time. The debugger will also highlight the elements indicated on the
next line, along with a red dot for the mouse location for clicks on the next
line, etc.