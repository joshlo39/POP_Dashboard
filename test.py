from utils import *
# Usage
# Usage example
file_path = "test_hyperlink.pdf"
url = "https://www.example.com"
text = "Click here for Example"
save_dir = "Mobile_Dev_Test"
video_hyperlinks = []
image_paths =[]
inner_array = []
file_names = os.listdir(save_dir)
#file_names.sort(key = lambda x: int(x.split('_')[1].split('.')[0]))
for idx, filename in enumerate(file_names):
    if filename.endswith(".png"):
        print(f"Index: {idx}, Filename: {filename}, URI: {video_hyperlinks[idx] if len(video_hyperlinks) > 0 else 'https://www.youtube.com/watch?v=v7ScGV5128A'}")
        filepath = os.path.join(save_dir, filename)
        inner_array.append((filepath, (f" ", video_hyperlinks[idx] if len(video_hyperlinks) > 0 else 'https://www.youtube.com/watch?v=v7ScGV5128A')))
        
        if len(inner_array) == 4:
            image_paths.append(sorted(inner_array))
            inner_array = []
#if there is a non-full page of images, then append it to the end of the outer array
if inner_array:
    image_paths.append(inner_array)

create_pdf_with_2x2_images_hyperlinks_small_hyperlink("mobile_dev_test.pdf",image_paths)
