import subprocess

"""
Plate solve image
"""
def plate_solve(filename):
    # Todo : Loop through latest images in directory and solve every 10-20s of new images
    astap_location = "c:\\Program Files\\astap\\astap.exe"
    subprocess.call(astap_location + " -f " + filename + " -r 50")

