from bs4.element import Tag
import yaml
import os
import bs4
import copy

ARTICLES_PATH = "articles"
HEADER_PATH = "subpage_head.html"

def main():
    with open(HEADER_PATH) as fh:
        header_data = fh.read()
    page_template = bs4.BeautifulSoup(header_data,features="lxml")
    for path in os.listdir(ARTICLES_PATH):
        with open(os.path.join(ARTICLES_PATH,path)) as article_yaml:
            data = yaml.safe_load(article_yaml)
            print(data)
            html = copy.copy(page_template)
            title_tag = page_template.new_tag("title")
            title_tag.append(f"Jedbrooke - {data['title']}")
            html.head.append(title_tag)
            print(html.prettify())
        print("------")


if __name__ == '__main__':
    main()


