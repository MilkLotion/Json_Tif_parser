import os
import json
import glob
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


def dict_maker(mystring, mydict, pre_key) :
    new_dict = dict()

    for i in range(len(mystring)) :
        letter = mystring[i]

        if letter == '{':
            mystring_split_s = mystring.split('{', 1)

            new_dict[mystring_split_s[0]] = ''

            new2_dict = dict_maker(mystring_split_s[1], new_dict, mystring_split_s[0])

            if len(new2_dict) > 0 :
                if type(new2_dict) is dict :
                    for new2_dict_key in new2_dict.keys() :
                        new_dict[new2_dict_key] = new2_dict[new2_dict_key]
                elif type(new2_dict) is str :
                    for new_dict_key in new_dict.keys() :
                        new_dict[new_dict_key] = new2_dict

            if len(mydict) > 0 :
                if pre_key in mydict.keys() :
                    mydict[pre_key] = new_dict

            break

        elif letter == '}' :

            mystring_split_e = mystring.split('}', 1)

            if mystring.index('}') == len(mystring) - 2 :
                return mystring_split_e[0]

            if len(mystring_split_e) > 0 and mystring_split_e[-1] != '}' :
                mydict[pre_key] = mystring_split_e[0]

                new_dict = dict_maker(mystring_split_e[1], new_dict, None)

                if len(new_dict) > 0 and type(new_dict) is dict:
                    for new_dict_key in new_dict.keys() :
                        mydict[new_dict_key] = new_dict[new_dict_key]

            else :
                mydict[pre_key] = mystring_split_e[0]

            break

        else :
            continue

    if len(mydict) == 0 :
        mydict = new_dict

    return mydict

def dict_maker2(mystring, mydict) :
    mystring = mystring.replace(' ', '')

    mystring_key, mystring_val = mystring.split(':', 1)

    while mystring_val.count(':') > 0 :
        if mystring_val.count(',') > 0 :
            if mystring_val.index(':') < mystring_val.index(','):
                dict_val = mystring_val.split(':', 1)
                mystring_key = dict_val[0]
                mystring_val = dict_val[1]

            else:
                dict_val = mystring_val.split(',', 1)

                # next parser check
                next_parser_1 = dict_val[1].index(',') if dict_val[1].count(',') > 0 else 9999
                next_parser_2 = dict_val[1].index(':') if dict_val[1].count(':') > 0 else 9999

                if next_parser_1 < next_parser_2 :
                    dict_val_1_split = dict_val[1].split(',', 1)

                    dict_val[0] = dict_val[0] + ',' + dict_val_1_split[0]
                    dict_val[1] = dict_val_1_split[1]

                mydict[mystring_key] = dict_val[0]
                mystring_val = dict_val[1]
        else :
            dict_val = mystring_val.split(':', 1)
            mystring_key = dict_val[0]
            mystring_val = dict_val[1]

    mydict[mystring_key] = mystring_val

    return mydict

def dict_name_update(first_line) :
    new_dict = dict()

    first_line = first_line.replace('{', '').strip()

    file_name = first_line.split(':', 1)[1].replace('"', '')

    new_dict['Info'] = {"File_name" : file_name}

    return new_dict

