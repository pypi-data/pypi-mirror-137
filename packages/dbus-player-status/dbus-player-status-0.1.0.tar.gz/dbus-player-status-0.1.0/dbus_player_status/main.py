import argparse
import json

import dbus

DESCRIPTION = """A tool for extracting media player status from DBus

By default it is configured to use Spotify:

    --bus-name=org.mpris.MediaPlayer2.spotify
    --player-name=Spotify
    --path=/org/mpris/MediaPlayer2
    --interface-property=org.freedesktop.DBus.Properties
    --interface-player=org.mpris.MediaPlayer2.Player

but it may work with other players that also expose information in the same
way via DBus.
"""


def get_parser():
    parser = argparse.ArgumentParser(
        description=DESCRIPTION, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--bus-name", default="org.mpris.MediaPlayer2.spotify")
    parser.add_argument("--player-name", default="Spotify")
    parser.add_argument("--path", default="/org/mpris/MediaPlayer2")
    parser.add_argument("--interface-property", default="org.freedesktop.DBus.Properties")
    parser.add_argument("--interface-player", default="org.mpris.MediaPlayer2.Player")

    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    try:
        status = get_status(args)
        print(json.dumps(status))
    except Exception:
        print(json.dumps({"error": "An unknown error occurred"}))


def get_status(args):
    status = {}
    bus = dbus.SessionBus()
    try:
        player = bus.get_object(args.bus_name, args.path)
        interface = dbus.Interface(player, args.interface_property)
        data = interface.Get(args.interface_player, "Metadata")
        playback_state = interface.Get(args.interface_player, "PlaybackStatus")
    except dbus.exceptions.DBusException:
        return {}

    if playback_state:
        status["state"] = str(playback_state)

    if not data:
        return status

    if title := data.get("xesam:title"):
        status["title"] = str(title)
    if artist := data.get("xesam:artist"):
        status["artist"] = str(artist[0])
    if album := data.get("xesam:album"):
        status["album"] = str(album)

    return status
