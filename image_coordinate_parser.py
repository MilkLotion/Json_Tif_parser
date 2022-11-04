import cv2
import numpy as np
import pandas as pd

#file library
import os
import glob
import shutil

# R G B
color_dict = {
    'PCEgn' : [137,68,68],
    'Cls' : [168,112,0],
    'Mi' : [158,38,0],
    'Km' : [20,86,195],
    'Km1' : [19,92,192],
    'Km2' : [16,99,186],
    'Km3' : [14,106,179],
    'Ky1' : [15,113,171],
    'Km4' : [19,121,164],
    'Km5' : [23,127,155],
    'Ke6' : [31,134,146],
    'Km6' : [37,141,136],
    'Km7' : [45,148,124],
    'Kyjp' : [53,154,112],
    'Kgc' : [60,160,100],
    'Kygs' : [66,165,87],
    'Kjk' : [72,169,73],
    'Kdd' : [77,172,58],
    'Kyjm' : [81,176,42],
    'Kv' : [76,0,115],
    'Tccg' : [233,142,28],
    'Tctr' : [82,14,122],
    'Tcka' : [90,28,130],
    'Tcsa' : [100,43,141],
    'Tcsh' : [234,153,31],
    'Tclc' : [225,167,34],
    'Tclb' : [111,57,152],
    'Tcuc' : [236,185,39],
    'Tcat' : [124,72,165],
    'Tcub' : [136,86,179],
    'Tcyt' : [149,101,192],
    'Tcbr' : [236,202,44],
    'Tcga' : [163,116,206],
    'Tcpp' : [175,129,218],
    'Tcma' : [186,141,229],
    'Tcca' : [195,152,237],
    'Tcpa' : [201,159,244],
    'Tecg' : [235,217,48],
    'Tesh' : [234,227,51],
    'Ted' : [232,237,54],
    'Qa' : [255,255,115]
}


def img_cnt(img):
    myimg = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    myimg = cv2.resize(myimg, dsize=(640, 480), interpolation=cv2.INTER_AREA)

    # 히스토그램 추출 - 빈도수 기준
    hist = cv2.calcHist([myimg], [0], None, [256], [0, 256])
    colors = np.where(hist > 1000)

    for color in colors[0] :
        split_image = myimg.copy()
        split_image[np.where(myimg != color)] = 0
        # thresh = cv2.resize(thresh, dsize=(640, 480), interpolation=cv2.INTER_AREA)
        # canvas = cv2.resize(canvas, dsize=(640, 480), interpolation=cv2.INTER_AREA)

        ret, thresh = cv2.threshold(split_image, color - 1, 255, cv2.THRESH_BINARY)

        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        canvas = np.zeros(myimg.shape)


        # contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        # canvas = np.zeros((contours[0].shape[0], contours[0].shape[0]), dtype=np.uint8)

        # for contour in contours :
        #     cv2.drawContours(canvas, [contour], -1, (0, 255, 0), 3)
        canvas = cv2.drawContours(canvas, contours, -1, 255, 3)

        cv2.imshow("result", split_image)
        cv2.imshow("result - threshold", thresh)
        cv2.imshow("result - contour", canvas)
        cv2.waitKey(0)

    print()


def file_save_csv(contours, img_path, output_dir, mycolor_key) :
    my_path = img_path.rsplit('\\', 1)

    output_dir = output_dir + my_path[0]
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    # with open(output_dir + './' + my_img[1].split('.')[0] + '.txt' , 'w', encoding='utf-8-sig') as f:
    #    f.write(json.dumps(contours, ensure_ascii=False, indent=2))

    df = pd.DataFrame(np.reshape(contours[0], (contours[0].shape[0], 2)), columns=['x', 'y'])
    df.to_csv(output_dir + './' + my_path[1].split('.')[0] + '_' + mycolor_key + '.csv', index=False)


def file_save_img(img_shape, pixel_list, cnt_shape, contours, img_path, output_dir, mycolor_key) :
    my_path = img_path.rsplit('\\', 1)

    output_dir = output_dir + my_path[0] + '_img'
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    canvas_cnt = np.zeros(shape=cnt_shape , dtype=np.uint8)

    canvas_img = np.zeros(shape=img_shape , dtype=np.uint8)
    canvas_img[pixel_list] = color_dict[mycolor_key]
    canvas_img = cv2.cvtColor(canvas_img, cv2.COLOR_RGB2BGR)

    cv2.drawContours(canvas_cnt, contours, -1, 255, 1)

    cv2.imwrite(output_dir + './' + my_path[1].split('.')[0] + '_' + mycolor_key + '.tif', canvas_img)
    cv2.imwrite(output_dir + './' + my_path[1].split('.')[0] + '_' + mycolor_key + '_contour.tif', canvas_cnt)


def image_contour(img_path, output_dir) :
    myimg = cv2.imread(img_path)
    # myimg = cv2.resize(myimg, dsize=(640, 480), interpolation=cv2.INTER_AREA)

    copy_img = myimg.copy()
    copy_img = cv2.cvtColor(copy_img, cv2.COLOR_BGR2RGB)

    key_cnt = 0

    for mycolor_key in color_dict :
        pixel_list = np.where((copy_img == color_dict[mycolor_key]).all(axis=2))

        if pixel_list[0].size > 0 :
            canvas = np.zeros(shape=(copy_img.shape[0],copy_img.shape[1]) , dtype=np.uint8)
            canvas[pixel_list] = 255
            # cv2.imshow("result " + mycolor_key, canvas)

            # contours, hierarchy = cv2.findContours(canvas, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            contours, hierarchy = cv2.findContours(canvas, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_KCOS)

            file_save_csv(contours, img_path, output_dir, mycolor_key)
            file_save_img(myimg.shape, pixel_list, canvas.shape, contours, img_path, output_dir, mycolor_key)
        else :
            key_cnt += 1

        if key_cnt == len(color_dict) :
            raise Exception(img_path.rsplit('\\', 1)[1] + ' file is not matching with color dict')

    # cv2.imshow("ori", myimg)
    # cv2.waitKey(0)


if __name__ == '__main__':
    root_dir = './original'

    result_coordinate_dir = './coordinate_output'
    except_coordinate_path = './coordinate_except'
    if not os.path.isdir(result_coordinate_dir) :
        os.makedirs(result_coordinate_dir)


    original_files = [path for path in glob.glob(f'{root_dir}/*/**/*.tif', recursive=True)]
    # original_files = [path for path in glob.glob(f'{root_dir}/*.tif', recursive=True)]

    for img_path in original_files :
        try :
            image_contour(img_path, result_coordinate_dir)
        except Exception as e:
            print(e)

            # print(img_path + " file parsing failed !!!!")

            my_path = img_path.rsplit('\\', 1)

            if not os.path.isdir(except_coordinate_path) :
                os.makedirs(except_coordinate_path)

            shutil.copy(img_path, except_coordinate_path + './' + my_path[1])

    # img_cnt('./tif\\GP_LD_GE35_D_01_01.tif')