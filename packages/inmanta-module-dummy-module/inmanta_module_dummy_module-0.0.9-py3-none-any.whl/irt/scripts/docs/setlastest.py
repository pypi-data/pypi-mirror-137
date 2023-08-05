# helpers script for updating latest link
import os
import sys
from pkg_resources import parse_version

latest = str(sorted([x for x in [parse_version(x) for x in os.listdir()] if not x.is_prerelease and not "Legacy" in x.__class__.__name__])[-1])
print("latest is ", latest)

if not os.path.exists(latest):
    raise Exception("%s does not exist"%latest)

if os.path.exists("latest"):
    print("latest link exists")
    if not os.path.islink("latest"):
        raise Exception("latest is not a link")
    if os.path.realpath("latest") == os.path.realpath(latest):
        print("link is up-to-date")
        sys.exit(0)
    print("removing latest link")
    os.remove("latest")

print("creating latest link")
os.symlink(latest,"latest")