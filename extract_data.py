import global_config
import os
import zipfile
import shutil


def make_dir(director):
    director = director[:-1] if director[-1] == '/' else director
    if os.path.exists(director):
        shutil.rmtree(director)
    os.mkdir(director)


def deg_split(deg_path, deg_split_path):
    file_list = os.listdir(deg_path)
    make_dir(deg_split_path)
    for zip_name in file_list:
        file_data = zipfile.ZipFile(os.path.join(deg_path, zip_name), "r")
        file_names = file_data.namelist()
        annotation = file_data.open(file_names[2], 'r')  # degannotation
        seq = file_data.open(file_names[0], 'r')  # degaa
        next(annotation)
        result = reconstruct_deg(annotation, seq, zip_name.replace('.zip', ''))
        write_to_deg_split(result, deg_split_path)


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
    assert(len(anno_infos) == len(seq_infos))
    result = dict()
    for index in range(len(anno_infos)):
        assert anno_infos[index][0] == seq_infos[index][0]
        deg_name = anno_infos[index][1]
        if deg_name in global_config.ID_MAP.keys():  # 首先需要这个存在
            final_name = global_config.ID_MAP[deg_name][0]
            sequence = seq_infos[index][1]
            if final_name in result.keys():  # 染化需要合并
                result[final_name].append(sequence)
            else:
                result[final_name] = list([sequence])
    return result


def write_to_deg_split(organs_ess_seqs, path):
    for organ_name in organs_ess_seqs.keys():
        ess_seqs = organs_ess_seqs[organ_name]
        store_path = os.path.join(path, organ_name+'.txt')
        with open(store_path, 'wb') as file:
            for ess_seq in ess_seqs:
                temp = bytes(ess_seq+'\n', 'utf-8')
                file.write(temp)


def get_protein_ids(string_seq_path, ess_seq_path):
    pass


def main():
    # deg_split(global_config.PATH_LIST['DEG'], global_config.PATH_LIST['DEG_split'])
    Fusion_path = global_config.PATH_LIST['Fusion']
    make_dir(Fusion_path)
    for organ in global_config.get_organs().keys():
        organ_path = os.path.join(Fusion_path, organ)
        make_dir(organ_path)

    pass


if __name__ == '__main__':
    main()
