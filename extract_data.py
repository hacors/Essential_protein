import global_config
import os
import zipfile
import shutil
import zipfile
import gzip
import networkx as nx


def deg_split(deg_origin_path, deg_split_path):  # 将deg数据集的有效数据提取出来
    os.makedirs(deg_split_path, exist_ok=True)
    file_list = os.listdir(deg_origin_path)
    for zip_name in file_list:
        file_data = zipfile.ZipFile(
            os.path.join(deg_origin_path, zip_name), "r")
        file_names = file_data.namelist()
        annotation = file_data.open(file_names[2], 'r')  # degannotation
        seq = file_data.open(file_names[0], 'r')  # degaa
        next(annotation)
        result = reconstruct_deg(annotation, seq)  # 整理结果
        write_to_deg_split(result, deg_split_path)  # 存储结果


def reconstruct_deg(annotation, seq):
    anno_infos = list()
    for anno_line in annotation:
        anno_line = anno_line.decode('utf-8').split('\t')
        deg_id = anno_line[1]
        organ_name = anno_line[8] if anno_line[7][:3] == 'NC_' else anno_line[7]
        anno_infos.append([deg_id, organ_name])
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
        deg_name = anno_infos[index][-1]
        if deg_name in global_config.ID_MAP.keys():  # 首先需要这个存在
            final_name = global_config.ID_MAP[deg_name]
            sequence = seq_infos[index][-1]
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


def get_ess_ids(string_seq_path, deg_seq_path):
    deg_seq_file = open(deg_seq_path)
    deg_seq = deg_seq_file.read().split('\n')
    string_seq_file = gzip.open(string_seq_path)
    string_seq_decode = string_seq_file.read().decode('utf-8')
    string_seq_split = string_seq_decode.split('>')
    string_seq_split.remove('')
    result = list()
    for string_seq_line in string_seq_split:
        string_seq_processed = string_seq_line.replace(
            '\n', ' ', 1).replace('\n', '').split()
        if string_seq_processed[1] in deg_seq:
            result.append(string_seq_processed[0])
    rate = len(result)/len(deg_seq)
    return result, rate


def main():
    '''
    deg_split(global_config.PATH_LIST['DEG'],
              global_config.PATH_LIST['DEG_split'])
    '''
    Fusion_path = global_config.PATH_LIST['Fusion']
    String_path = global_config.PATH_LIST['STRING']
    Deg_split_path = global_config.PATH_LIST['DEG_split']
    Uniprot_path = global_config.PATH_LIST['UNIPROT']
    os.makedirs(Fusion_path, exist_ok=True)
    for organ in global_config.ID_MAP.values():
        organ_path = os.path.join(Fusion_path, organ)
        os.makedirs(organ_path, exist_ok=True)

        ess_ids, rate = get_ess_ids(os.path.join(
            String_path, organ, 'protein_sequences.txt.gz'), os.path.join(Deg_split_path, organ+'.txt'))
        if rate > 0.80:
            init_graph = nx.MultiGraph()

        pass


if __name__ == '__main__':
    main()