def mydict_to_parsingJson(mydict, new_dict) :
    mydata = mydict['data']

    lith_arr = []
    # boun_arr = []
    # rang_arr = []

    for mydata_key in mydata.keys() :
        if mydata_key.count('Lithology') > 0 :
            lith_data = mydata[mydata_key]

            lith_dict = dict()
            lith_dict = dict_maker2(lith_data, lith_dict)

            # idx str to int
            # try :
            #     lith_dict['Litho_idx'] = int(lith_dict['Litho_idx'])
            # except :
            #     lith_dict['Litho_idx'] = lith_dict['Litho_idx']

            for lith_dict_key in lith_dict.keys() :
                if lith_dict_key in ['Litho_depth_S', 'Litho_depth_E'] :
                    lith_dict[lith_dict_key] = int(lith_dict[lith_dict_key])
                elif lith_dict_key == 'Litho_idx' :
                    if lith_dict[lith_dict_key] in idx_dict :
                        lith_dict[lith_dict_key] = idx_dict[lith_dict[lith_dict_key]]
                    else :
                        lith_dict[lith_dict_key] = int(lith_dict[lith_dict_key])

            lith_arr.append(lith_dict)

    new_dict['Lithology'] = lith_arr

    # new_dict['Boundary'] = boun_arr
    # new_dict['Range'] = rang_arr


    # boundary, range after (순서 맞추기 위함)
    for mydata_key in mydata.keys() :
        # Boundary Parser
        if mydata_key.count('Boundary') > 0 :
            boun_data = mydata[mydata_key]

            boun_dict = dict()
            boun_dict = dict_maker2(boun_data, boun_dict)

            # B_count to num
            if 'B_count' in boun_dict.keys() :
                boun_dict['B_Count'] = int(boun_dict.pop('B_count'))
            else :
                boun_dict['B_Count'] = int(boun_dict['B_Count'])

            # boun_arr.append(boun_dict)
            new_dict['Boundary'] = boun_dict

        # False Parser
        elif mydata_key.count('Fault') > 0 :
            fault_data = mydata[mydata_key]

            fault_dict = dict()
            fault_dict = dict_maker2(fault_data, fault_dict)

            for fault_dict_key in fault_dict.keys() :
                if fault_dict[fault_dict_key].count('.') > 0 :
                    fault_dict[fault_dict_key] = float(fault_dict[fault_dict_key])
                else :
                    fault_dict[fault_dict_key] = int(fault_dict[fault_dict_key])

            new_dict['Fault'] = fault_dict

        # Inf_fault Parser
        elif mydata_key.count('Inf_fault') > 0 :
            inf_fault_data = mydata[mydata_key]

            inf_fault_dict = dict()
            inf_fault_dict = dict_maker2(inf_fault_data, inf_fault_dict)

            for inf_fault_dict_key in inf_fault_dict.keys() :
                if inf_fault_dict[inf_fault_dict_key].count('.') > 0 :
                    inf_fault_dict[inf_fault_dict_key] = float(inf_fault_dict[inf_fault_dict_key])
                else :
                    inf_fault_dict[inf_fault_dict_key] = int(inf_fault_dict[inf_fault_dict_key])

            new_dict['Inf_fault'] = inf_fault_dict

        # Etc Parser
        elif mydata_key.count('Etc') > 0 :
            etc_data = mydata[mydata_key]

            etc_dict = dict()
            etc_dict = dict_maker2(etc_data, etc_dict)

            # dict del, pop array shallow copy
            etc2_dict = dict()
            test2 = etc_dict.keys()

            for etc_dict_key in test2 :
                # D_Direction_@ to D_Direction
                if etc_dict_key.count('D_Direction') > 0 :
                    etc2_dict['D_Direction'] = etc_dict[etc_dict_key]

                # D_Degree_@ to D_Degree and str to int
                elif etc_dict_key.count('D_Degree') > 0 :
                    etc2_dict['D_Degree'] = int(etc_dict[etc_dict_key])

            # rang_arr.append(rang_dict)
            new_dict['ETC'] = etc2_dict

        # Range Parser
        elif mydata_key.count('Range') > 0 :
            rang_data = mydata[mydata_key]

            rang_dict = dict()
            rang_dict = dict_maker2(rang_data, rang_dict)

            for rang_dict_key in rang_dict.keys() :
                if rang_dict_key in ['Start_pt', 'End_pt'] :
                    convert_val = rang_dict[rang_dict_key]

                    if convert_val.count(',') > 0 :
                        replace_str = ''
                        convert_val_split = convert_val.split(',')[:2]

                        # 소수점 정리
                        for convert_val2 in convert_val_split :
                            convert_val2_split = convert_val2.split('.')
                            replace_str += convert_val2_split[0] + '.' + convert_val2_split[1][:6] + ', '

                        rang_dict[rang_dict_key] = replace_str[:-len(', ')]

                    else :
                        convert_val_split = convert_val.split('.')
                        rang_dict[rang_dict_key] = convert_val_split[0] + '.' + convert_val_split[1][:6]

                elif rang_dict_key in ['Length_m', 'Start_depth', 'End_depth', 'Elevation_MIN', 'Elevation_MAX', 'Elevation_BL'] :
                    if rang_dict[rang_dict_key].count('.') > 0 :
                        rang_dict[rang_dict_key] = float(rang_dict[rang_dict_key])
                    else :
                        rang_dict[rang_dict_key] = int(rang_dict[rang_dict_key])


            # rang_arr.append(rang_dict)
            new_dict['Range'] = rang_dict

    return new_dict

