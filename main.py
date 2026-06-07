from playwright.sync_api import sync_playwright, Playwright
import scraper, tts, asyncio




def main():

    with sync_playwright() as playwright:
        num_posts = 100;
        upvote_threshold = 500
        comment_threshold = 100
        
        # Run the scraper and get the posts
        posts = run(playwright, num_posts, upvote_threshold, comment_threshold)
        
        for post in posts:
            print("Generating audio for post:", post["title"])
            # place the files inside a folder called "audio" and replace spaces in the title with underscores
            asyncio.run(tts.generate_audio(post["body"].replace('AITA', 'Am I the Asshole'), f"output/{post['title'].replace(' ', '_')}.mp3"))




def run(playwright: Playwright, num_posts: int, upvote_threshold: int = 0, comment_threshold: int = 0):
    # Creats a browser and goes to the subreddit page
    chromium = playwright.chromium  # or "firefox" or "webkit".
    browser = chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.reddit.com/r/AmItheAsshole/rising/")

    # Extract the posts
    posts = scraper.find_Posts(page, browser, num_posts, upvote_threshold, comment_threshold)


    # Print the posts
    scraper.print_Posts(posts)

    # To keep the browser open
    # input("Press Enter to close the browser...")
    browser.close()

    return posts




if __name__ == "__main__":
    main()
