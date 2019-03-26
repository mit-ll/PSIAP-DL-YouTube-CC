# Adapted from the quickstart example at https://developers.google.com/youtube/v3/quickstart/python
import os
import json
import argparse
import google.oauth2.credentials
import youtube_dl
import isodate
import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

# Set up argument parsing
parser = argparse.ArgumentParser(description='Download all CC-licensed videos for a given channel')
parser.add_argument('-c','--channelid', type=str, required=True,
        help='id for the channel of the form https://www.youtube.com/channel/{channel_id}',
        dest='channelid')
parser.add_argument('-f','--filepath', type=str,
        help='file path where the downloaded videos should be downloaded. Defaults to local directory',
        default='./', dest='filepath')
parser.add_argument('-w','--overwrite', action='store_true',
        help='if specified, will overwrite existing videos with the same name when downloading. By default, it will skip over existing files',
        dest='overwrite')
parser.add_argument('-a','--getaudio', action='store_true',
        help='if specified, will also try to get audio file (separately)',
        dest='audio')
parser.add_argument('-v','--verbose', action='store_true', help="print extra details", dest='verbose')
parser.add_argument('-d','--dry-run', action='store_true', help="don't download files, only print information about channel and videos", dest='dry')

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. Requires an application to be registered with the Youtube Data API: https://developers.google.com/youtube/v3/quickstart/python
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

class VideoResults:
    """
    Iterator class to return the results of the video search query
    Each iteration returns a dict corresponding to a page of results see: https://developers.google.com/resources/api-libraries/documentation/youtube/v3/python/latest/youtube_v3.search.html
    Stops iterating when no more result pages are available

    Usage: v = VideoResults(service, request)
    args:
        service     Output of get_authenticated_service()
        request     A search request of the type service.list()
    """
    requests = None
    results = None
    service = None
    def __init__(self, service, request):
        self.service = service
        self.request = request

    def __iter__(self):
        return self

    def __next__(self):
        try:
            self.results = self.request.execute()
            self.request = service.search().list_next(self.request, self.results)
            if self.results:
                return self.results
        except:
            raise StopIteration


def get_authenticated_service():
    """
    Performs authentication by providing the client_secret.json API information, prompts user to authenticate via their Google account
    """
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    try:
        credentials = Credentials.from_authorized_user_file('tokens/credentials.json', scopes=SCOPES)
    except:
        credentials = flow.run_console()
    credentials_dict = {
	    'token': credentials.token,
	    'refresh_token': credentials.refresh_token,
	    'id_token': credentials.id_token,
	    'token_uri': credentials.token_uri,
	    'client_id': credentials.client_id,
	    'client_secret': credentials.client_secret
    }
    with open('tokens/credentials.json', 'w') as cred_file:
        json.dump(credentials_dict, cred_file)
    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def get_video_ids(service, channel_id):
    """
    Gets the ids of all creative commons licensed videos of a given channel
    args:
        service         Output of get_authenticated_service()
        channel_id      String of channel id
    returns:
        VideoResults    Iterable of results
    """
    request = service.search().list(part='id',
                channelId=channel_id,
                type='video',
                videoLicense='creativeCommon')
    vid_results = VideoResults(service, request)
    return vid_results

def format_timedelta(timedelta):
    """
    convenience function to convert timedelta object into %HH%MM%SS string, since strftime isn't defined for timedelta objects
    """
    seconds = timedelta.seconds % 60
    minutes = (timedelta.seconds % 3600) // 60
    hours = timedelta.days*24 + timedelta.seconds // 3600
    if hours > 0:
        return '{} Hours, {} Minutes, {} Seconds'.format(hours, minutes, seconds)
    elif minutes > 0:
        return '{} Minutes, {} Seconds'.format(minutes, seconds)
    else:
        return '{} Seconds'.format(seconds)


