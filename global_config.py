'''
设置全局的配置文件，比如下载地址，运行环境等等
'''
import os
DATA_ROOT = os.path.join('Data')
PATH_LIST = {
    'DEG': os.path.join(DATA_ROOT, 'DEG'),
    'STRING': os.path.join(DATA_ROOT, 'STRING'),
    'UNIPROT': os.path.join(DATA_ROOT, 'UNIPROT'),
    'DEG_split': os.path.join(DATA_ROOT, 'DEG_split'),
    'Fusion': os.path.join(DATA_ROOT, 'Fusion'),
    'driver': os.path.join(DATA_ROOT, 'Support', 'chromedriver')
}
DEG_BIO_CLASS = ['Bacteria', 'Archaea', 'Eukaryotes']
STRING_FILES = ['protein_actions', 'protein_info', 'protein_sequences']

ID_MAP = {
    'Acinetobacter baumannii ATCC 17978': '470',
    'Acinetobacter baylyi ADP1': '62977',
    'Agrobacterium f': '176299',
    'Arabidopsis thaliana': '3702',
    'Aspergillus fumigatus': '746128',
    'Bacillus subtilis 168': '224308',
    'Bacteroides thetaiotaomicron VPI-5482': '226186',
    'Brevundimonas subvibrioides ATCC 15264': '633149',
    'Burkholderia pseudomallei K96243': '272560',
    'Caenorhabditis elegans': '6239',
    'Campylobacter jejuni subsp. jejuni 81-176': '354242',
    'Campylobacter jejuni subsp. jejuni NCTC 11168 = ATCC 700819': '192222',
    'Danio rerio': '7955',
    'Drosophila melanogaster': '7227',
    'Escherichia coli MG1655 I': '511145',
    'Escherichia coli MG1655 II': '511145',
    'Haemophilus influenzae Rd KW20': '71421',
    'Helicobacter pylori 26695': '85962',
    'Homo sapiens': '9606',
    'Methanococcus maripaludis S2': '267377',
    'Mus musculus': '10090',
    'Mycobacterium tuberculosis H37Rv': '83332',
    'Mycobacterium tuberculosis H37Rv II': '83332',
    'Mycobacterium tuberculosis H37Rv III': '83332',
    'Mycoplasma genitalium G37': '243273',
    'Mycoplasma pulmonis UAB CTIP': '272635',
    'Porphyromonas gingivalis ATCC 33277': '431947',
    'Pseudomonas aeruginosa PAO1': '287',
    'Pseudomonas aeruginosa UCBPP-PA14': '287',
    'Rhodopseudomonas palustris CGA009': '258594',
    'Saccharomyces cerevisiae': '4932',
    'Schizosaccharomyces pombe 972h-': '4896',
    'Shewanella oneidensis MR-1': '211586',
    'Sphingomonas wittichii RW1': '392499',
    'Staphylococcus aureus N315': '1280',
    'Staphylococcus aureus NCTC 8325': '1280',
    'Streptococcus pyogenes MGAS5448': '1314',
    'Streptococcus pyogenes NZ131': '1314',
    'Streptococcus sanguinis': '388919',
    'Synechococcus elongatus PCC 7942': '1140',
    'Synechococcus elongatus PCC 7942 plasmid 1': '1140',
    'Vibrio cholerae N16961': '243277'
}

if __name__ == '__main__':
    print(len(ID_MAP))
