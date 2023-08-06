"""ocmr dataset."""

import ast
import pathlib

import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_datasets as tfds

from mri_datasets.ocmr import ocmr_reader


_DESCRIPTION = """
This is the *Open-Access Multi-Coil k-Space Dataset for Cardiovascular Magnetic
Resonance Imaging* (OCMR) dataset.

This dataset contains all the unmodified, fully sampled data from the original
dataset (74 examples) and all relevant metadata, in TFRecord format.

This dataset does not include the undersampled data from the original dataset.
"""

_CITATION = """
@misc{chen2020ocmr,
      title={OCMR (v1.0)--Open-Access Multi-Coil k-Space Dataset for Cardiovascular Magnetic Resonance Imaging}, 
      author={Chong Chen and Yingmin Liu and Philip Schniter and Matthew Tong and Karolina Zareba and Orlando Simonetti and Lee Potter and Rizwan Ahmad},
      year={2020},
      eprint={2008.03410},
      archivePrefix={arXiv},
      primaryClass={eess.IV}
}
"""

_DOWNLOAD_URL = "https://ocmr.s3.amazonaws.com/data/ocmr_cine.tar.gz"


class Ocmr(tfds.core.GeneratorBasedBuilder):
  """DatasetBuilder for ocmr dataset."""

  VERSION = tfds.core.Version('1.0.0')
  RELEASE_NOTES = {
      '1.0.0': 'Initial release.',
  }

  def _info(self) -> tfds.core.DatasetInfo:
    """Returns the dataset metadata."""
    return tfds.core.DatasetInfo(
        builder=self,
        description=_DESCRIPTION,
        features=tfds.features.FeaturesDict({
            'kspace': tfds.features.Tensor(
                shape=(None,) * 8,
                dtype=tf.dtypes.complex64,
                encoding=tfds.features.Encoding.BYTES),
            'metadata': {
                'readout_fov': tf.float32,
                'phase_fov': tf.float32,
                'slice_thickness': tf.float32,
                'te': tf.float32,
                'ti': tf.float32,
                'tr': tf.float32,
                'echo_spacing': tf.float32,
                'flip_angle': tf.float32,
                'sequence_type': tf.string,
                'manufacturer': tf.string,
                'manufacturer_model_name': tf.string,
                'magnetic_field_strength': tf.float32,
                'sampling_type': tf.string,
                'asymmetric_echo': tf.string,
                'cardiac_orientation': tf.string,
                'spatial_aliasing': tf.string,
                'subject_type': tf.string,
                'ocmr_id': tf.string,
                'num_slices': tf.int32,
                'slice_index': tf.int32
            }
        }),
        supervised_keys=None,
        homepage='https://ocmr.info/',
        citation=_CITATION
    )

  def _split_generators(self, dl_manager: tfds.download.DownloadManager):
    """Returns SplitGenerators."""
    path = dl_manager.download_and_extract(_DOWNLOAD_URL)
    return {
        'train': self._generate_examples(path)
    }

  def _generate_examples(self, path):
    """Yields examples.

    Args:
      path: Path to extracted data.

    Yields:
      tuple(str, dict): (example id, example). Each example contains a k-space
        tensor and a metadata dictionary.

    Raises:
      ValueError: If `kspace` slice is too large (> 2 GB).
    """
    # Read OCMR data attributes and clean up empty rows and columns.
    df = pd.read_csv(pathlib.Path(__file__).parent / 'ocmr_data_attributes.csv')
    df.dropna(how='all', axis=0, inplace=True)
    df.dropna(how='all', axis=1, inplace=True)
    # Keep only fully sampled examples.
    df = df.loc[df.smp == 'fs']

    for _, attrs in df.iterrows():
      # Get the filename.
      filename = path / 'OCMR_data' / attrs['file name']

      # Read OCMR data.
      kspace, meta = ocmr_reader.read(filename)
      meta = _parse_meta(meta)
      meta.update(_parse_attrs(attrs))
      meta['ocmr_id'] = filename.stem

      # Split kspace into slices.
      slice_axis = 6
      num_slices = kspace.shape[slice_axis]
      kspace_slices = np.split(kspace, num_slices, axis=slice_axis)
      meta['num_slices'] = num_slices

      for slice_index, kspace in enumerate(kspace_slices):

        # Remove slice axis.
        kspace = np.squeeze(kspace, axis=slice_axis)

        if kspace.nbytes >= _MAX_PROTOBUF_SIZE:
          raise ValueError("`kspace` too large for serialization.")

        meta['slice_index'] = slice_index
        yield filename.stem + f'_slc{slice_index:03}', {
            'kspace': kspace,
            'metadata': meta
        }


