# Copyright 2018 The KaiJIN Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""AFFINE TRANSFORM

"""
from typing import Sequence
import math
import random
import cv2
import numpy as np
import torch
import torchvision.transforms.functional as tvf
import torchvision.transforms as tvt
import kornia
import PIL

from tw import transform as T
from tw import logger


#!<----------------------------------------------------------------------------
#!< VFLIP
#!<----------------------------------------------------------------------------

def _vflip_np(inputs):
  return np.ascontiguousarray(inputs[::-1, ...])


@T.MetaWrapper(support=[T.ImageMeta, T.VideoMeta, T.BoxListMeta, T.KpsListMeta])
def _vflip_meta(metas: Sequence[T.MetaBase], **kwargs):

  for meta in metas:

    if isinstance(meta, T.ImageMeta):
      meta.bin = np.ascontiguousarray(meta.bin[::-1, ...])

    if isinstance(meta, T.VideoMeta):
      meta.bin = np.ascontiguousarray(meta.bin[:, ::-1, ...])

    if isinstance(meta, T.BoxListMeta):
      assert meta.is_affine_size
      x1, y1 = meta.bboxes[..., 0], meta.bboxes[..., 1]
      x2, y2 = meta.bboxes[..., 2], meta.bboxes[..., 3]
      meta.bboxes = np.stack([x1, meta.max_y - y2, x2, meta.max_y - y1], axis=1)

    if isinstance(meta, T.KpsListMeta):
      assert meta.is_affine_size
      x, y = meta.keypoints[..., 0], meta.keypoints[..., 1]
      meta.keypoints = np.stack([x, meta.max_y - y], axis=1)

  return metas


def vflip(inputs, **kwargs):
  if T.IsNumpy(inputs):
    return _vflip_np(inputs)
  elif T.IsMeta(inputs):
    return _vflip_meta(inputs, **kwargs)
  elif T.IsTensor(inputs):
    if inputs.ndim == 4:
      return torch.flip(inputs, dims=(2, ))
    elif inputs.ndim == 3:
      return torch.flip(inputs, dims=(1, ))
    else:
      raise NotImplementedError(inputs.ndim)
  elif T.IsPilImage(inputs):
    return tvt.functional.vflip(inputs)

#!<----------------------------------------------------------------------------
#!< HFLIP
#!<----------------------------------------------------------------------------


def _hflip_np(inputs):
  return np.ascontiguousarray(inputs[:, ::-1, ...])


@T.MetaWrapper(support=[T.ImageMeta, T.BoxListMeta, T.VideoMeta, T.KpsListMeta])
def _hflip_meta(metas: Sequence[T.MetaBase], **kwargs):

  for meta in metas:

    if isinstance(meta, T.ImageMeta):
      meta.bin = np.ascontiguousarray(meta.bin[:, ::-1, ...])

    if isinstance(meta, T.BoxListMeta):
      assert meta.is_affine_size
      x1, y1 = meta.bboxes[..., 0], meta.bboxes[..., 1]
      x2, y2 = meta.bboxes[..., 2], meta.bboxes[..., 3]
      meta.bboxes = np.stack([meta.max_x - x2, y1, meta.max_x - x1, y2], axis=1)

    if isinstance(meta, T.VideoMeta):
      meta.bin = np.ascontiguousarray(meta.bin[:, :, ::-1, ...])

    if isinstance(meta, T.KpsListMeta):
      assert meta.is_affine_size
      x, y = meta.keypoints[..., 0], meta.keypoints[..., 1]
      meta.keypoints = np.stack([meta.max_x - x, y], axis=1)

  return metas


def hflip(inputs, **kwargs):
  if T.IsNumpy(inputs):
    return _hflip_np(inputs)
  elif T.IsMeta(inputs):
    return _hflip_meta(inputs, **kwargs)
  elif T.IsTensor(inputs):
    if inputs.ndim == 4:
      return torch.flip(inputs, dims=(3, ))
    elif inputs.ndim == 3:
      return torch.flip(inputs, dims=(2, ))
    else:
      raise NotImplementedError(inputs.ndim)
  elif T.IsPilImage(inputs):
    return tvt.functional.hflip(inputs)

#!<----------------------------------------------------------------------------
#!< RANDOM FLIP
#!<----------------------------------------------------------------------------


def random_vflip(inputs, p=0.5, **kwargs):
  """random vertical flip sample.

  Args:
    p (float): the possibility to flip

  """
  if random.random() > p:
    return vflip(inputs, **kwargs)
  return inputs


def random_hflip(inputs, p=0.5, **kwargs):
  """random horizontal flip sample.

  Args:
    p (float): the possibility to flip

  """
  if random.random() > p:
    return hflip(inputs)
  return inputs


#!<----------------------------------------------------------------------------
#!< ROTATE
#!<----------------------------------------------------------------------------


def _rotate_numpy(inputs, angle, interpolation=cv2.INTER_LINEAR, border_mode=cv2.BORDER_CONSTANT, border_value=0):
  scale = 1.0
  shift = (0, 0)
  height, width = inputs.shape[:2]
  matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, scale)
  matrix[0, 2] += shift[0]
  matrix[1, 2] += shift[1]
  cv2.warpAffine(inputs,
                 M=matrix,
                 dsize=(width, height),
                 dst=inputs,
                 flags=interpolation,
                 borderMode=border_mode,
                 borderValue=border_value)
  return inputs


@T.MetaWrapper(support=[T.ImageMeta, T.BoxListMeta, T.KpsListMeta])
def _rotate_meta(metas: Sequence[T.MetaBase], angle, interpolation=cv2.INTER_LINEAR,
                 border_mode=cv2.BORDER_CONSTANT, border_value=0, **kwargs):

  scale = 1.0
  shift = (0, 0)

  # params checking
  assert len(shift) == 2

  for meta in metas:
    if meta.source == T.COLORSPACE.HEATMAP:
      interpolation = cv2.INTER_NEAREST

    if isinstance(meta, T.ImageMeta):
      height, width = meta.bin.shape[:2]
      matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, scale)
      matrix[0, 2] += shift[0]
      matrix[1, 2] += shift[1]
      cv2.warpAffine(meta.bin,
                     M=matrix,
                     dsize=(width, height),
                     dst=meta.bin,
                     flags=interpolation,
                     borderMode=border_mode,
                     borderValue=border_value)

    if isinstance(meta, T.BoxListMeta):
      width, height = meta.max_x, meta.max_y
      center = (width / 2, height / 2)
      matrix = cv2.getRotationMatrix2D(center, angle, scale)
      matrix[0, 2] += shift[0]
      matrix[1, 2] += shift[1]

      bbox = np.stack([meta.bboxes[:, 0], meta.bboxes[:, 1],
                       meta.bboxes[:, 2], meta.bboxes[:, 1],
                       meta.bboxes[:, 0], meta.bboxes[:, 3],
                       meta.bboxes[:, 2], meta.bboxes[:, 3]], axis=1).reshape(-1, 2)
      bbox = cv2.transform(bbox[None], matrix).squeeze().reshape(-1, 8)
      meta.bboxes = np.stack([
          np.amin(bbox[..., ::2], axis=1),
          np.amin(bbox[..., 1::2], axis=1),
          np.amax(bbox[..., ::2], axis=1),
          np.amax(bbox[..., 1::2], axis=1),
      ], axis=1)

      if meta.visibility:
        meta.clip_with_affine_size()

    if isinstance(meta, T.KpsListMeta):
      width, height = meta.max_x, meta.max_y
      center = (width / 2, height / 2)
      matrix = cv2.getRotationMatrix2D(center, angle, scale)
      matrix[0, 2] += shift[0]  # * width
      matrix[1, 2] += shift[1]  # * height
      meta.keypoints = cv2.transform(meta.keypoints[None], matrix).squeeze()
      if meta.visibility:
        meta.clip_with_affine_size()

  return metas


def rotate(inputs, angle, interpolation=cv2.INTER_LINEAR, border_mode=cv2.BORDER_CONSTANT, border_value=0, **kwargs):
  """rotate

  Args:
      inputs ([type]): [description]
      angle (float): degree representation
      interpolation ([type], optional): [description]. Defaults to cv2.INTER_LINEAR.
      border_mode ([type], optional): [description]. Defaults to cv2.BORDER_CONSTANT.
      border_value (int, optional): [description]. Defaults to 0.

  Raises:
      NotImplementedError: [description]
      NotImplementedError: [description]
      NotImplementedError: [description]

  Returns:
      [type]: [description]
  """
  if T.IsNumpy(inputs):
    return _rotate_numpy(inputs, angle, interpolation, border_mode, border_value)
  elif T.IsMeta(inputs):
    return _rotate_meta(inputs, angle, interpolation, border_mode, border_value, **kwargs)
  elif T.IsTensor(inputs):
    assert border_value == 0
    assert inputs.ndim == 4
    return kornia.rotate(inputs, torch.tensor(angle).to(inputs.device), mode=T.INTER_CV_TO_TCH[interpolation])
  elif T.IsPilImage(inputs):
    raise NotImplementedError


def random_rotate(inputs, angle_limit=(-30, 30), interpolation=cv2.INTER_LINEAR,
                  border_mode=cv2.BORDER_CONSTANT, border_value=0, **kwargs):
  """rotate

  Args:
      inputs ([type]): [description]
      angle (float): degree representation
      interpolation ([type], optional): [description]. Defaults to cv2.INTER_LINEAR.
      border_mode ([type], optional): [description]. Defaults to cv2.BORDER_CONSTANT.
      border_value (int, optional): [description]. Defaults to 0.

  Raises:
      NotImplementedError: [description]
      NotImplementedError: [description]
      NotImplementedError: [description]

  Returns:
      [type]: [description]
  """

  angle = random.uniform(angle_limit[0], angle_limit[1])

  if T.IsNumpy(inputs):
    raise NotImplementedError
  elif T.IsMeta(inputs):
    return _rotate_meta(inputs, angle, interpolation, border_mode, border_value, **kwargs)
  elif T.IsTensor(inputs):
    raise NotImplementedError
  elif T.IsPilImage(inputs):
    raise NotImplementedError
