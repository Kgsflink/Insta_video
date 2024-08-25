import instaloader
import os

# Function to download Instagram Shorts video
def download_instagram_shorts_video(url):
    # Create an instance of Instaloader
    loader = instaloader.Instaloader()

    try:
        # Extract the shortcode from the Instagram URL
        if "/p/" in url:
            # For posts
            shortcode = url.split("/p/")[1].split("/")[0]
        elif "/reel/" in url:
            # For reels
            shortcode = url.split("/reel/")[1].split("/")[0]
        else:
            raise ValueError("Invalid Instagram URL")

        # Load the post metadata
        post = instaloader.Post.from_shortcode(loader.context, shortcode)

        # Create a folder named "insta" if it doesn't exist in the current directory
        save_path = "/sdcard/insta"
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # Download the video to the specified path
        loader.download_post(post, target=os.path.join(save_path, shortcode))
        print("\033[32mVideo downloaded successfully.\033[0m")  # Green color for success message

    except ValueError as ve:
        print(f"\033[31mInvalid Instagram URL. Error: {str(ve)}\033[0m")  # Red color for error
    except instaloader.exceptions.InstaloaderException as e:
        print(f"\033[31mFailed to download video. Error: {str(e)}\033[0m")  # Red color for error

# Function to download from a single link
def download_from_link():
    # Ask for the Instagram share link
    instagram_url = input("\033[31mEnter the Instagram share link: \033[0m")  # Red color for prompt

    # Download the Instagram Shorts video
    download_instagram_shorts_video(instagram_url)

# Function to download from a file containing links
def download_from_file():
    # Ask for the file path
    file_path = input("\033[31mEnter the path of the file containing the links: \033[0m")  # Red color for prompt

    try:
        with open(file_path, 'r') as file:
            # Read the file and process each link
            for line in file:
                link = line.strip()
                download_instagram_shorts_video(link)
                print("\033[32m")  # Green color for success message

    except FileNotFoundError:
        print(f"\033[31mFile not found: {file_path}\033[0m")  # Red color for error

# Ask whether to download from a link or a file
choice = input("\033[31mDo you want to download a video from a link (L) or from a file (F)? \033[0m").upper()  # Red color for prompt

if choice == 'L':
    download_from_link()
elif choice == 'F':
    download_from_file()
else:
    print("\033[31mInvalid choice.\033[0m")  # Red color for error
