import subprocess
import tempfile
import musicbrainzngs
import discid

def analyze():
    success = subprocess.call(["cdparaonoia", "-A"])
    return success == 0

def rip():
    success = subprocess.call(["cdparanoia", "-l", "-z", "-B"])
    return success == 0

def compress(files):
    for file_name in files:
        success = subprocess.call(["flac", "-8", file_name])
        if success == 1:
            return False

    return True

def get_cuesheet():
    toc_file = tempfile.mkstemp()[1]
    success = subprocess.call(["cdrdao", "read-toc", "--device", 
                               device, "--datafile", toc_file])
    if success == 1:
        return False

    success = subprocess.call(["cueconvert", "-i toc", "-o cue",
                               toc_file, "cuefile.cue"])
    return success == 0

def tag(files):
    discid = discid.read()
    musicbrainzngs.set_useragent("whirrer", 0.1)
    disc_info = musicbrainzngs.get_releases_by_discid(discid,
                                                      includes=["labels"])


if __name__ == "__main__":
    analyze()
    rip()
