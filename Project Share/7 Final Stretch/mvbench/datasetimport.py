import os, shutil

# Space check
total, used, free = shutil.disk_usage("/kaggle/working")
print(f"Free: {free/1024**3:.1f} GB")

# Sirf sample 0-999 ke video names nikalo
video_names = []
for i in range(0, 1000):
    video_names.append(mvbench_dataset[i]['video'])

unique_videos = list(set(video_names))
print(f"Unique videos needed: {len(unique_videos)}")
print("Sample names:", unique_videos[:5])


#------------------------------------------


import os

os.makedirs("/kaggle/working/videos", exist_ok=True)

# MVBench videos Google Drive se available hain official repo ke through
# Pehle distribution check karo
ssv2 = []
kinetics = []
tv = []

for name in unique_videos:
    base = name.replace('.mp4','').replace('.webm','')
    if len(base) == 5 and base.isalnum() and any(c.isalpha() for c in base):
        ssv2.append(name)
    elif base.isdigit():
        kinetics.append(name)
    else:
        tv.append(name)

print(f"SSv2 type    : {len(ssv2)}")
print(f"Kinetics type: {len(kinetics)}")  
print(f"TV/other type: {len(tv)}")
print("\nTV samples:", tv[:3])
print("Kinetics samples:", kinetics[:3])

#---------------------------------------------------------------------------------------------

from huggingface_hub import hf_hub_download, list_repo_files
import os

# Pehle dekho repo mein kya kya hai
print("Checking repo files...")
all_files = list(list_repo_files("OpenGVLab/MVBench", repo_type="dataset"))
print(f"Total files in repo: {len(all_files)}")

# Video/zip files dhundo
video_files = [f for f in all_files if any(ext in f for ext in ['.mp4', '.zip', '.tar', '.webm', 'video'])]
print(f"\nVideo/archive files found: {len(video_files)}")
for f in video_files[:20]:
    print(" ", f)

# Baaki sab files bhi dekho
print("\nAll file types:")
extensions = set(f.split('.')[-1] for f in all_files if '.' in f)
print(extensions)

####------------------------------------------------------------------



from huggingface_hub import hf_hub_download
import zipfile, os

needed = set(unique_videos)
print(f"Total needed: {len(needed)}\n")

all_zips = [
    "video/ssv2_video.zip", "video/tvqa.zip", "video/star.zip",
    "video/clevrer.zip", "video/data0613.zip", "video/FunQA_test.zip",
    "video/Moments_in_Time_Raw.zip", "video/perception.zip",
    "video/scene_qa.zip", "video/sta.zip", "video/vlnqa.zip"
]

found_total = set()

for zip_name in all_zips:
    zip_path = hf_hub_download(
        repo_id="OpenGVLab/MVBench",
        filename=zip_name,
        repo_type="dataset",
        local_dir="/kaggle/working/zips/"
    )
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zip_files = set(os.path.basename(f) for f in zf.namelist())
        matched = zip_files & needed
        found_total |= matched
        print(f"{zip_name.split('/')[-1]:<35} matched: {len(matched)}")

print(f"\n✅ Total found : {len(found_total)}")
print(f"❌ Not found   : {len(needed - found_total)}")
print(f"Missing videos : {list(needed - found_total)[:10]}")

#--------------------------------------------------

import zipfile, os

needed = set()
for i in range(0, 1000):
    needed.add(os.path.basename(mvbench_dataset[i]['video']))

os.makedirs("/kaggle/working/videos", exist_ok=True)

matched_zips = [
    "ssv2_video.zip", "star.zip", "clevrer.zip",
    "data0613.zip", "perception.zip", "sta.zip"
]

total_extracted = 0
for zip_name in matched_zips:
    zip_path = f"/kaggle/working/zips/video/{zip_name}"
    print(f"📦 Extracting {zip_name}...")
    with zipfile.ZipFile(zip_path, 'r') as zf:
        for file_info in zf.infolist():
            fname = os.path.basename(file_info.filename)
            if fname in needed:
                file_info.filename = fname
                zf.extract(file_info, "/kaggle/working/videos/")
                total_extracted += 1

print(f"\n✅ Extracted: {total_extracted}")
print(f"📁 Videos folder: {len(os.listdir('/kaggle/working/videos/'))} files")
