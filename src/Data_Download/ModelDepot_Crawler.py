#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import selenium.webdriver as webdriver
from selenium.webdriver.firefox.options import Options

# %% PATH

RELATIVE_PATH = "../data.nosync/"


# %%
def init_browser(headless=False):
    """
    Initialize selenium browser
    NEEDS TO BE CLOSED ( *.close() )

    :Returns:
        - webdriver element
    """

    GECKO_DRIVER_PATH = RELATIVE_PATH + "Cloning/requirements/geckodriver"
    options = Options()
    options.headless = headless
    browser = webdriver.Firefox(options=options, executable_path=GECKO_DRIVER_PATH)
    return browser


# %%
def get_results_DS(search_term, search_framework="", search_language="", search_category=""):
    """
    Gets search result from DeepSearch by keyword

    :Returns:
        - Array of GitHub links
    """

    # get URL
    url = "https://modeldepot.io/search/results? CATEGORY q= TERM  FRAMEWORK  LANGUAGE "
    url = url.replace(' TERM ', search_term)
    url = url.replace(' FRAMEWORK ', "&framework=" + search_framework)
    url = url.replace(' LANGUAGE ', "&language=" + search_language)
    url = url.replace(' CATEGORY ', "category=" + search_category + "&")

    # open browser
    browser = init_browser()
    browser.get(url)

    # scroll page to load
    eor_found = False
    while not eor_found:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(.1)
        try:
            browser.find_element_by_class_name("end-results")
        except:
            eor_found = False
        else:
            eor_found = True

    # scrape HTML
    links = browser.find_elements_by_xpath("//span[@class=\"cite\"]")
    results = []
    for link in links:
        href = link.text
        results.append(href)
    print("{} github links found".format(len(results)))

    browser.close()

    return results


# %%
def get_arxivIDs(github_urls):
    """
    Gets arxiv paper ID from list of github_url

    :Returns:
        - Array of Array of arxiv ID's
    """

    PAGE_CAP = 100

    pages_visited = 0
    ID_list = []
    total = len(github_urls)

    browser = init_browser(headless=True)
    for url in github_urls:
        if pages_visited % PAGE_CAP == 0:
            browser.quit()
            browser = init_browser(headless=True)
        ID_list.append(get_arxiv_ID(browser, url))
        pages_visited += 1
        progress(pages_visited, total)
    browser.quit()

    return ID_list


# %%
def get_arxiv_ID(browser, github_url):
    """
    Gets arxiv paper ID from github_url

    :Returns:
        - Array of arxiv ID's
    """

    # get URL
    url = "https://github.com/PATH"
    url = url.replace('PATH', github_url)

    # open browser
    browser.get(url)

    time.sleep(.2)

    # verify if 404
    page_404 = browser.find_elements_by_xpath("//title[contains(text(),\'Page not found\')]") != []
    if page_404:
        results = '404'
    else:
        # scrape HTML
        results = []
        links = browser.find_elements_by_xpath("//a[contains(@href,\'arxiv.org/\')]")
        for link in links:
            href = link.get_attribute("href")
            if ".pdf" in href:
                arxivID = href[-14:-4]
            elif "v" in href[-12:]:
                arxivID = href[-12:]
            else:
                arxivID = href[-10:]
            arxivID = arxivID.replace("/", "")
            if arxivID not in results:
                results.append(arxivID)

    return results


# %%
def get_depends(github_urls):
    """
    Gets dependents & dependencies from list of github_url

    :Returns:
        - dictionnary of Array of Array of dependents & dependencies
    """

    PAGE_CAP = 100

    pages_visited = 0
    depend_dict = {'dependents': [], 'dependencies': []}
    total = len(github_urls)

    browser = init_browser(headless=True)
    for url in github_urls:
        if pages_visited % PAGE_CAP == 0:
            browser.quit()
            browser = init_browser(headless=True)
        dep = get_depend(browser, url, dependencies=False)
        depend_dict['dependents'].append(dep[1])
        depend_dict['dependencies'].append(dep[0])
        pages_visited += 1
        progress(pages_visited, total)
    browser.quit()

    return depend_dict


# %%
def get_depend(browser, github_url, dependencies=False, dependants=False):
    """
    Gets dependencies ID from github_url

    :Returns:
        - Array of dependencies
    """

    # get URL
    url = "https://github.com/PATH/network/DEP"
    url = url.replace('PATH', github_url)
    if dependencies == dependants:
        dependencies = get_depend(browser, github_url, dependencies=True)
        dependants = get_depend(browser, github_url, dependants=True)
        return (dependencies, dependants)
    elif dependencies == True:
        url = url.replace('DEP', 'dependencies')
    elif dependants == True:
        url = url.replace('DEP', 'dependents')

        # open browser
    browser.get(url)

    time.sleep(.2)

    # verify if 404
    page_404 = browser.find_elements_by_xpath("//title[contains(text(),\'Page not found\')]") != []
    if page_404:
        depend = '404'
    else:
        # scrape HTML
        depend = []
        pages_left = True
        while (pages_left):
            links = browser.find_elements_by_xpath(
                "//a[contains(@data-hovercard-type,\'repository\') and (contains(@class,\'text-bold\') or contains(@data-octo-click,\'dep_graph_package\'))]")
            for link in links:
                url = link.get_attribute("href")
                dep = url[19:]  # remove 'github.com'
                if dep not in depend:
                    depend.append(dep)
            buttons = browser.find_elements_by_xpath("//a[contains(@class,\'btn btn-outline BtnGroup-item\')]")
            for b in buttons:
                if b.text == 'Next':
                    next_button = b
            try:
                url = next_button.get_attribute("href")
            except:
                pages_left = False
            else:
                browser.get(url)

    return depend


# %%
def get_number_results(search_term, search_framework="", search_language="", search_category=""):
    """
    Gets number of search result from DeepSearch by keyword

    :Returns:
        - int of numbers
    """

    # get URL
    url = "https://modeldepot.io/search/results? CATEGORY q= TERM  FRAMEWORK  LANGUAGE "
    url = url.replace(' TERM ', search_term)
    url = url.replace(' FRAMEWORK ', "&framework=" + search_framework)
    url = url.replace(' LANGUAGE ', "&language=" + search_language)
    url = url.replace(' CATEGORY ', "category=" + search_category + "&")

    # open browser
    browser = init_browser(headless=True)
    browser.get(url)

    # scrape HTML
    count = browser.find_element_by_xpath("//div[@class=\"count\"]")
    result = int(count.text[0:-8])

    browser.close()

    return result


# %%
def progress(current, total):
    print("Currently at {:.2f}%".format(current / total * 100))
