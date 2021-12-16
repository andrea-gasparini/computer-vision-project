from typing import List, Optional, Union
from torch.utils.data import DataLoader
from src.data.datasets import RacingF1Dataset
from torchvision.transforms import Compose
from src.utils import join_dirs

import pytorch_lightning as pl

class RacingF1DataModule(pl.LightningDataModule):

    def __init__(self, batch_size: int, dataset_dir: str,
                       val_subdirs: List[str]   = ["racing-10", "racing-11"],
                       train_subdirs: List[str] = ["racing-1", "racing-7",
                                                   "racing-9", "racing-20"],
                       test_subdirs: List[str]  = ["racing-12"],
                       data_transform: Optional[Compose] = None):

        super().__init__()
        self.batch_size = batch_size
        self.dataset_dir = dataset_dir
        self.train_dirs = join_dirs(self.dataset_dir, train_subdirs)
        self.val_dirs = join_dirs(self.dataset_dir, val_subdirs)
        self.test_dirs = join_dirs(self.dataset_dir, test_subdirs)
        self.data_transform = data_transform

    # def prepare_data(self, *args, **kwargs):
    # 	raise NotImplementedError


    def setup(self, stage: Optional[str] = None) -> None:
        if stage == 'fit' or stage is None:
            self.train_dataset = RacingF1Dataset(self.train_dirs, self.data_transform)
            self.val_dataset = RacingF1Dataset(self.val_dirs, self.data_transform)
        
        if stage == 'test' or stage is None:
            self.test_set = RacingF1Dataset(self.test_dirs, self.data_transform)


    def train_dataloader(self) -> DataLoader:
        return DataLoader(self.train_dataset, batch_size=self.batch_size)


    def val_dataloader(self) -> Union[DataLoader, List[DataLoader]]:
        return DataLoader(self.val_dataset, batch_size=self.batch_size)


    def test_dataloader(self) -> Union[DataLoader, List[DataLoader]]:
        return DataLoader(self.test_set, batch_size=self.batch_size)


    # def transfer_batch_to_device(self, batch: Any, device: torch.device) -> Any:
    # 	raise NotImplementedError