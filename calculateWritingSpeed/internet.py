"""
Gets a text from a URL and cleans the HTML
Creation 2021/10/03
Dependencies: mechanize (https://github.com/python-mechanize/mechanize), validators (https://github.com/kvesteri/validators), random_user_agent (https://github.com/Luqman-Ud-Din/random_user_agent/), beautifulsoup4 (https://www.crummy.com/software/BeautifulSoup/)
"""

#Necessary for importing file from parent folder
import os
import sys
currentdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import masterUtil
import fileUtil
import mechanize # for scraping website for dummy text
#import validators # for input check
#for random user agent when scraping website
from random_user_agent.user_agent import UserAgent
from datetime import datetime as DateTime, timedelta as TimeDelta # for setting timeout
from bs4 import BeautifulSoup # for getting HTML elements of website
import os

def get_data_path():
    """
    Gets the path of the data.txt file
    :returns: path to file
    """
    dir = os.path.dirname(os.path.abspath(__file__))
    file_name = "data.txt"
    file_path = os.path.join(dir, file_name)
    return file_path

def is_first_execution():
    """
    Checks if script is executed the first time
    :returns: true if script is executed the first time
    """
    file_path = get_data_path()
    if os.path.exists(file_path):
        first_execution = False
        return False
    else:
        first_execution = True
        return True

def get_text_from_URL():
    """
    Gets text from a URL
    :returns: text from URL
    """
    URL = "https://www.lipsum.com/"

    def check_input(URL):
        """
        Checks if given URL is valid
        :string URL: url to check
        :returns: true if url is valid
        :raises ValueError: url is invalid
        """
        #if (validators.url(URL) == 'True'):
            #return True
        #else:
            #raise ValueError("URL is not valid")
        return True
    
    def scrape_text(URL):
        """
        Scrapes a text from a URL
        :returns: text from URL
        """

        def set_random_user_agent():
            """
            Sets a random user agent
            :returns: random user agent
            """
            set_popularity = ['POPULARITY.POPULAR.value', 'POPULARITY.COMMON.value']
            user_agent_rotator = UserAgent(Popularity = set_popularity, limit = 10000)
            random_user_agent = user_agent_rotator.get_random_user_agent()
            return {'User-Agent': random_user_agent,'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

        def handle_timeout(timeout):
            """
            Ensures that website is only scraped every timeout seconds
            :int timeout: timeout in seconds
            """

            if is_first_execution() is False:
                last_execution = fileUtil.access_file_line(get_data_path(), 1, False, 'r')
            else:
                # create a file
                now = str(DateTime.now())
                fileUtil.access_file_line(get_data_path(), 1, 'w', False, now)
                last_execution = now
                
            def raise_exception(last_execution, next_execution, first_execution):
                """
                Raises an exception if website would be scraped too often
                :datetime last_execution: date and time of last execution
                :datetime next_execution: date and time of next execution
                :boolean first_execution: True if script is executed for the first time
                :raises Exception: last execution is before next execution and first_execution is false
                """
                if (last_execution < next_execution and first_execution == False):
                    duration = (next_execution - last_execution).total_seconds()
                    msg = "Execution is only allowed every " + str(timeout) + " seconds to not disrupt the website. Next execution: " + str(next_execution) + "(in " + str(duration) + " seconds)"
                    raise Exception(msg)
            
            last_execution = DateTime.strptime(last_execution, '%Y-%m-%d %H:%M:%S.%f')
            next_execution = last_execution + TimeDelta(seconds = timeout)
        
            #raise_exception(last_execution, next_execution, first_execution)

        br = mechanize.Browser()
        #br.set_handle_robots(False)
        #br.set_handle_equiv(False)
        br.addheaders = [set_random_user_agent()]
        handle_timeout(60)
        response = br.open(URL)
        
        #Write current time to file
        fileUtil.access_file_line(get_data_path(), 1, 'w', False, str(DateTime.now()))
        
        soup = BeautifulSoup(response.get_data())
        all_paragraphs = soup.find_all('p')
        string = ''
        for item in all_paragraphs:
            string += str(item)
        all_paragraphs = string.replace('[', '')
        all_paragraphs = string.replace(']', '')
        text = masterUtil.clean_HTML(all_paragraphs, False)
        fileUtil.access_file_line(get_data_path(), 1, 'w', False, '\n')
        fileUtil.access_file_line(get_data_path(), 2, 'w', False, text)
        return text

    if is_first_execution() == True:
        if check_input(URL) == True:
            text = scrape_text(URL)
    else:
        text = fileUtil.access_file_line(get_data_path(), 2, 'r', False)
    return text