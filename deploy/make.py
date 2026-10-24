#! /usr/bin/env python3

import csv
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
from bs4 import BeautifulSoup

##
# Author: Chris Eldon
# Email: mail@chriseldon.com
# Description: This script is used to build some of the various included files that are needed to build a successful website. This is heavily custom and based on how I designed my website (which is very minimal). YMMV if you use this on your own.
# Last Updated: 10/20/2026
# License: MIT License
## 

DEPLOY_BASE_PATH = "deploy"
TEMPLATE_BASE_PATH = "templates"
SITE_BASE_PATH = "_site"


def read_posts(file_path):
    '''
    Reads a supplied CSV file and returns a dictionary of the posts with their relevant details.
    '''

    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        posts = []

        for row in reader:
            item = {
                'post_date': row['post_date'].strip(),
                'post_year': row['post_date'].strip().split('-')[0],
                'post_month': row['post_date'].strip().split('-')[1],
                'post_day': row['post_date'].strip().split('-')[2],
                'post_slug': row['post_title'].strip().lower().replace(' ', '-'),
                'post_name': row['post_name'].strip()
            }
            posts.append(item)

    return posts


def build_bloglist(posts, output_path, max_posts=None):
    '''
    Builds the blog list HTML file based on the provided posts and template.
    '''

    bloglist_html = '<ul>\n'

    posts_to_include = posts[:max_posts] if max_posts is not None else posts
    posts_newest_first = reversed(posts)
    posts_to_include = list(posts_newest_first)
    if max_posts is not None:
        posts_to_include = posts_to_include[:max_posts]

    for post in posts_to_include:
        post_html = f'    <li>\n'
        post_html += f'        <i><span><time datetime="{post["post_date"]}" pubdate>{post["post_date"]}</time></span></i>\n'
        post_html += f'        <a href="https://www.chriseldon.com/blog/{post["post_year"]}/{post["post_month"]}/{post["post_slug"]}.html">{post["post_name"]}</a>\n'
        post_html += f'    </li>\n'
        bloglist_html += post_html

    bloglist_html += '</ul>'

    # Write the generated HTML to the output file
    with open(output_path, 'w') as output_file:
        output_file.write(bloglist_html)


def adjust_footer_date():
    '''
    Adjusts the footer.html file to include the current date in the appropriate format.
    '''

    with open(f"{TEMPLATE_BASE_PATH}/footer.html", 'r') as footer_file:
        footer_content = footer_file.read()

    current_date = datetime.now().strftime("%Y-%m-%d")
    current_date_long = datetime.now().strftime("%b %d, %Y")

    footer_content = footer_content.replace("%%CUR_DATE%%", current_date).replace("%%CUR_DATE_LONG%%", current_date_long)

    with open(f"{SITE_BASE_PATH}/includes/footer.html", 'w') as footer_file:
        footer_file.write(footer_content)


def generate_rss_feed(posts, output_path):
    '''
    Generates an RSS feed XML file based on the provided posts.
    '''

    rss_feed = '<?xml version="1.0" encoding="UTF-8" ?>\n'
    rss_feed += '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
    rss_feed += '  <channel>\n'
    rss_feed += '    <title>Random Musings</title>\n'
    rss_feed += '    <link>https://www.chriseldon.com/</link>\n'
    rss_feed += '    <description>Blog content on www.chriseldon.com</description>\n'
    rss_feed += '    <language>en-us</language>\n'
    rss_feed += '    <webMaster>mail@chriseldon.com (Chris Eldon)</webMaster>\n'
    rss_feed += '    <atom:link href="https://www.chriseldon.com/rss.xml" rel="self" type="application/rss+xml"/>\n'

    for post in posts:
        with open(f"{SITE_BASE_PATH}/blog/{post['post_year']}/{post['post_month']}/{post['post_slug']}.html", 'r') as post_file:
            post_content = post_file.read()

        soup = BeautifulSoup(post_content, 'html.parser')
        main_element = soup.find('main')
        main_html = main_element.decode_contents() if main_element else ''

        pub_date = datetime.strptime(post["post_date"], "%Y-%m-%d").replace(tzinfo=timezone(timedelta(hours=-4)))

        rss_feed += '    <item>\n'
        rss_feed += f'      <title>{post["post_name"]}</title>\n'
        rss_feed += f'      <link>https://www.chriseldon.com/blog/{post["post_year"]}/{post["post_month"]}/{post["post_slug"]}.html</link>\n'
        rss_feed += f'      <pubDate>{format_datetime(pub_date)}</pubDate>\n'
        rss_feed += f'      <author>mail@chriseldon.com (Chris Eldon)</author>\n'
        rss_feed += f'      <guid>https://www.chriseldon.com/blog/{post["post_year"]}/{post["post_month"]}/{post["post_slug"]}.html</guid>\n'
        rss_feed += f'      <description><![CDATA[{main_html}<p>Thanks for reading this post through an RSS reader and keeping the small web alive!</p>]]></description>\n'
        rss_feed += '    </item>\n'

    rss_feed += '  </channel>\n'
    rss_feed += '</rss>'

    # Write the generated RSS feed to the output file
    with open(output_path, 'w') as output_file:
        output_file.write(rss_feed)


def main():
    print("Building website files...")
    # Read the list of posts from the CSV file and build the blog list files
    # The first bloglist.html is the latest 10 posts
    # The second bloglistfull.html is *every* post
    posts = read_posts(f"{DEPLOY_BASE_PATH}/blog_posts.csv")
    build_bloglist(posts, f"{SITE_BASE_PATH}/includes/bloglist.html", 10)
    build_bloglist(posts, f"{SITE_BASE_PATH}/includes/bloglistfull.html")
    adjust_footer_date()

    # Generate RSS Feed
    print("Generating RSS feed...")
    generate_rss_feed(posts, f"{SITE_BASE_PATH}/rss.xml")

    print("Website files built successfully.")


if __name__ == "__main__":
    main()