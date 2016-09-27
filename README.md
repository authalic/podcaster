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
  *  `/var/www/html/podcast/media/'
  *  `/user/pi/podcast/`
  *  Set the ownership to `pi` user
  *  Set the permissions to read, write, execute `777`
4.  Copy the Python scripts from this repository to `/user/pi/python`
5.  Copy the xml and html files to `/var/www/html/podcast/`
6.  Install the [mutagen Python library](https://pypi.python.org/pypi/mutagen) for MP3 tagging
  *  $ `pip install mutagen`
7.  Schedule the recordings using Cron
  *  $ `crontab -e` to edit the crontab
  *  `# 0 16 * * 1-5 python /user/pi/python/PodRipper.py MBE 180`
  
