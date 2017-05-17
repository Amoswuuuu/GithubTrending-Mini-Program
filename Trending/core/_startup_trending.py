import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import web
import json
from time import time
import requests
import common,logging,datetime,os,trending_html_parse
import util
import github_token
import hashlib,urllib
CODEHUB_API = 'http://trending.codehub-app.com/v2/trending?since=%s'
CODEHUB_API_LAN = 'http://trending.codehub-app.com/v2/trending?since=%s&language=%s'
CODEHUB_API_LANGUAGES = 'http://trending.codehub-app.com/v2/languages'
SEARCH_API = 'https://api.github.com/search/repositories?q=%s&sort=stars&order=desc'
urls = (
    '/all/','AllLang',
    '/capture/(.*)','Capture',
    '/v1/trending','Trending',
    '/v1/languages','Languages',
    '/v1/repos','Repos',
    '/v1/repos/search','ReposSearch'
)
app = web.application(urls,globals())
dirs = 'CodeJsonData'
header={
    'Authorization':' token '+github_token.token
}
class ReposSearch:
    def GET(self):
        print web.input()
        params = util.getInput(web.input())
        q = params['q']
        q = urllib.quote(q)
        print q
        api = SEARCH_API % q
        print api,header
        r = requests.get(api, verify=False,headers=header)
        return r.text
class Trending:
    def GET(self):
        if not os.path.exists(dirs):
            os.mkdir(dirs)
        
        print web.input()
        params = util.getInput(web.input())
        print params
        since = params['since']
        language = params.get('language')
        print language
        if not language == None:
            filename = _get_time() + since + language + '.json'
        else:
            filename = _get_time() + since + '.json'
        if os.path.exists(dirs + '/' + filename):
            with open(dirs + '/' + filename,'r') as f:
                content = f.readline()
            if not content == '':
                return content
        if not language == None:
            trending_api = CODEHUB_API_LAN % (since,language)           
        else:
            trending_api = CODEHUB_API % since           
        _trending_json = requests.get(trending_api)
        with open('CodeJsonData/' + filename,'w') as f:
            f.write(_trending_json.text.encode('utf-8'))
        return _trending_json.text
class Languages:
    def GET(self):
        _lans_json = requests.get(CODEHUB_API_LANGUAGES,headers=header)
        return _lans_json.text
class Repos:
    def GET(self):
        params = util.getInput(web.input())
        github_url = params['github']
        m2 = hashlib.md5()   
        m2.update(github_url)   
        url_md5 =  m2.hexdigest()   
        if os.path.exists(dirs + '/' + _get_time() + url_md5):
            with open(dirs + '/' + _get_time() + url_md5,'r') as f:
                c = f.readline()
            if not c == None:
                return c
        _json = requests.get(github_url,verify=False,headers=header)
        with open(dirs + '/' + _get_time() + url_md5,'w') as f:
            f.write(_json.text.encode('utf-8'))
        return _json.text

class Capture:
    def GET(self,rep):
            capture_png = rep.split('/')[-1] + '.png'
            print capture_png   
            png_path = common.PIC + '/' + capture_png
            # webp_path = common.WEBP +'/' + capture_png + '.webp'
            if not os.path.exists(png_path):
                png_path = trending_html_parse.capture(common.API.replace('trending',rep),png_path)
            # if not os.path.exists(webp_path):
            #     webp_path = trending_html_parse.convert_webp(png_path)
            return png_path
class AllLang:
    def GET(self):
            logging.warning("======= GET STARTED =======")
            filePath = _get_time() + 'all.json'
            if os.path.exists(filePath):
                f = open(filePath,'r')
                s = f.readline()
                f.close()
                return s
            # self.path = '/index.html'
            # SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
            else:
                s = requests.get(common.API)
                t = trending_html_parse.TrendingHtmlParser(s.text.encode('utf-8'))
                _json = t._get_json()
                # self.wfile.write(json.dumps(_json))
                f = open(filePath,'w')
                f.write(json.dumps(_json))
                f.close()
                return json.dumps(_json)
def _get_time():
        return datetime.datetime.now().strftime('%Y-%m-%d')

if __name__ == '__main__':
    app.run()