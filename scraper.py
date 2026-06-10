import os
import re


def find_Posts(page, browser, num_posts, upvote_threshold, comment_threshold):
    post_info = page.query_selector_all("shreddit-post")
    posts = []

    # Loop through each post and extract the information
    for post in post_info[:num_posts]:
        title = post.get_attribute("post-title")
        url = "https://www.reddit.com" + post.get_attribute("permalink")
        upvotes = post.get_attribute("score")
        comment_count = post.get_attribute("comment-count")
        

        # Only get the body and add the post to the list if it meets the requirements
        if int(upvotes) >= upvote_threshold and int(comment_count) >= comment_threshold:
            body = get_body(url, browser, title)

            posts.append(
                {
                    "title": title,
                    "url": url,
                    "upvotes": int(upvotes),
                    "comment_count": int(comment_count),
                    "body": body,
                    "word_count": len(body.split()),
                    "character_count": len(body)
                }
            )
    return posts


def print_Posts(posts):
    for post in posts:
        print("Title:", post["title"])
        print("URL:", post["url"])
        print("Upvotes:", post["upvotes"])
        print("Number of Comments:", post["comment_count"])
        print("Body:", post["body"])
        print("Word Count:", post["word_count"])
        print("Character Count:", post["character_count"])
        print("\n")


def get_body(url, browser, title):
    # Opens the post in a new page and return the body text
    page = browser.new_page(viewport={"width": 1280, "height": 4000})
    page.goto(url)
    page.wait_for_selector("shreddit-post-text-body")
    body = page.query_selector("shreddit-post-text-body")
    body_text = ""

    os.makedirs("screenshots", exist_ok=True)
    page.query_selector("shreddit-post").screenshot(path=f"screenshots/{get_clean_title(title)}.png")

    if body:
        body_text = body.inner_text().replace("\n", " ").replace("  ", " ")
    
    page.close()
    return body_text


def get_clean_title(title):
    # imrpove the line below and use just one sub
    title = re.sub(r'[\\/*?:"<>|]', "", title)
    return title.replace(" ", "_")