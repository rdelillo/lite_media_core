""" path templates.
"""

from __future__ import absolute_import

import re

# Matches the dailies show mount point. Ex: "/Volumes/SSD/rdo/staging" , "/Volumes/SSD002/rdo/staging"
DAILIES_MOUNT_REGEX = r"(?P<dailiesMount>/Volumes/SSD\d*/rdo/staging)"

# Matches the old dailies show mount point. Ex: "/Volumes/SSD", "/Volumes/SSD002"
OLD_DAILIES_MOUNT_REGEX = r"(?P<oldDailiesMount>/Volumes/SSD\d*)"

# Matches the network and raid show mount points,
# Ex: "/rdo/shows", "/rdo/ads", "/Volumes/raid/nuke_TMP/rdo/shows", "/foo/bar/shows", "/foo/bar/42/ads"
NETWORK_AND_RAID_MOUNT_REGEX = r"(?P<networkMount>.*/(?:shows|ads))"

# Matches a date. Ex: "2019_03_25" TODO: Should we support different separators? "..(_|-)\d{2}(_|-).."
DATE_REGEX = r"(?P<date>\d{4}_\d{2}_\d{2})"

# Matches a project code. Ex: "Boy1", "lak", "kry2"
PROJECT_REGEX = r"(?P<project>[a-zA-Z0-9]+)"

# Matches a sequence code. Ex: "0001", "dev", "Dev01"
SEQUENCE_REGEX = r"(?P<sequence>[a-zA-Z0-9]+)"

# Matches a shot name. Ex: "0001", "dev", "Dev01"
SHOT_TANK_NAME_REGEX = r"(?P<shotTankName>[a-zA-Z0-9]+)"

# Matches a shot code. Ex: "foo01_bar0020", "Foo01_Bar0020", "foo_bar"
SHOT_REGEX = r"(?P<shot>[a-zA-Z0-9]+_[a-zA-Z0-9]+)"

# Matches an asset code. Ex: "01a_lookVillage", "01alookVillage", "01alookvillage", "lookvillage"
ASSET_REGEX = r"(?P<asset>\w+)"

# Matches a user login. (any character that is not "/" any number of times.)
USER_REGEX = r"(?P<user>[^/]*)"

# Note: Never rely on an explicit trailing "/" in order to match the input string.
# '/rdo/shows/<show>/<sequence>/<shotTankName>' and '/rdo/shows/<show>/<sequence>/<shotTankName>/'
# Should both be supported.

