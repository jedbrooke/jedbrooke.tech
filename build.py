import yaml
import os
import bs4
import copy

ARTICLES_PATH = "articles"
HEADER_PATH = "subpage_head.html"


TAG_BADGE_CLASS = "badge bg-secondary text-decoration-none link-light"
MAIN_TEXT_CLASS = "fs-5 mb-4"
SUB_HEADER_CLASS = "fw-bolder mb-4 mt-5"

def local_image(data):
    tag = bs4.BeautifulSoup().new_tag("img")
    if 'alt' in data:
        tag['alt'] = data['alt']
    if 'src' in data:
        tag['src'] = f"/images/{data['src']}"
    return tag

def web_image(data):
    tag = bs4.BeautifulSoup().new_tag("img")
    if 'alt' in data:
        tag['alt'] = data['alt']
    if 'src' in data:
        tag['src'] = data['src']
    return tag

def text(data):
    tag = bs4.BeautifulSoup().new_tag("p")
    tag['class'] = MAIN_TEXT_CLASS
    tag.append(bs4.BeautifulSoup(data,"lxml"))
    return tag

def sub_header(data):
    tag = bs4.BeautifulSoup().new_tag("h2")
    tag['class'] = SUB_HEADER_CLASS
    tag.append(bs4.BeautifulSoup(data,"lxml"))
    return tag

ITEM_ACTIONS = {
    "local-image": local_image,
    "text": text,
    "web-image": web_image,
    "sub-header": sub_header,
}


def main():

    # generate sub_pages
    with open(HEADER_PATH) as fh:
        header_data = fh.read()
    page_template = bs4.BeautifulSoup(header_data,features="lxml")
    for path in os.listdir(ARTICLES_PATH):
        input_file = os.path.join(ARTICLES_PATH,path)
        output_file = os.path.join("public_html",path.replace(".yaml",".html"))
        if os.path.exists(output_file) and os.path.getmtime(output_file) >= os.path.getmtime(input_file):
            print("already generated, skipping")  
        else:
            with open(input_file) as article_yaml:
                data = yaml.safe_load(article_yaml)
                if 'draft' in data and data['draft'] == True:
                    print("draft, skipping")
                else:
                    html = copy.copy(page_template)
                    title_tag = page_template.new_tag("title")
                    title_tag.append(f"Jedbrooke - {data['title']}")
                    html.head.append(title_tag)
                    html.find(id="main-title").append(data['title'])
                    html.find(id="date").append(data['date'])

                    article_header = html.find(id="article-header")
                    for tag in data['tags']:
                        badge = page_template.new_tag("a")
                        badge.append(tag)
                        badge['class'] = TAG_BADGE_CLASS
                        badge['href'] = f"tags.html#{tag}"
                        article_header.append(badge)
                    article_content = html.find(id="article-content")
                    for item in data['body']:
                        for k,v in item.items():
                            article_content.append(ITEM_ACTIONS[k](v))
                    
                    with open(output_file,"w") as ofh:
                        ofh.write(html.prettify())
        print("------")


if __name__ == '__main__':
    main()


