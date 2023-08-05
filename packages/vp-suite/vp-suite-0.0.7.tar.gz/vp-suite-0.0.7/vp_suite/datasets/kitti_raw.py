import random
from pathlib import Path

import cv2
import numpy as np
import torch

from vp_suite.base.base_dataset import VPDataset, VPData
import vp_suite.constants as constants
from vp_suite.utils.utils import set_from_kwarg


class KITTIRawDataset(VPDataset):
    r"""

    """
    NAME = "KITTI raw"
    DEFAULT_DATA_DIR = constants.DATA_PATH / "kitti_raw"
    VALID_SPLITS = ["train", "val", "test"]
    MIN_SEQ_LEN = 994  #: Minimum number of frames across all sequences (6349 in longest)
    ACTION_SIZE = 0  #: No actions given
    DATASET_FRAME_SHAPE = (375, 1242, 3)
    FPS = 10  #: TODO
    AVAILABLE_CAMERAS = [f"image_{i:02d}" for i in range(4)]  #: cameras: [greyscale_left, greyscale_right, color_left, color_right]

    camera = "image_02"  #: TODO
    trainval_to_test_ratio = 0.8  #: TODO
    train_to_val_ratio = 0.9  #: big dataset -> val can be smaller
    trainval_test_seed = 1612  #: The seed to separate training data from test data; Taken from the Noether Networks code
    train_val_seed = 1234  #: The seed to separate training/validation data from the previously split training data

    def __init__(self, split, **dataset_kwargs):
        r"""

        Args:
            split ():
            **dataset_kwargs ():
        """
        super(KITTIRawDataset, self).__init__(split, **dataset_kwargs)
        self.NON_CONFIG_VARS.extend(["sequences", "sequences_with_frame_index",
                                     "AVAILABLE_CAMERAS"])

        # set attributes
        set_from_kwarg(self, "camera", self.camera, dataset_kwargs)
        set_from_kwarg(self, "trainval_to_test_ratio", self.trainval_to_test_ratio, dataset_kwargs)
        set_from_kwarg(self, "train_to_val_ratio", self.train_to_val_ratio, dataset_kwargs)
        set_from_kwarg(self, "trainval_test_seed", self.trainval_test_seed, dataset_kwargs)
        set_from_kwarg(self, "train_val_seed", self.train_val_seed, dataset_kwargs)

        # get video filepaths
        dd = Path(self.data_dir)
        sequence_dirs = [sub for d in dd.iterdir() for sub in d.iterdir() if dd.is_dir() and sub.is_dir()]
        if len(sequence_dirs) < 3:
            raise ValueError(f"Dataset {self.NAME}: found less than 3 sequences "
                             f"-> can't split dataset -> can't use it")

        # slice accordingly
        slice_idx = max(1, int(len(sequence_dirs) * self.trainval_to_test_ratio))
        random.Random(self.train_val_seed).shuffle(sequence_dirs)
        if self.split == "test":
            sequence_dirs = sequence_dirs[slice_idx:]
        else:
            sequence_dirs = sequence_dirs[:slice_idx]
            slice_idx = max(1, int(len(sequence_dirs) * self.train_to_val_ratio))
            if self.split == "train":
                sequence_dirs = sequence_dirs[:slice_idx]
            else:
                sequence_dirs = sequence_dirs[slice_idx:]

        # retrieve sequence lengths and store
        self.sequences = []
        for sequence_dir in sorted(sequence_dirs):
            sequence_len = len(list(sequence_dir.rglob(f"{self.camera}/data/*.png")))
            self.sequences.append((sequence_dir, sequence_len))

        self.sequences_with_frame_index = []  # mock value, must not be used for iteration till sequence length is set

    def _set_seq_len(self):
        r"""
        Determine per video which frame indices are valid

        Returns:

        """
        for sequence_path, frame_count in self.sequences:
            valid_start_idx = range(0, frame_count - self.seq_len + 1,
                                    self.seq_len + self.seq_step - 1)
            for idx in valid_start_idx:
                self.sequences_with_frame_index.append((sequence_path, idx))

    def __getitem__(self, i) -> VPData:
        r"""

        Args:
            i ():

        Returns:

        """
        sequence_path, start_idx = self.sequences_with_frame_index[i]
        all_img_paths = sorted(list(sequence_path.rglob(f"{self.camera}/data/*.png")))
        seq_img_paths = all_img_paths[start_idx:start_idx+self.seq_len:self.seq_step]  # t items of [h, w, c]
        seq_imgs = [cv2.cvtColor(cv2.imread(str(fp.resolve())), cv2.COLOR_BGR2RGB) for fp in seq_img_paths]
        vid = np.stack(seq_imgs, axis=0)  # [t, *self.DATASET_FRAME_SHAPE]
        vid = self.preprocess(vid)  # [t, *self.img_shape]
        actions = torch.zeros((self.total_frames, 1))  # [t, a], actions should be disregarded in training logic

        data = {"frames": vid, "actions": actions}
        return data

    def __len__(self):
        r"""

        Returns:

        """
        return len(self.sequences_with_frame_index)

    @classmethod
    def download_and_prepare_dataset(cls):
        r"""

        Returns:

        """
        d_path = cls.DEFAULT_DATA_DIR
        d_path.mkdir(parents=True, exist_ok=True)

        # download and extract sequences if we can't find them in our folder yet
        try:
            _ = next(d_path.rglob(f"**/*.png"))
            print(f"Found image data in {str(d_path.resolve())} -> Won't download {cls.NAME}")
        except StopIteration:
            from vp_suite.utils.utils import run_shell_command
            import vp_suite.constants as constants
            prep_script = (constants.PKG_RESOURCES / 'get_dataset_kitti_raw.sh').resolve()
            run_shell_command(f"{prep_script} {cls.DEFAULT_DATA_DIR}")
