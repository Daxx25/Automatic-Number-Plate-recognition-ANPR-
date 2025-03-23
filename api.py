from flask import *
from werkzeug.utils import secure_filename
from product import *
from splitfunction import *
import time
import shutil
app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

    

@app.route('/get_video', methods=['POST'])
def get_video():

    #saving incoming vedio file
    f = request.files['file']
    
    #saving src directory path
    src = os.getcwd()
    
    os.chdir(src)
    directory = "input_vedio"
    #input_vedio is saved in this directory
    input_dir = os.path.join(src, directory)
    
    os.mkdir(input_dir)
    if(os.path.exists(input_dir)):
        pass

    else:
        os.mkdir(input_dir)

    os.chdir(input_dir)
    f.save(secure_filename(f.filename))
    os.chdir(src)
    
    #path of the vedio file to be passed to frame sliptting function
    vediopath = os.path.join(input_dir, secure_filename(f.filename))
    
     # ./data ->> directory where all generated frames will be stored.
    data_dir = os.path.join(src, 'data')

    if os.path.exists(data_dir):
        shutil.rmtree('./data')

    os.mkdir('data')

   
    frames = splitvedio(vediopath,src,data_dir)
    time.sleep(2)
    
    os.chdir(data_dir)

    #getting the no of frames generated in data_dir folder
    no_of_frames_created = len(os.listdir(data_dir))
    print(no_of_frames_created)

    detected_liscense_plates = []

    #looping through each frame to scan the liscence plates
    for i in range(0,no_of_frames_created,30):
        name = 'frame_' + str(i) + '_.jpg'
        img_path = os.path.join(data_dir, name)
        image_path = img_path.replace(os.sep, '/')
        lic_text = database1(image_path,src)
        detected_liscense_plates.append(lic_text)
    
    return render_template('index.html',message = 'Task Completed Thank You !',result = detected_liscense_plates)



if __name__ == '__main__':
    app.run()
