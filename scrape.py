from bs4 import BeautifulSoup as bsoup
import requests
import re
import argparse

class MannKiBaat:
    HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        }
    pages_url ='https://www.pmindia.gov.in/wp-admin/admin-ajax.php?action=demoMannKiBaat&page_no={no}&language={lang}&tag=mann-ki-baat'

    def get_html(self,url):
        r = requests.get(url, headers=self.HEADERS, timeout=60)
        return r.content

    def gsoup(self,url):    
        return bsoup(self.get_html(url), 'html.parser')
    
    def print_result(self, para_txt, regexp, add_href):
        for sent_txt in para_txt.split("."):
            if regexp.search(sent_txt):
                print("\nText = ", sent_txt)
                print("\nMatches = ", regexp.findall(sent_txt))
                print("\nLink = ", add_href)
    
    def get_word(self, urlno, regexp, lang="en"):
        pages_soup1 = self.gsoup(self.pages_url.format(no=urlno, lang=lang))
        for add in pages_soup1.find_all("a", href = re.compile(r'pms-address-in-')):
            add_href = add["href"]
            add_soup = self.gsoup(add_href)
            for para in (add_soup.find_all("p")):
                self.print_result(para.text, regexp, add_href)
                

    def loop_list_urls(self, search_str, lang="en"):
        for urlno in range(1,100):
            self.get_word(urlno, search_str, lang)

def _main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-s', '--search_str', metavar='s', type=str,
                        help='the search string')
    parser.add_argument('-l', '--lang', metavar='l', nargs='?', default="en", type=str,
                        help='the search language')
    args = parser.parse_args()
    if args.search_str is None:
        parser.error("Search string is empty")
    if args.lang not in ['en', 'hi']:
        parser.error("either en or hi for language")
    m = MannKiBaat()
    try:
        m.loop_list_urls(re.compile(args.search_str), lang=args.lang)
    except KeyboardInterrupt:
        print("Ctrl+c pressed!")

if __name__ == '__main__':
    _main()