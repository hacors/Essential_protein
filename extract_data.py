import global_config
import os
import zipfile
from collections import Counter


def deg_split(deg_path, deg_split_path):
    result = {}
    file_list = os.listdir(deg_path)
    for zip_name in file_list:
        file_data = zipfile.ZipFile(os.path.join(deg_path, zip_name), "r")
        file_names = file_data.namelist()
        annotation = file_data.open(file_names[2], 'r')  # degannotation
        seq = file_data.open(file_names[0], 'r')  # degaa
        next(annotation)
        result = reconstruct_deg(annotation, seq, zip_name.replace('.zip', ''))
        write_to_deg_split(result, deg_split_path)
    pass


def reconstruct_deg(annotation, seq, name):
    anno_infos = list()
    for anno_line in annotation:
        anno_line = anno_line.decode('utf-8').split('\t')
        organ_name = anno_line[8] if anno_line[7][:3] == 'NC_' else anno_line[7]
        anno_infos.append([anno_line[1], organ_name])
    seq_infos = list()
    for seq_line in seq:
        seq_line = seq_line.decode('utf-8').replace('\n', '')
        if len(seq_line) > 0 and seq_line[0] == '>':
            seq_infos.append(list((seq_line[1:], str())))
        else:
            seq_infos[-1][-1] = seq_infos[-1][-1]+seq_line
    assert(len(anno_infos)==len(seq_infos))

    result={}
    for index in range(len(anno_infos)):
        pass
    return result


def write_to_deg_split(result, path):
    pass


def main():
    deg_split(global_config.PATH_LIST['DEG'],
              global_config.PATH_LIST['DEG_split'])
    pass


if __name__ == '__main__':
    main()
