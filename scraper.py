import os
import re


def find_Posts(
    page,
    browser,
    post_limit,
    upvote_threshold,
    comment_threshold,
    min_word_count,
    max_word_count,
):
    post_info = page.query_selector_all("shreddit-post")
    posts = []

    # Extract information from each post and add it to the list if it meets the requirements
    for post in post_info:
        if len(posts) >= post_limit:
            break

        title = post.get_attribute("post-title")
        url = "https://www.reddit.com" + post.get_attribute("permalink")
        upvotes = post.get_attribute("score")
        comment_count = post.get_attribute("comment-count")

        if int(upvotes) >= upvote_threshold and int(comment_count) >= comment_threshold:
            page = browser.new_page()
            page.goto(url)
            body = get_body(page)
            
            
            word_count = len(body.split())
            if min_word_count <= word_count <= max_word_count:
                take_screenshot(page, title)
                posts.append(
                    {
                        "title": title,
                        "url": url,
                        "upvotes": int(upvotes),
                        "comment_count": int(comment_count),
                        "body": body,
                        "word_count": word_count,
                        "character_count": len(body),
                    }
                )

            page.close()
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


def get_body(page):
    # Opens the post in a new page and return the body text
    
    page.wait_for_selector("shreddit-post-text-body")
    body = page.query_selector("shreddit-post-text-body")
    body_text = ""

    # Click read more to remove it from the screenshot and the body text
    read_more = page.query_selector('button[id$="-read-more-button"]')
    if read_more:
        read_more.click()

    if body:
        body_text = body.inner_text().replace("\n", " ").replace("  ", " ")

    return body_text


def take_screenshot(page, title):
    os.makedirs("screenshots", exist_ok=True)
    
    # Zoom in page to make the text larger
    page.evaluate("""
    () => {
        document.body.style.zoom = "150%"
    }
    """)

    page.query_selector("shreddit-post").screenshot(
        path=f"screenshots/{get_clean_title(title)}.png"
    )


def get_clean_title(title):
    # Remove special characters from the title
    title = re.sub(r"[\\/*?:\"\'<>|]", "", title)
    return title.replace(" ", "_")