if __name__ == '__main__':
    # Parse arguments
    args = vars(parser.parse_args())
    write_path = args['filepath']
    if not os.path.exists(write_path):
        os.makedirs(write_path)
    channel_id = args['channelid']
    overwrite = args['overwrite'] # whether to overwrite existing files
    if overwrite:
        no_ow = False
    else:
        no_ow = True
    audio = args['audio'] # whether to try and download audio
    if audio:
        dl_fmt = 'bestvideo,bestaudio/best' # try and get best video and audio, otherwise, best stream with both
    else:
        dl_fmt = 'bestvideo/best' # try only to get best video stream, fallback to best both if no video-only file
    # Set options for youtube_dl
    ydl_opts = {
            'format': dl_fmt, # what format video should we get
            'outtmpl': '{path}%(id)s.%(ext)s'.format(path=write_path), # write to write_path, using the video id as filename
            'retries': 10, # number of times to retry if connection errors
            'writeinfojson': True # save metadata to vid_id.info.json
            }
    if overwrite:
        ydl_opts['nooverwrites'] = False
    else:
        ydl_opts['nooverwrites'] = True
        ydl_opts['download_archive'] = os.path.join(write_path, 'dl_status') # stores progress in an archive file
    if args['dry']:
        ydl_opts['skip_download'] = True # don't actually download if --dry-run is given
    # Authenticate with the API
    service = get_authenticated_service()
    # build dictionary to hold channel summary information
    summary = {'channel_name':None, 'channel_id':channel_id,
            'num_cc_vids':0, 'total_duration':datetime.timedelta(0), 'min_duration':datetime.timedelta(0),
            'max_duration':datetime.timedelta(0)}
    # Request channel information from youtube channels api
    channel_info = service.channels().list(part='snippet', id=channel_id).execute()['items'][0]
    summary['channel_name'] = channel_info['snippet']['title']
    # Search for videos for given channel
    vid_res = get_video_ids(service, channel_id)
    for res_page in vid_res: # iterate over response pages
        for response in res_page['items']: # iterate over items on page
            vid_id = response['id']['videoId'] # get the id string of vid
            # increment the counter for number of cc videos found
            summary['num_cc_vids'] = summary['num_cc_vids'] + 1
            # get video details
            vid_details = service.videos().list(part='snippet,contentDetails', id=vid_id).execute()['items'][0]
            if args['dry'] or args['verbose']:
                print(vid_details)
            # get duration of video for summary
            content_duration = isodate.parse_duration(vid_details['contentDetails']['duration'])
            summary['total_duration'] = summary['total_duration'] + content_duration # add duration to total
            if ((summary['min_duration'] == datetime.timedelta(0)) and (content_duration > datetime.timedelta(0)))\
                    or (content_duration < summary['min_duration']):
                summary['min_duration'] = content_duration # set new minimum duration if we find one smaller than current
            if content_duration > summary['max_duration']:
                summary['max_duration'] = content_duration # likewise for max
            vid_url = 'https://www.youtube.com/watch?v={}'.format(vid_id) # format the youtube video url
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                if not args['dry']: # don't attempt to download if it's a dry run
                    try:
                        ydl.download([vid_url])
                    except youtube_dl.utils.DownloadError as e:
                        print("{} raised for {}".format(e,vid_url)) # skip if you get a download error like 404
                        pass
    # compute average duration
    summary['avg_duration'] = summary['total_duration']/summary['num_cc_vids']
    # format timedeltas into strings for serialization and printing
    summary['total_duration'] = format_timedelta(summary['total_duration'])
    summary['min_duration'] = format_timedelta(summary['min_duration'])
    summary['max_duration'] = format_timedelta(summary['max_duration'])
    summary['avg_duration'] = format_timedelta(summary['avg_duration'])
    # write summary to json file
    with open(os.path.join(write_path, 'channel_summary.json'), 'w') as summary_file:
        json.dump(summary, summary_file)
    # print summary
    if args['verbose'] or args['dry']:
        print("We identified the YouTube Channel '{channel_name}', it has {num_cc_vids} Creative Common videos for a total of {total_duration}. The videos range from {min_duration} to {max_duration} in length with an average of {avg_duration}".format(**summary))
