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
import numpy as np
from .base import Evaluator


class RegressionEvaluator(Evaluator):
  def __init__(self, root=None):
    super(RegressionEvaluator, self).__init__(root=root)

  def accumulate(self):
    r"""unzip each tuple. compute mae and rmse.
      metric layout: [preds, targets, (paths)]
    """
    total = []
    for batch in self.metrics:
      for content in zip(*batch):
        total.append(content)

    preds = []
    targets = []
    if self.root is not None:
      path = self.root + '/result.txt'
      with open(path, 'w') as fw:
        for res in total:
          pred = res[0].cpu().item()
          target = res[1].cpu().item()
          preds.append(pred)
          targets.append(target)
          fw.write('{} {} {}\n'.format(res[2], target, pred))

    preds = np.array(preds)
    targets = np.array(targets)
    error = preds - targets
    mae = np.mean(np.abs(error))
    rmse = np.sqrt(np.mean(error * error))

    return {'mae': mae, 'rmse': rmse}
