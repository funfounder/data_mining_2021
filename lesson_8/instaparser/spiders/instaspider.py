import scrapy
import re
import json
from copy import deepcopy
from urllib.parse import urlencode
from scrapy.http import HtmlResponse
from lesson_8.instaparser.items import InstaparserItem
from lesson_8.instaparser.credentials import instagram_login, instagram_password

class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']

    instagram_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    instagram_login = instagram_login
    instagram_password = instagram_password
    users_list = ['ai_machine_learning', 'tribunaby']
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    query_posts_hash = '8c2a529969ee035a5063f2fc8602a0fd'
    users_type = ['followers', 'following']

    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(self.instagram_login_link,
                                 method='POST',
                                 callback=self.login,
                                 formdata={'username': self.instagram_login,
                                           'enc_password': self.instagram_password},
                                 headers={'x-csrftoken': csrf})

    def login(self, response: HtmlResponse):
        j_data = response.json()
        if j_data['authenticated']:
            for user in self.users_list:
                yield response.follow(f'/{user}', callback=self.profile_data_parsing, cb_kwargs={'username': user})

    def profile_data_parsing(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        for type in self.users_type:
            yield response.follow(f'https://i.instagram.com/api/v1/friendships/{user_id}/{type}/?count=12',
                                  callback=self.user_data_parse,
                                  cb_kwargs={'username': deepcopy(username),
                                             'user_id': deepcopy(user_id),
                                             'user_type': type})

   # def user_parsing(self, response: HtmlResponse, username):
    #     user_id = self.fetch_user_id(response.text, username)
    #     variables = {'id': user_id,
    #                  'first': 12}
    #     url_posts = self.graphql_url + f'query_hash={self.query_posts_hash}&{urlencode(variables)}'
    #     yield response.follow(url_posts,
    #                           callback=self.user_data_parse,
    #                           cb_kwargs={'username': username,
    #                                      'user_id': user_id,
    #                                      'variables': deepcopy(variables)})

    def user_data_parse(self, response:HtmlResponse, username, user_id, user_type):
        # user_type = user_type
        # user_id = user_id
        # username = username
        j_data = response.json()
        if j_data.get('next_max_id'):
            max_id = j_data.get('next_max_id')
            for user_type in self.users_type:
                yield response.follow(f'https://i.instagram.com/api/v1/friendships/{user_id}/{user_type}/?count'
                                      f'=12&max_id={max_id}',
                                      callback=self.user_data_parse,
                                      cb_kwargs={'username': deepcopy(username),
                                                 'user_id': deepcopy(user_id),
                                                 'user_type': type})
        for uid in j_data.get('users'):
            item = InstaparserItem(user_id=user_id,
                                   user_fullname=username,
                                   subuser_type=user_type,
                                   subuser_id=uid.get('pk'),
                                   subuser_fullname=uid.get('full_name'),
                                   subuser_link_to_pic=uid.get('profile_pic_url'))
            yield item

    # def user_data_parse(self, response:HtmlResponse, username, user_id, variables):
    #     j_data = response.json()
    #     page_info = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('page_info')
    #     if page_info.get('has_next_page'):
    #         variables['after'] = page_info.get('end_cursor')
    #         url_posts = self.graphql_url + f'query_hash={self.query_posts_hash}&{urlencode(variables)}'
    #         yield response.follow(url_posts,
    #                               callback=self.user_data_parse,
    #                               cb_kwargs={'username': username,
    #                                          'user_id': user_id,
    #                                          'variables': deepcopy(variables)})
    #
    #     posts = j_data.get('data').get('user').get('edge_owner_to_timeline_media').get('edges')
    #     for post in posts:
    #         item = InstaparserItem(user_id=user_id,
    #                                username=username,
    #                                picture=post.get('node').get('display_url'),
    #                                likes=post.get('node').get('edge_media_preview_like').get('count'),
    #                                post_data=post.get('node'))
    #         yield item


    #Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')


    #Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')