def line_parser(mystring) :
    mystring = mystring.replace('\r\n', '')
    mystring = mystring.replace('\n', '')
    mystring = mystring.replace('\r', '')
    mystring = mystring.replace('\t', '')

    mystring = mystring.strip()

    return mystring

def file_to_str(file) :
    ori = open(file, encoding='utf-8')
    ori_lines = ori.readlines()

    # lines = ''
    #
    # if ori_lines[0].count('File_name') :
    #     lines = ori_lines[0].replace('{', '').strip() + ',"data":{'
    # else :
    #     lines = '{"data":{'

    lines = '"data"{'

    for line in ori_lines[1:] :
         lines += line_parser(line)

    lines = lines.replace('""', '","')

    lines = lines.replace('"', '')

    # 251부터 Lithology_N { 없는 부분있어서 파싱
    for i in range(10) :
        if lines.count('Lithology_' + str(i) + '{') == 0 and lines.count('Lithology_' + str(i)) > 0 :
            lines = lines.replace('Lithology_' + str(i), 'Lithology_' + str(i) + '{')

    # 338부터 } boundary 없음
    if lines.count('}Boundary') == 0 and lines.count('Boundary') > 0 :
        lines = lines.replace('Boundary', '}Boundary')
        lines = lines.replace(',}Boundary', '}Boundary')

    # 378부터 } falut 없음
    if lines.count('}Fault') == 0 and lines.count('Fault') > 0 :
        lines = lines.replace('Fault', '}Fault')
        lines = lines.replace(',}Fault', '}Fault')

    # 381부터 } Lithology_N 없는 부분있어서 파싱
    for i in range(10) :
        if lines.count('}Lithology_' + str(i)) == 0 and lines.count('Lithology_' + str(i)) > 0 :
            lines = lines.replace('Lithology_' + str(i), '}Lithology_' + str(i))

        lines = lines.replace('Lithology_' + str(i) +'{,', 'Lithology_' + str(i) + '{')
        lines = lines.replace('{}Lithology_' + str(i), '{Lithology_' + str(i))

    # GM_LD_HF31_171 } Range 없는 부분있어서 파싱
    if lines.count('}Range') == 0 and lines.count('Range') > 0 :
        lines = lines.replace('Range', '}Range')
        lines = lines.replace(',}Range', '}Range')


    return ori_lines[0], lines



if __name__ == "__main__":

    root_dir = "./original"
    original_json_files = [path for path in glob.glob(f'{root_dir}/*/**/*.json', recursive=True)]

    # original_json_path = './original_json/GM_LD_HD25'


    result_json_path = './json_output'
    except_json_path = './json_except'

    if not os.path.isdir(result_json_path) :
        os.makedirs(result_json_path)

    # original_json_files = os.listdir(original_json_path)

    # filename = 'GM_LD_HD25_013.json'

    for original_json_file in original_json_files :
        try :
            original_json_file = original_json_file.replace(root_dir, '')

            # print(original_json_file + " file parsing start")
            first_line, lines = file_to_str(root_dir + original_json_file)

            mydict = dict()

            mydict = dict_maker(lines, mydict, None)

            new_dict = dict_name_update(first_line)

            new_dict = mydict_to_parsingJson(mydict, new_dict)

            # auto directory builder
            original_json_path = original_json_file[:original_json_file.rindex('\\')] \
                if original_json_file.count('\\') > 0 \
                else original_json_file[:original_json_file.rindex('/')]

            output_dir = result_json_path + original_json_path
            if not os.path.isdir(output_dir) :
                os.makedirs(output_dir)

            with open(result_json_path + original_json_file , 'w', encoding='utf-8-sig') as f:
                f.write(json.dumps(new_dict, ensure_ascii=False, indent=2))

            # print(original_json_file + " file parsing end")

        except Exception as e :
            print(e)
            original_json_file = original_json_file.replace(root_dir, '')

            print(original_json_file + " file parsing failed !!!!")

            original_json_path = original_json_file[:original_json_file.rindex('\\')] \
                if original_json_file.count('\\') > 0 \
                else original_json_file[:original_json_file.rindex('/')]

            except_dir = except_json_path + original_json_path
            if not os.path.isdir(except_dir) :
                os.makedirs(except_dir)

            shutil.copy(root_dir + original_json_file, except_json_path + original_json_file)

        # print()