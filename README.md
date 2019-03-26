# PSIAP-DL-Youtube-CC

This python script downloads all Creative Commons licensed videos for a given YouTube channel. Downloads are saved to `FILEPATH/{video_id}.{ext}`, where `{video_id}` is the YouTube id of the video, and `{ext}` is the filetype extension. The metadata is also stored in `FILEPATH/{video_id}.info.json` as a JSON file. An additional utility file at `FILEPATH/dl_status` keeps track of the download status, and an informational file about the channel is stored at `FILEPATH/channel_summary.json`

## Usage
```
usage: python get_vids.py [-h] -c CHANNELID [-f FILEPATH] [-w] [-a]

optional arguments:
  -h, --help            show this help message and exit
  -c CHANNELID, --channelid CHANNELID
                        id for the channel of the form
                        https://www.youtube.com/channel/{channel_id}
  -f FILEPATH, --filepath FILEPATH
                        file path where the downloaded videos should be
                        downloaded. Defaults to local directory
  -w, --overwrite       if specified, will overwrite existing videos with the
                        same name when downloading. By default, it will skip
                        over existing files
  -a, --getaudio        if specified, will also try to get audio file
                        (separately)
  -v, --verbose         print extra details
  -d, --dry-run         don't download files, only print information about
                        channel and videos
```

## Requirements
### Python packages
Python requirements listed in `environment.yml` conda environment file. Requires [conda](https://conda.io/en/master/). Create an environment with the required packages using:
```
conda env create -f environment.yml
```  
Important packages:  
* [youtube-dl](https://github.com/rg3/youtube-dl) is used for downloading the videos  
* [google-api-python-client](https://github.com/googleapis/google-api-python-client) is used for authentication and youtube API requests  

### YouTube API Key
In order to use the YouTube API, the user must register an API key with Google. See [this tutorial](https://developers.google.com/youtube/v3/quickstart/python) for instructions on how to get an API key. Users should replace the `client_secret.json_demo` with their respective `client_secret.json`. 

The first time the script is run on a machine, it will prompt for user authentication via a URL. Users should copy the URL into a browser, and authenticate using their Google/Youtube credentials. An access token will be stored in the `tokens/credentials.json` file, which should automatically be used for future runs.

The `client_secret.json` and `credentials.json` files should be kept secret.

### Additional Requirements

[ffmpeg](https://www.ffmpeg.org/) or a similar tool is necessary to combine audio and high resolution videos. By default, YouTube stores high resolution (1080p+) videos separately from audio files. If available, we download the best video and audio files separately. They can then be combined by the user as needed using a tool such as ffmpeg.

Some media may require [VLC](https://github.com/videolan/vlc) or similar software for playing different formats. 

## Motivation
This software, funded by PSIAP 2017, supports the development of datasets representative of public safety operations, whose need was formally identified in [NIST TN 1917: Public Safety Analytics R&D Roadmap](https://www.nist.gov/publications/public-safety-analytics-rd-roadmap):

> One of the most fundamental barriers to seamless data integration is simply a lack of awareness or access to datasets that are accurate, current, and relevant to improving response.

This effort is motivated by the increasing importance of video and imagery for public safety operations. The goal is to accelerate technology innovation for network providers, application providers, and public safety agencies. Videos with a Creative Commons (CC) license are routinely uploaded to YouTube. As part of the PSIAP dataset effort, we identified specific YouTube channels with representative public safety content. YouTube channels operate independently on the PSIAP effort and will continue to collect and post videos beyond the PSIAP effort. This results in an ever growing dataset. This growth is a realization discussed in [NISTIR 8164: First Workshop on Video Analytics in Public Safety](https://www.nist.gov/publications/first-workshop-video-analytics-public-safety):

> **Thoughts on future development:** Increasingly, software developers will need to take advantage of new hardware innovations. With the increasing reliance on machine learning methods such as deep learning, developers will require access to ever-increasing quantities of data for both training and evaluation purposes. Going beyond static datasets (which can be overlearned), future algorithms will require constant novelty allowing for a state of never-ending unsupervised learning. This will require a migration from data-sets to data-sites and, perhaps, data-cities.

## Example Creative Commons Videos
[![Working Vehicle Fire on Garden State Parkway NJ - Helmet Cam](https://img.youtube.com/vi/4pd1oEmsJiI/mqdefault.jpg)](https://youtu.be/4pd1oEmsJiI?t=234 "Working Vehicle Fire on Garden State Parkway NJ - Helmet Cam")
[![Sleeping to the GATES OF HELL in 6 minutes!! (Helmet Cam)](https://img.youtube.com/vi/VbHaJbJ4_Ao/mqdefault.jpg)](https://youtu.be/VbHaJbJ4_Ao?t=58 "Sleeping to the GATES OF HELL in 6 minutes!! (Helmet Cam)")

[![65. Callout - Storm Desmond - Cumbria Floods 5th Dec 2015](https://img.youtube.com/vi/TxniKN7jL8U/mqdefault.jpg)](https://youtu.be/TxniKN7jL8U?t=193 "T65. Callout - Storm Desmond - Cumbria Floods 5th Dec 2015")
[![Navy Helo Crew Rescues Texans](https://img.youtube.com/vi/GoST8oc_6Zs/mqdefault.jpg)](https://youtu.be/GoST8oc_6Zs?t=152 "Navy Helo Crew Rescues Texans")

[![Body-worn camera video: Officers assist man in crisis, detain and release bystander](https://img.youtube.com/vi/Pa2g4NRl97g/mqdefault.jpg)](https://youtu.be/Pa2g4NRl97g?t=1946 "Body-worn camera video: Officers assist man in crisis, detain and release bystander")
[![Toyota Land Cruiser VII | 4K POV Test Drive #155 Joe Black](https://img.youtube.com/vi/2LsswJ7665w/mqdefault.jpg)](https://youtu.be/2LsswJ7665w?t=230 "Toyota Land Cruiser VII | 4K POV Test Drive #155 Joe Black")

## Useful Links
* [Creative Commons](https://creativecommons.org/)  
* [Creative Commons - YouTube Help](https://support.google.com/youtube/answer/2797468) 
* [Public Safety Innovation Accelerator Program 2017](https://www.nist.gov/ctl/pscr/funding-opportunities/past-funding-opportunities/psiap-2017)  
* [ResearchGate - NIST PSIAP: Representative Public Safety Video Dataset](https://www.researchgate.net/project/NIST-PSIAP-Representative-Public-Safety-Video-Dataset)  
* [New Jersey Office of Homeland Security and Preparedness](https://www.njhomelandsecurity.gov/home/)
* [MIT Lincoln Laboratory - Humanitarian Assistance and Disaster Relief Systems](https://www.ll.mit.edu/r-d/homeland-protection/humanitarian-assistance-and-disaster-relief-systems)  

## Authors
* Jeffrey Liu (MITLL)  
* Andrew Weinert  (MITLL)    

## Acknowledgments
* Gabriela Barrera (MITLL)
* Dieter Schuldt (MITLL)  
* Steven Talpas (NJOHSP)  
* William Drew (NJOHSP)  

## Disclaimer
This work was performed under the following financial assistance award 70NANB17Hl69 from U.S. Department of Commerce, National Institute of Standards and Technology.
