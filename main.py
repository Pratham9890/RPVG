from playwright.sync_api import sync_playwright, Playwright
import scraper, tts, os, video_generator


def main():

    posts = []
    with sync_playwright() as playwright:
        num_posts = 2
        upvote_threshold = 500
        comment_threshold = 100

        # Run the scraper and get the posts
        posts = run(playwright, num_posts, upvote_threshold, comment_threshold)

    # Generate the audio for each post
    for post in posts:
        clean_title = scraper.get_clean_title(post["title"])
        save_audio(post)
        video_generator.generate_video(
            back_img="videos/background.mp4",
            post_img=f"screenshots/{clean_title}.png",
            audio_file=f"audios/{clean_title}.mp3",
            out_file=f"output/{clean_title}.mp4",
        )


def run(
    playwright: Playwright,
    num_posts: int,
    upvote_threshold: int = 0,
    comment_threshold: int = 0,
):
    # Creates a browser and goes to the subreddit page
    chromium = playwright.chromium
    browser = chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.reddit.com/r/pettyrevenge/rising/")

    # Extract the posts
    posts = scraper.find_Posts(
        page, browser, num_posts, upvote_threshold, comment_threshold
    )

    scraper.print_Posts(posts)

    browser.close()

    return posts


def save_audio(post):
    print("Generating audio for post:", post["title"])
    filename = scraper.get_clean_title(post["title"])
    # Generate the audio file with title as the filename
    os.makedirs("audios", exist_ok=True)
    tts.generate_audio(post["body"], f"audios/{filename}.mp3")


if __name__ == "__main__":
    main()
