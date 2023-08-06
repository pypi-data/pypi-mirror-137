'''
Date: 2022.02.05 16:55
Description: Omit
LastEditors: Rustle Karl
LastEditTime: 2022.02.05 16:55
'''
import click

from .vhd import FixedVHDWriter


@click.command('Fixed VHD Writer')
@click.option('--vhd_file', '-v', required=True, type=str, help='specify .vhd file to write')
@click.option('--bin_file', '-b', type=str, help='specify .bin file to read')
@click.option('--sector_offset', '-o', type=int, default=0, help='specify sector offset to write')
@click.option('--show_geometry', '-s', type=bool, default=False, help='show information about specify .vhd file')
def fixed_vhd_writer(bin_file, vhd_file, sector_offset, show_geometry):
    vhd = FixedVHDWriter(vhd_file)

    if show_geometry:
        click.echo(vhd.geometry)
        return

    if bin_file:
        vhd.write_from_binary_file(bin_file, sector_offset)
