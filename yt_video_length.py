#!/usr/bin/env python

"""This script scrapes the length of youtube videos that are over a certain
number of minutes. It saves the results in a json file.
"""

import time
import json

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

def main():
    """Run the functions below. This code gets executed when in __main__.
    """
    chrome_driver_location = '/opt/chromedriver/chromedriver'
    url = 'https://www.youtube.com/user/sheepsempire/videos'
    filename = 'yt_video.json'
    wait = 3
    duration_over = 10  # get videos that are over X minutes in duration

    try:
        driver = webdriver.Chrome(chrome_driver_location)
        driver.get(url)

        get_all_videos(driver, wait, '.load-more-text')
        video_index = get_video_index(driver, duration_over, '.video-time')
        video_title = get_video_title(driver, video_index,
                                      'a.yt-uix-tile-link', 'title')
        output_json_file(video_title, filename)
    finally:
        driver.close()

def get_all_videos(driver, wait, css_selector):
    """Clicks on the load more button on the bottom of the page.
    Continuous for as long as there is a button.
    """
    time.sleep(wait)
    try:
        click_element = driver.find_element_by_css_selector(css_selector)
        while click_element.is_displayed():
            click_element.click()
            time.sleep(wait)
            click_element = driver.find_element_by_css_selector(css_selector)
    except NoSuchElementException:
        pass

def get_video_index(driver, duration_over, css_selector):
    """Get all the videos that have a duration over a specific length in
    minutes.
    """
    get_time = driver.find_elements_by_css_selector(css_selector)
    index = []
    for i, j in enumerate(get_time):
        units_list = str(j.text).split(':')  # splitted list of [hours:]min:sec
        if len(units_list) == 3:
            length_in_min = int(units_list[0]) * 60 + int(units_list[1])
        else:
            length_in_min = int(units_list[0])
        if length_in_min > duration_over:
            index.append(i)
    return index

def get_video_title(driver, index, css_selector, attribute):
    """Get the video titles as they appear on the page based on the indices in
    index.
    """
    get_title = driver.find_elements_by_css_selector(css_selector)
    title = []
    for i, j in enumerate(get_title):
        if i in index:
            title.append(str(j.get_attribute(attribute)))
    return title

def output_json_file(title, filename):
    """Creates a file with video titles in json format"""

    json_title = json.dumps(title, indent=4)
    with open(filename, 'w') as output:
        output.write(json_title)

if __name__ == '__main__':
    main()
