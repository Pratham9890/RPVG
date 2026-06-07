from playwright.sync_api import sync_playwright, Playwright


def main():

    with sync_playwright() as playwright:
        run(playwright)


def run(playwright: Playwright):
    chromium = playwright.chromium  # or "firefox" or "webkit".
    browser = chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.reddit.com/r/AmItheAsshole/rising/")
    print("Page title", page.title())

    # Get the posts and print them
    posts = findPosts(page)
    printPosts(posts)

    # For debugging
    input("Press Enter to close the browser...")
    browser.close()


def findPosts(page):
    post_info = page.query_selector_all("shreddit-post")
    posts = []

    # Loop through each post and extract the information
    for post in post_info:
        title = post.get_attribute("post-title")
        url = "https://www.reddit.com" + post.get_attribute("permalink")
        upvotes = post.get_attribute("score")
        comment_count = post.get_attribute("comment-count")

        posts.append(
            {
                "title": title,
                "url": url,
                "upvotes": upvotes,
                "comment_count": comment_count,
            }
        )
    return posts


def printPosts(posts):
    for post in posts:
        print("Title:", post["title"])
        print("URL:", post["url"])
        print("Upvotes:", post["upvotes"])
        print("Number of Comments:", post["comment_count"])


if __name__ == "__main__":
    main()
