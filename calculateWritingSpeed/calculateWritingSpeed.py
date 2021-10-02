#!/usr/bin/python
"""
This program calculates the writing speed for a dummy text
Creation date 09/30/2021
Author Jankol643
Dependencies: mechanize (https://github.com/python-mechanize/mechanize), validators (https://github.com/kvesteri/validators), random_user_agent (https://github.com/Luqman-Ud-Din/random_user_agent/), beautifulsoup4 (https://www.crummy.com/software/BeautifulSoup/)
"""

import mechanize # for scraping website for dummy text
#import validators # for input check
#for random user agent when scraping website
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import Popularity
import os # for file manipulations
from datetime import datetime as DateTime, timedelta as TimeDelta # for setting timeout
from bs4 import BeautifulSoup # for getting HTML elements of website

def calculate_speed(time):
    
    def decide_text():
        text_source = input("Would you like to get a dummy text from the internet or from a file? (internet/file)")
        if text_source in ('INTERNET', 'Internet', 'internet'):
            text = getTextFromURL()
            return 'internet'
        if text_source in ('FILE', 'File', 'file'):
            filepath = input("Please specify a filepath")
            os.path.isfile('filepath')
            return 'file'
            
    def getTextFromURL():
        URL = "https://www.lipsum.com/"    
        def check_input(URL):
            #if (validators.url(URL) == 'True'):
                #return True
            #else:
                #raise Exception("URL is not valid")
            return True
        
        def scrape_text(URL):
            
            def set_user_agent():
                set_popularity = ['POPULARITY.POPULAR.value', 'POPULARITY.COMMON.value']
                user_agent_rotator = UserAgent(Popularity = set_popularity, limit = 10000)
                random_user_agent = user_agent_rotator.get_random_user_agent()
                return {'User-Agent': random_user_agent,'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
            
            def handle_timeout(timeout):
                # Write last datetime script was run to file
                dir = os.path.dirname(os.path.abspath(__file__))
                file_name = "data.txt"
                file_path = os.path.join(dir, file_name)
                if os.path.exists(file_path):
                    first_execution = False
                    with open(file_path) as f:
                        last_execution = f.readline().rstrip()
                else:
                    first_execution = True
                    # create a file
                    with open(file_path, 'w') as fp:
                        fp.write(str(DateTime.now()))
                    last_execution = str(DateTime.now())
                    
                def raise_exception():
                    if (last_execution < next_execution and first_execution == False):
                        duration = (next_execution - last_execution).total_seconds()
                        msg = "Execution is only allowed every " + str(timeout) + " seconds to not disrupt the website. Next execution: " + str(next_execution) + "(in " + str(duration) + " seconds)"
                        raise Exception(msg)
                
                last_execution = DateTime.strptime(last_execution, '%Y-%m-%d %H:%M:%S.%f')
                next_execution = last_execution + TimeDelta(seconds = timeout)
            
                raise_exception()
            br = mechanize.Browser()
            #br.set_handle_robots(False)
            #br.set_handle_equiv(False)
            br.addheaders = [set_user_agent()]
            handle_timeout(60)
            response = br.open(URL)
            
            #Write current time to file
            dir = os.path.dirname(os.path.abspath(__file__))
            file_name = "data.txt"
            file_path = os.path.join(dir, file_name)
            if os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    f.write(str(DateTime.now()))
            else:
                # create a file
                with open(file_path, 'w') as fp:
                        fp.write(str(DateTime.now()))
            
            soup = BeautifulSoup(response.get_data())
            all_paragraphs = soup.find_all('p')
            print(all_paragraphs)

        if check_input(URL) == True:
            scrape_text(URL)
            
    decision = decide_text()
    if (decision == 'internet'):
        getTextFromURL()
    
    def print_text(text):
        def print_separator(n):
            separator = ''
            char = '='
            i = 0
            while (i < n) :
                separator += char
            print(separator)
        
        n = 80 # number of separator characters
        print_separator(n)
        #print_text(text)
        print_separator(n)
        
if __name__ == '__main__':
    time = int(input("Please enter how long the test should take: "))
    res = calculate_speed(time)