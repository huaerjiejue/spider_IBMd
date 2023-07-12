"""
todo: 1. get the quote from the website and save it
      2. get the picture from the website and save it
      3. get the main information about the fime and save it
      4. get the review from the website and save it
      5. put them together and save it as a docx file
"""

import requests
from bs4 import BeautifulSoup


# import os


class IBMD(object):
    def __init__(self, label):
        self.label = label
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebK'
                          'it/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safar'
                          'i/537.36 Edg/113.0.1774.50',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,i'
                      'mage/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
        }
        # https://www.imdb.com/title/tt2194499/
        self.main_url = 'https://www.imdb.com/title/' + self.label + '/'
        self.quotes = []  # quotes
        self.characters = []  # characters
        self.one_picture = ''  # one picture
        self.pictures = []  # pictures
        self.director = ''  # director
        self.writer = ''  # writer
        self.story_line = ''  # story line
        self.title = ''  # title
        self.basic_info = []  # release_data reting_film film_length
        self.reviews = []  # review
        self.review_titles = []  # review title
        self.urls_picture = []  # urls of pictures

    def get_quote(self, num=20):
        print("getting the quote...")
        # https://www.imdb.com/title/tt2194499/quotes/?ref_=tt_trv_qu
        quote_url = self.main_url + 'quotes/?ref_=tt_trv_qu'
        res = requests.get(quote_url, headers=self.headers)
        soup = BeautifulSoup(res.text, 'lxml')
        sub_section = soup.find('div', attrs={'data-testid': 'sub-section'})
        items = sub_section.find_all('div', attrs={'data-testid': 'item-id'})
        for count, item in enumerate(items):
            if count < num:
                quote = item.find('div', attrs={'data-testid': 'quote'}).get_text(strip=True)
                self.quotes.append(quote)
                print(quote)
            else:
                break
        print('getting the quote done!')

    def get_one_picture(self):
        res = requests.get(self.main_url, headers=self.headers)
        soup = BeautifulSoup(res.content, 'lxml')
        pic = soup.find('a', attrs_='ipc-lockup-overlay ipc-focusable')
        pic_url_tail = pic['href']
        print('getting the url of pic...')
        pic_url = 'https://www.imdb.com/' + pic_url_tail
        res = requests.get(pic_url, headers=self.headers)
        soup = BeautifulSoup(res.content, 'lxml')
        div_media = soup.find('div', attrs={'data-testid': "media-viewer"})
        div = div_media.find('div', style=True)
        pic_url = div['src']
        pic_content = requests.get(pic_url).content
        print('downloading the picture!!!')
        # put the picture into the self.one_picture
        self.one_picture = pic_content
        if self.one_picture != '':
            print('downloading the picture done!')
        else:
            print('downloading the picture failed!')

    def get_info_characters(self):
        res = requests.get(self.main_url, headers=self.headers)
        soup = BeautifulSoup(res.content, 'lxml')
        characters = soup.find_all('div', attrs={'data-testid': 'title-cast-item'})
        for character in characters:
            real_name = character.find('a', calss_='ipc-lockup-overlay')['aria-label']
            character_name = character.find('span').get_text(strip=True)
            print(real_name + ' as ' + character_name)
            self.characters.append([real_name, character_name])
        print('getting the characters done!')

    def get_director_writer(self):
        print('getting the director and writer...')
        res = requests.get(self.main_url, headers=self.headers)
        soup = BeautifulSoup(res.content, 'lxml')
        director_writer = soup.find_all('a', class_='ipc-metadata-list-item__list-content-item')
        director = director_writer[0].get_text(strip=True)
        writer = director_writer[1].get_text(strip=True)
        print('director: ' + director)
        print('writer: ' + writer)
        self.director = director
        self.writer = writer
        print('getting the director and writer done!')

    def get_story_line(self):
        print('getting the story line...')
        # https://www.imdb.com/title/tt2194499/plotsummary/?ref_=tt_ov_pl
        story_line_url = self.main_url + 'plotsummary/?ref_=tt_ov_pl'
        res = requests.get(story_line_url, headers=self.headers)
        soup = BeautifulSoup(res.content, 'lxml')
        sections = soup.find_all('section', attrs={'class': 'ipc-page-section ipc-page-section--base'})
        # there is 3 section, we need the second one
        story_line_section = sections[1]
        self.story_line = story_line_section.get_text(strip=True)
        print('getting the story line done!')

    def get_title(self):
        print('getting the title...')
        res = requests.get(self.main_url, headers=self.headers)
        soup = BeautifulSoup(res.content, 'lxml')
        h1 = soup.find('h1', attrs={'data-testid': 'hero__pageTitle'})
        self.title = h1.get_text(strip=True)
        print('getting the title done!')

    def get_basic_info(self):  # release_data film_rating film_length
        print('getting the basic info...')
        res = requests.get(self.main_url, headers=self.headers)
        soup = BeautifulSoup(res.content, 'lxml')
        h1 = soup.find('h1', attrs={'data-testid': 'hero__pageTitle'})
        ul = h1.next_sibling()
        li_list = ul.find_all('li')
        print('getting the time of release_data...')
        release_data = li_list[0].get_text(strip=True)
        print('release: ' + release_data)
        self.basic_info.append(release_data)
        print('getting the rate fo film...')
        film_rating = li_list[1].get_text(strip=True)
        print('film_rating: ' + film_rating)
        self.basic_info.append(film_rating)
        print('getting the length of film...')
        film_length = li_list[2].get_text(strip=True)
        print('film_length: ' + film_length)
        self.basic_info.append(film_length)
        print('getting the basic info...')
        """
        release_data : self.basic_info[0]
        film_rating : self.basci_info[1]
        film_length : self.basic_info[2]
        """

    def get_pictures(self, num=10):

        # url = "https://www.imdb.com/title/tt2194499/mediaindex?ref_=tt_ov_mi_sm"
        print('getting the pictures...')
        pictures_url = self.main_url + 'mediaindex?ref_=tt_ov_mi_sm'
        res = requests.get(pictures_url, headers=self.headers)
        soup = BeautifulSoup(res.content, 'lxml')
        media_list = soup.find('div', attrs={'class': 'media_index_thumb_list'})
        urls = media_list.find_all('a')
        for i in range(num):
            print('getting the picture ' + str(i) + '...')
            img = urls[i].find('img')
            img_url = img['src']
            self.urls_picture.append(img_url)
            print('getting the picture ' + str(i) + ' done!')
        print('getting the pictures done!')

    def get_reviews(self):
        # url = 'https://www.imdb.com/title/tt2085059/reviews?ref_=tt_urv'
        review_url = self.main_url + 'reviews?ref_=tt_urv'
        res = requests.get(review_url, headers=self.headers)
        print('getting the reviews...')
        soup = BeautifulSoup(res.content, 'lxml')
        lister_list = soup.find('div', attrs={'class': 'lister-list'})
        lister_list_items = lister_list.find_all('div', attrs={'class': 'lister-item-content'})
        for lister_list_item in lister_list_items:
            # get the title and text of the review
            title = lister_list_item.find('a', attrs={'class': 'title'}).get_text(strip=True)
            text = lister_list_item.find('div', attrs={'class': 'text show-more__control'}).get_text(strip=True)
            self.reviews.append(title)
            self.reviews.append(text)
        print('getting the reviews done!')
