import cognitive_face as CF
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import patches
from notification import *
KEY = '375407f0f0d04c2785721db89ab93a62'  # Replace with a valid Subscription Key here.
CF.Key.set(KEY)

BASE_URL = 'https://eastasia.api.cognitive.microsoft.com/face/v1.0'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)


def resize(image,width=1000,length=250):
    im = Image.open(image)
    im.thumbnail( (width,length) )
    im.save(image)

def family_or_not(image="./test.jpg",facelist=1,printf=0):
    temp = []
    rec_list = []
    family = False
    img=image
    result = CF.face.detect(img)
    num_people = len(result)
    if(num_people==0):
        return 2
    for i in range(num_people):
        rec = result[i]['faceRectangle']
        id = result[i]['faceId']
        a = CF.face.find_similars(id,facelist,max_candidates_return = 2)
        try:
            confi = a[0]['confidence']
        except:
            print(a)
            confi = 0
        if confi > 0.6:
            family = True
        else:
            print_face(img,facess=result)
    #if(family):
    #    k = len(temp)
    #    for i in range(k):
    #        CF.face_list.add_face(image,2,target_face=(rec[i]['left'],rec[i]['top'],rec[i]['width'],rec[i]['height']))
    return family

def add_family_member(image):
    CF.face_list.add_face(image,1)

def print_face(img,facess=0):
    if not facess:
        faces = CF.face.detect(img)
    else:
        faces = facess
    image = Image.open(img)
    plt.figure(figsize=(8,8))
    ax = plt.imshow(image, alpha=0.8)
    for i in range(len(faces)):
        fr = faces[i]["faceRectangle"]
        #fa = face[0]["faceAttributes"]
        origin = (fr["left"], fr["top"])
        p = patches.Rectangle(origin, fr["width"], fr["height"], fill=False, linewidth=2, color='b')
        ax.axes.add_patch(p)
        #plt.text(origin[0], origin[1], "%s, %d"%(fa["gender"].capitalize(), fa["age"]), fontsize=20, weight="bold", va="bottom")
    _ = plt.axis("off")
    #plt.show()
    plt.savefig("show.jpg")
    notification("入侵警報！！", uploadIMGUR('./show.jpg'))

#result = CF.face.detect("123.jpg")
#print_face("123.jpg",facess=result)


