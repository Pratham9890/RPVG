from playwright.sync_api import sync_playwright, Playwright
import scraper




def main():

    with sync_playwright() as playwright:
        num_posts = 100;
        upvote_threshold = 500
        comment_threshold = 100
        run(playwright, num_posts, upvote_threshold, comment_threshold)




def run(playwright: Playwright, num_posts, upvote_threshold=0, comment_threshold=0):
    # Creats a browser and goes to the subreddit page
    chromium = playwright.chromium  # or "firefox" or "webkit".
    browser = chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.reddit.com/r/AmItheAsshole/rising/")

    # Extract the posts
    posts = scraper.find_Posts(page, browser, num_posts, upvote_threshold, comment_threshold)


    # Print the posts
    scraper.print_Posts(posts)

    # For debugging
    # input("Press Enter to close the browser...")
    browser.close()




if __name__ == "__main__":
    main()
