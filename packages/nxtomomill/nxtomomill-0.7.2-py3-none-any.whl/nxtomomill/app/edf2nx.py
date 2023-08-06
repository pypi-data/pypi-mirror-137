# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2015-2020 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/

"""
Application to convert a tomo dataset written in edf into and hdf5/nexus file.

.. code-block:: bash

    usage: nxtomomill edf2nx [-h] [--file_extension] [--motor_pos_key MOTOR_POS_KEY] [--motor_mne_key MOTOR_MNE_KEY] [--refs_name_keys REFS_NAME_KEYS] [--ignore_file_containing IGNORE_FILE_CONTAINING]
                             [--rot_angle_key ROT_ANGLE_KEY] [--dark_names DARK_NAMES] [--x_trans_key X_TRANS_KEY] [--y_trans_key Y_TRANS_KEY] [--z_trans_key Z_TRANS_KEY]
                             scan_path output_file

    convert data acquired as edf to hdf5 - nexus compliant file format.

    positional arguments:
      scan_path             folder containing the edf files
      output_file           foutput .h5 file

    optional arguments:
      -h, --help            show this help message and exit
      --file_extension      extension of the output file. Valid values are .h5/.hdf5/.nx
      --motor_pos_key MOTOR_POS_KEY
                            motor position key in EDF HEADER
      --motor_mne_key MOTOR_MNE_KEY
                            motor mne key in EDF HEADER
      --refs_name_keys REFS_NAME_KEYS
                            prefix of flat field file
      --ignore_file_containing IGNORE_FILE_CONTAINING
                            substring that lead to ignoring the file if contained in the name
      --rot_angle_key ROT_ANGLE_KEY
                            rotation angle key in EDF HEADER
      --dark_names DARK_NAMES
                            prefix of the dark field file
      --x_trans_key X_TRANS_KEY
                            x translation key in EDF HEADER
      --y_trans_key Y_TRANS_KEY
                            y translation key in EDF HEADER
      --z_trans_key Z_TRANS_KEY
                            z translation key in EDF HEADER
"""

__authors__ = ["C. Nemoz", "H. Payno", "A.Sole"]
__license__ = "MIT"
__date__ = "16/01/2020"


import argparse
import logging

from nxtomomill.converter.hdf5.acquisition.baseacquisition import SourceType
from nxtomomill import utils
from nxtomomill import converter
from nxtomomill.utils import Progress
from nxtomomill.settings import Tomo
from tomoscan.esrf.edfscan import EDFTomoScan

EDF_MOTOR_POS = Tomo.EDF.MOTOR_POS
EDF_MOTOR_MNE = Tomo.EDF.MOTOR_MNE
EDF_REFS_NAMES = Tomo.EDF.REFS_NAMES
EDF_TO_IGNORE = Tomo.EDF.TO_IGNORE
EDF_ROT_ANGLE = Tomo.EDF.ROT_ANGLE
EDF_DARK_NAMES = Tomo.EDF.DARK_NAMES
EDF_X_TRANS = Tomo.EDF.X_TRANS
EDF_Y_TRANS = Tomo.EDF.Y_TRANS
EDF_Z_TRANS = Tomo.EDF.Z_TRANS

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


def main(argv):
    """ """
    parser = argparse.ArgumentParser(
        description="convert data acquired as "
        "edf to hdf5 - nexus "
        "compliant file format."
    )
    parser.add_argument("scan_path", help="folder containing the edf files")
    parser.add_argument("output_file", help="foutput .h5 file")
    parser.add_argument(
        "--file_extension",
        action="store_true",
        default=".h5",
        help="extension of the output file. Valid values are "
        "" + "/".join(utils.FileExtension.values()),
    )
    parser.add_argument(
        "--motor_pos_key",
        default=EDF_MOTOR_POS,
        help="motor position key in EDF HEADER",
    )
    parser.add_argument(
        "--motor_mne_key", default=EDF_MOTOR_MNE, help="motor mne key in EDF HEADER"
    )
    parser.add_argument(
        "--refs_name_keys",
        default=",".join(EDF_REFS_NAMES),
        help="prefix of flat field file",
    )
    parser.add_argument(
        "--ignore_file_containing",
        default=",".join(EDF_TO_IGNORE),
        help="substring that lead to ignoring the file if " "contained in the name",
    )
    parser.add_argument(
        "--rot_angle_key",
        default=EDF_ROT_ANGLE,
        help="rotation angle key in EDF HEADER",
    )
    parser.add_argument(
        "--dark_names",
        default=",".join(EDF_DARK_NAMES),
        help="prefix of the dark field file",
    )
    parser.add_argument(
        "--x_trans_key", default=EDF_X_TRANS, help="x translation key in EDF HEADER"
    )
    parser.add_argument(
        "--y_trans_key", default=EDF_Y_TRANS, help="y translation key in EDF HEADER"
    )
    parser.add_argument(
        "--z_trans_key", default=EDF_Z_TRANS, help="z translation key in EDF HEADER"
    )
    parser.add_argument("--sample_name", default=None, help="name of the sample")
    parser.add_argument("--title", default=None, help="title")
    parser.add_argument("--instrument_name", default=None, help="instrument name used")
    parser.add_argument("--source_name", default="ESRF", help="name of the source used")
    parser.add_argument(
        "--source_type",
        default=SourceType.SYNCHROTRON_X_RAY_SOURCE,
        help="type of the source used",
    )

    options = parser.parse_args(argv[1:])

    conv = utils.get_tuple_of_keys_from_cmd
    file_keys = converter.EDFFileKeys(
        motor_mne_key=options.motor_mne_key,
        motor_pos_key=options.motor_pos_key,
        ref_names=conv(options.refs_name_keys),
        to_ignore=conv(options.ignore_file_containing),
        rot_angle_key=options.rot_angle_key,
        dark_names=conv(options.dark_names),
        x_trans_key=options.x_trans_key,
        y_trans_key=options.y_trans_key,
        z_trans_key=options.z_trans_key,
    )

    input_dir = options.scan_path
    scan = EDFTomoScan(input_dir)
    converter.edf_to_nx(
        scan=scan,
        output_file=options.output_file,
        file_extension=options.file_extension,
        file_keys=file_keys,
        progress=Progress(""),
        sample_name=options.sample_name,
        title=options.title,
        instrument_name=options.instrument_name,
        source_name=options.source_name,
        source_type=options.source_type,
    )


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
