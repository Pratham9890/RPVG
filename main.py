from playwright.sync_api import sync_playwright, Playwright
import scraper, tts, os, video_generator, subtitles


def main():

    posts = []
    with sync_playwright() as playwright:
        # Limit the number of post to create video for
        num_posts = 1
        # Set requirements for the posts
        upvote_threshold = 100
        comment_threshold = 10
        min_word_count = 200
        max_word_count = 280
        # Set the subreddit to scrape
        subreddit = "pettyrevenge"

        # Run the scraper and get the posts
        posts = run(
            playwright,
            num_posts,
            upvote_threshold,
            comment_threshold,
            min_word_count,
            max_word_count,
            subreddit,
        )

    if not posts:
        print("No posts found that meet the criteria.")
        return

    # Loops over all posts
    for post in posts:
        clean_title = scraper.get_clean_title(post["title"])
        # Save audio
        save_audio(post)
        # Generate video with background, post image, and audio
        video_generator.generate_video(
            back_img="videos/background.mp4",
            post_img=f"screenshots/{clean_title}.png",
            audio_file=f"audios/{clean_title}.mp3",
            out_file=f"output/{clean_title}.mp4",
        )

        # Generating subtitles
        subtitles.generate_subtitles(f"audios/{clean_title}.mp3", clean_title)
        # Burn subtitles into the video
        subtitles.burn_subtitles(
            video_file=f"output/{clean_title}.mp4",
            subtitle_file=f"subtitles/{clean_title}.ass",
            output_file=f"output/{clean_title}_subtitled.mp4",
        )


def run(
    playwright: Playwright,
    num_posts: int,
    upvote_threshold: int = 0,
    comment_threshold: int = 0,
    min_word_count: int = 0,
    max_word_count: int = 1000,
    subreddit: str = "pettyrevenge",
):
    # Creates a browser and goes to the subreddit page
    chromium = playwright.chromium
    browser = playwright.chromium.launch_persistent_context(
        user_data_dir="./reddit_profile",
        headless=False,
        channel="chrome",
        viewport={"width": 600, "height": 4000},
    )
    page = browser.new_page()
    page.goto(f"https://www.reddit.com/r/{subreddit}/rising/")

    # Extract the posts
    posts = scraper.find_Posts(
        page,
        browser,
        num_posts,
        upvote_threshold,
        comment_threshold,
        min_word_count,
        max_word_count,
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
