import os
import glob
import json
import csv
import pandas as pd
import shutil

idx_dict = {
    'PCEgn' : 1,
    'Cls' : 2,
    'Mi' : 3,
    'Km' : 4,
    'Km1' : 5,
    'Km2' : 6,
    'Km3' : 7,
    'Ky1' : 8,
    'Km4' : 9,
    'Km5' : 10,
    'Ke6' : 11,
    'Km6' : 12,
    'Km7' : 13,
    'Kyjp' : 14,
    'Kgc' : 15,
    'Kygs' : 16,
    'Kjk' : 17,
    'Kdd' : 18,
    'Kyjm' : 19,
    'Kv' : 20,
    'Tccg' : 21,
    'Tctr' : 22,
    'Tcka' : 23,
    'Tcsa' : 24,
    'Tcsh' : 25,
    'Tclc' : 26,
    'Tclb' : 27,
    'Tcuc' : 28,
    'Tcat' : 29,
    'Tcub' : 30,
    'Tcyt' : 31,
    'Tcbr' : 32,
    'Tcga' : 33,
    'Tcpp' : 34,
    'Tcma' : 35,
    'Tcca' : 36,
    'Tcpa' : 37,
    'Tecg' : 38,
    'Tesh' : 39,
    'Ted' : 40,
    'Qa' : 41
}


if __name__ == '__main__':
    json_dir = './json_output'
    coordinate_dir = './coordinate_output'

    merge_dir = './merge_output'
    except_dir = './merge_except'
    if not os.path.isdir(merge_dir) :
        os.makedirs(merge_dir)

    json_files = [path for path in glob.glob(f'{json_dir}/*/**/*.json', recursive=True)]

    for json_file in json_files :
        try :
            my_path, my_file = json_file.rsplit('\\', 1)

            my_file = my_file.rsplit('.', 1)[0]

            coordinate_files = [path for path in glob.glob(f'{coordinate_dir}/*/**/' + my_file + '*.csv', recursive=True)]

            if len(coordinate_files) > 0 :
                with open(json_file, 'r', encoding='utf-8-sig') as my_json:
                    my_json = json.load(my_json)
                lithology_dicts = my_json['Lithology']

                for coordinate_file in coordinate_files :
                    idx_parse = idx_dict[coordinate_file.rsplit('_', 1)[1].split('.')[0]]
                    for lithology_dict in lithology_dicts :
                        if lithology_dict['Litho_idx'] == idx_parse :
                            lithology_dict["Coordinates"] = [pd.read_csv(coordinate_file).values.tolist()]
                            break

                    # auto directory builder
                merge_path, merge_file = json_file.rsplit('\\', 1)
                _, merge_path = merge_path.split('\\', 1)

                merge_path = merge_dir + '\\' + merge_path
                if not os.path.isdir(merge_path):
                    os.makedirs(merge_path)

                with open(merge_path + '\\' + merge_file, 'w', encoding='utf-8-sig') as f:
                    f.write(json.dumps(my_json, ensure_ascii=False, indent=2))

                # file line cleaner
                file_reader = open(merge_path + '\\' + merge_file, 'r', encoding='utf-8-sig')
                new_line = ''
                new_line_flag = False
                new_line_flag2 = 0
                for line in file_reader.readlines() :
                    if line.count('"Coordinates": [') > 0 :
                        new_line_flag = True
                        new_line_flag2 = 0

                    if new_line_flag :
                        if line.replace(' ', '') == ']\n':
                            line = line.replace(' ', '')
                            new_line_flag = False

                        elif new_line_flag2 == 2 :
                            line = line.replace('\n', '')

                        elif new_line_flag2 > 2 :
                            line = line.replace(' ', '')
                            line = line.replace('\n', '')

                        new_line_flag2 += 1

                    new_line += line
                file_reader.close()

                file_writer = open(merge_path + '\\' + merge_file, 'w', encoding='utf-8-sig')
                file_writer.write(new_line)
                file_writer.close()


                # data = [line for line in f.readlines()].join("").replace("[\n", "[").replace("\n]", "]")

            else :
                raise Exception(my_file + " coordinate file is not exists")

        except Exception as e :
            print(e)

            if not os.path.isdir(except_dir) :
                os.makedirs(except_dir)

            shutil.copy(json_file, except_dir + './' + my_file + '.json')