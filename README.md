# podcaster
Record a scheduled streaming audio feed, save it as an MP3, serve it as a podcast feed for subscription through iTunes.

## Installation Notes

### Setup the Server (Raspberry Pi)

1.  Install the OS and updates
2.  Set a static IP address (this code uses 192.168.1.198)
  *  Method 1:  Set a reserved IP for the Raspberry Pi in the router configurations
  *  Method 2:  Edit the interfaces file
    *  $ `sudo nano /etc/network/interfaces`
    *  $ `sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`
3.  Install web server (Apache)
  *  $ `sudo apt-get install apache2 -y`
  *  Web files are served out of `/var/www/html/`
4.  Create the following folders
  *  `/var/www/html/podcast/`
  *  `/var/www/html/podcast/media/`
  *  `/user/pi/podcast/`
  *  Set the ownership to `pi` user `sudo chown pi:pi *.*`
5.  Copy the Python scripts from this repository to `/user/pi/python`
6.  Copy the xml and html files to `/var/www/html/podcast/`
  *  Change the permissions of the xml files: `chmod 766 *.xml`
7.  Install the [mutagen Python library](https://pypi.python.org/pypi/mutagen) for MP3 tagging
  *  $ `pip install mutagen`
8.  Install the [Request library](http://docs.python-requests.org) to get playlist info off the API
  *  $ `pip install requests`
9.  Schedule the recordings using Cron
  *  $ `crontab -e` to edit the crontab
  *  `# 0 16 * * 1-5 python /user/pi/python/PodRipper.py MBE 180`

Note:  Raspberry Pi needs to be set to local timezone in raspi-config utility

* command line call:
`$> python PodRipper [programname] [duration in minutes]`