# Note: The templates are ordered by the amount of named capturing groups.
# This is important for lite_media_core.path_utils.path.getContextFromPath
# to work properly since it assumes the first
# match to be the most qualified.
TEMPLATES = (
    # Shot daily template.
    # Match example: "/Volumes/SSD/rdo/staging/<project>/_dailies/<date>/<user>/<shot>_comp_v005"
    re.compile(
        r"{dailiesMount}/{project}/_dailies/{date}/{user}/{shot}_".format(
            dailiesMount=DAILIES_MOUNT_REGEX,
            project=PROJECT_REGEX,
            date=DATE_REGEX,
            user=USER_REGEX,
            shot=SHOT_REGEX,
        )
    ),
    # Asset daily template.
    # Match example: /Volumes/SSD/rdo/staging/<project>/_dailies/<date>/<user>/_assets/<asset>
    re.compile(
        r"{dailiesMount}/{project}/_dailies/{date}/{user}/_assets/{asset}".format(
            dailiesMount=DAILIES_MOUNT_REGEX,
            project=PROJECT_REGEX,
            date=DATE_REGEX,
            user=USER_REGEX,
            asset=ASSET_REGEX,
        )
    ),
    # Old shot daily template.
    # Match example: /Volumes/SSD/<project>/_dailies/<date>/<user>/<shot>_comp_v005/
    # Use case example: /Volumes/SSD/imm/_dailies/2010_09_23/vincent/ht068_0010_comp_v002/...
    re.compile(
        r"{oldDailiesMount}/{project}/_dailies/{date}/{user}/{shot}_".format(
            oldDailiesMount=OLD_DAILIES_MOUNT_REGEX,
            project=PROJECT_REGEX,
            date=DATE_REGEX,
            user=USER_REGEX,
            shot=SHOT_REGEX,
        )
    ),
    # Shot template.
    # Match examples: "/rdo/shows/<project>/<sequence>/<shotTankName>",
    # "/rdo/ads/<project>/<sequence>/<shotTankName>",
    # "/Volumes/raid/nuke_TMP/rdo/shows/<project>/<sequence>/<shotTankName>/"
    re.compile(
        r"{networkAndRaidMount}/{project}/{sequence}/{shotTankName}".format(
            networkAndRaidMount=NETWORK_AND_RAID_MOUNT_REGEX,
            project=PROJECT_REGEX,
            sequence=SEQUENCE_REGEX,
            shotTankName=SHOT_TANK_NAME_REGEX,
        )
    ),
    # Published shot template.
    # Match examples: "/rdo/shows/<project>/.published/<sequence>/<shotTankName>",
    #                 "/rdo/ads/<project>/.published/<sequence>/<shotTankName>/",
    #                 "/Volumes/raid/nuke_TMP/rdo/shows/<project>/.published/<sequence>/<shotTankName>"
    # Note: "/.published(?!/assets)/" uses the directory following the .published directory as the sequence
    # name. UNLESS it is named "assets".
    re.compile(
        r"{networkAndRaidMount}/{project}/.published(?!/assets)/{sequence}/{shot}".format(
            networkAndRaidMount=NETWORK_AND_RAID_MOUNT_REGEX,
            project=PROJECT_REGEX,
            sequence=SEQUENCE_REGEX,
            shot=SHOT_REGEX,
        )
    ),
    # Plate daily template.
    # Match example: /Volumes/SSD/rdo/staging/<project>/_plates/<shot>_plate_mpwr_v001/
    re.compile(
        r"{dailiesMount}/{project}/_plates/{shot}_".format(
            dailiesMount=DAILIES_MOUNT_REGEX, project=PROJECT_REGEX, shot=SHOT_REGEX,
        )
    ),
    # Old asset daily template (Doesn't use the old dailies mount point).
    # (Supposed to be deprecated but still used by some active projects.)
    # Match example: /Volumes/SSD/rdo/staging/<project>/_assets/<asset>/
    # Use case example: /Volumes/SSD/rdo/staging/lak/_assets/rat/rat_...
    re.compile(
        r"{dailiesMount}/{project}/_assets/{asset}".format(
            dailiesMount=DAILIES_MOUNT_REGEX, project=PROJECT_REGEX, asset=ASSET_REGEX,
        )
    ),
    # Asset template.
    # Match examples: "/rdo/shows/<project>/_asset/<asset>/", "/rdo/ads/<project>/_asset/<asset>",
    #                 "/Volumes/raid/nuke_TMP/rdo/shows/<project>/_asset/<asset>"
    re.compile(
        r"{networkAndRaidMount}/{project}/_asset/{asset}".format(
            networkAndRaidMount=NETWORK_AND_RAID_MOUNT_REGEX, project=PROJECT_REGEX, asset=ASSET_REGEX,
        )
    ),
    # Published asset template.
    # Match example: /rdo/shows/<project>/.published/assets/<asset>
    re.compile(
        r"{networkAndRaidMount}/{project}/.published/assets/{asset}".format(
            networkAndRaidMount=NETWORK_AND_RAID_MOUNT_REGEX, project=PROJECT_REGEX, asset=ASSET_REGEX,
        )
    ),
    # Sequence template
    # Match example: "/rdo/shows/<project>/<sequence>", "/rdo/ads/<project>/<sequence>",
    #                "/Volumes/raid/nuke_TMP/rdo/shows/<project>/<sequence>"
    re.compile(
        r"{networkAndRaidMount}/{project}/{sequence}".format(
            networkAndRaidMount=NETWORK_AND_RAID_MOUNT_REGEX, project=PROJECT_REGEX, sequence=SEQUENCE_REGEX,
        )
    ),
    # Published sequence template
    # Match example: "/rdo/shows/<project>/.published/<sequence>", "/rdo/ads/<project>/.published/<sequence>",
    #                "/Volumes/raid/nuke_TMP/rdo/shows/<project>/.published/<sequence>/"
    re.compile(
        r"{networkAndRaidMount}/{project}/.published/{sequence}".format(
            networkAndRaidMount=NETWORK_AND_RAID_MOUNT_REGEX, project=PROJECT_REGEX, sequence=SEQUENCE_REGEX,
        )
    ),
    # Project daily template.
    # Match example: /Volumes/SSD/rdo/staging/<project>
    re.compile(r"{dailiesMount}/{project}".format(dailiesMount=DAILIES_MOUNT_REGEX, project=PROJECT_REGEX,)),
    # Project template:
    # Matches: "/rdo/shows/<project>", "/rdo/ads/<project>/", "/Volumes/raid/nuke_TMP/rdo/shows/<project>"
    re.compile(
        r"{networkAndRaidMount}/{project}".format(
            networkAndRaidMount=NETWORK_AND_RAID_MOUNT_REGEX, project=PROJECT_REGEX,
        )
    ),
)