_MAX_PROTOBUF_SIZE = 2 ** 31 - 1  # 2 GB


def _parse_meta(meta):
  """Parse metadata from OCMR files.

  Args:
    meta: Example metadata as returned by the OCMR reader.

  Returns:
    A metadata dictionary ready for serialization.
  """
  # Process metadata.
  assert len(meta['FOV']) == 3
  readout_fov = meta['FOV'][0]
  phase_fov = meta['FOV'][1]
  slice_thickness = meta['FOV'][2]
  tr = ast.literal_eval(meta['TRes'])
  assert len(tr) == 1
  tr = tr[0]
  te = ast.literal_eval(meta['TE'])
  assert len(te) == 1
  te = te[0]
  ti = ast.literal_eval(meta['TI'])
  assert len(ti) == 1
  ti = ti[0]
  echo_spacing = ast.literal_eval(meta['echo_spacing'])
  assert len(echo_spacing) == 1
  echo_spacing = echo_spacing[0]
  flip_angle = ast.literal_eval(meta['flipAngle_deg'])
  assert len(flip_angle) == 1
  flip_angle = flip_angle[0]
  sequence_type = meta['sequence_type'].lower()

  return {
      'readout_fov': readout_fov,
      'phase_fov': phase_fov,
      'slice_thickness': slice_thickness,
      'te': te,
      'ti': ti,
      'tr': tr,
      'echo_spacing': echo_spacing,
      'flip_angle': flip_angle,
      'sequence_type': sequence_type
  }


def _parse_attrs(df):
  """Parse OCMR attributes.

  Args:
    df: Dataframe with attributes.

  Returns:
    A metadata dictionary ready for serialization.
  """
  manufacturer = 'siemens'
  manufacturer_model_name_map = {
      'avan': 'avanto',
      'pris': 'prisma',
      'sola': 'sola'}
  manufacturer_model_name = manufacturer_model_name_map[df.scn[2:]]
  magnetic_field_strength_map = {'15': 1.5, '30': 3.0}
  magnetic_field_strength = magnetic_field_strength_map[df.scn[:2]]
  sampling_type_map = {'fs': 'fully_sampled'}
  sampling_type = sampling_type_map[df.smp]
  asymmetric_echo_map = {'asy': 'yes', 'sym': 'no'}
  asymmetric_echo = asymmetric_echo_map[df.ech]
  cardiac_orientation_map = {'sax': 'short_axis', 'lax': 'long_axis'}
  cardiac_orientation = cardiac_orientation_map[df.viw]
  spatial_aliasing_map = {'ali': 'yes', 'noa': 'no'}
  spatial_aliasing = spatial_aliasing_map[df.fov]
  subject_type_map = {'vol': 'healthy_volunteer', 'pat': 'patient'}
  subject_type = subject_type_map[df['sub']]

  return {
      'manufacturer': manufacturer,
      'manufacturer_model_name': manufacturer_model_name,
      'magnetic_field_strength': magnetic_field_strength,
      'sampling_type': sampling_type,
      'asymmetric_echo': asymmetric_echo,
      'cardiac_orientation': cardiac_orientation,
      'spatial_aliasing': spatial_aliasing,
      'subject_type': subject_type
  }
