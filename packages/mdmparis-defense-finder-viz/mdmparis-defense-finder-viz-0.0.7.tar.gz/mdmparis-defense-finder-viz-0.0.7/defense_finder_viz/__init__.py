import pandas as pd
from Bio import SeqIO
import json
import os


def run(contig_path, mrna_path, df_genes_path, df_systems_path, outdir):
    neighborhood_margin = 5000  # how many nucleotides on each side of the system's core do you consider to be part of the "neighborhood"

    def get_genes(contig, start, end):
        if start <= end:
            mini_gene_df = genes_df[
                (genes_df.start > start) & (genes_df.end < end) & (genes_df.contig == contig)].copy()
        elif start > end:
            mini_gene_df = genes_df[((genes_df.start > start) | (genes_df.start < end)) & (
                        (genes_df.end > start) | (genes_df.end < end)) & (genes_df.contig == contig)].copy()

        mini_gene_df['role'] = DF_genes['hit_gene_ref'].str.replace('_', ' ')
        mini_gene_df['role'].fillna('non defensive', inplace=True)
        return mini_gene_df

    contigs = []
    contig_length = {}
    for record in SeqIO.parse(contig_path, "fasta"):
        contigs.append({"name": record.id, "length": len(record.seq), "description": record.description})
        contig_length[record.id] = len(record.seq)

    genes = {}
    for record in SeqIO.parse(mrna_path, "fasta"):
        [id, start, end, strand, _] = record.description.split(' # ')
        contig = "_".join(id.split('_')[:-1])
        start = int(start)
        end = int(end)
        strand = int(strand)
        genes[id] = {'start':start, 'end':end, 'strand':strand,'contig':contig}

    contigsOutpath = os.path.join(outdir, 'dfviz_contigs.json')
    with open(contigsOutpath, "w") as outfile:
        json.dump(contigs, outfile)

    genes_df = pd.DataFrame(genes).T

    DF_genes = pd.read_csv(df_genes_path, sep='\t', index_col="hit_id")
    systems_df = pd.read_csv(df_systems_path, sep='\t')

    systems_df['core_start'] = systems_df.sys_beg.map(lambda x: genes.get(x).get('start'))
    systems_df['core_end'] = systems_df.sys_end.map(lambda x: genes.get(x).get('end'))
    systems_df['contig'] = systems_df.sys_beg.map(lambda x: "_".join(x.split('_')[:-1]))

    systems_df['contig_length'] = systems_df.contig.map(contig_length)
    systems_df['neighborhood_start'] = (systems_df.core_start - neighborhood_margin) % systems_df.contig_length
    systems_df['neighborhood_end'] = (systems_df.core_end + neighborhood_margin) % systems_df.contig_length

    dirname = os.path.dirname(__file__)
    palette_path = os.path.join(dirname, 'systems_palette.csv')
    DF_colors = pd.read_csv(palette_path)

    systems_df = systems_df.merge(DF_colors[['system_type', 'hex_code_rainbow']], left_on='subtype',
                                  right_on='system_type')

    systems = systems_df.to_dict(orient='records')

    for sys in systems:
        sys['genes'] = get_genes(sys['contig'], sys['neighborhood_start'], sys['neighborhood_end']).to_dict(
            orient='records')

    systemsOutpath = os.path.join(outdir, 'dfviz_systems.json')
    with open(systemsOutpath, "w") as outfile:
        json.dump(systems, outfile)
