import os
import shutil
import click
import defense_finder_viz

@click.command()
@click.option('-c', '--contig-file', 'contig', type=click.Path(exists=True), required=True, help='Prodigal\'s input file')
@click.option('-m', '--mrna-file', 'mrna', type=click.Path(exists=True), required=True, help='Prodigal\'s `-d` output file')
@click.option('-g', '--genes-file', 'genes', type=click.Path(exists=True), required=True, help='Defense Finder defense_finder_genes.tsv output')
@click.option('-s', '--systems-file', 'systems', type=click.Path(exists=True), required=True, help='Defense Finder defense_finder_systems.tsv output')
@click.option('-o', '--out-dir', 'outdir', type=click.Path(exists=True), help='The target directory where to store the results. Defaults to the current directory.')
def run(contig, mrna, genes, systems, outdir):
    """
    """
    default_outdir = os.getcwd()
    outdir = outdir if outdir != None else default_outdir
    defense_finder_viz.run(contig, mrna, genes, systems, outdir)
