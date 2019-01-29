# wall_hook

This program fetches the latest post from the subreddit earthporn, downloads the image in the post. 
Performs a resolution scale down to match my monitor and calls the kde module via qbus to replace the wallpaper.

## Steps to install

git clone this repository and add a cron job to start brain.py


## Things to do:
Provide support for additional subreddits
Replace hardcoded resolutions to generic file configurable values
Download additional image incase the latest one is of a lesser resoultion
Should make sure the process runs after the system connects to the internet
