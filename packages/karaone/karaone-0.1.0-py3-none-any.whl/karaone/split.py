""" Scripts to split Kqra One database into numpy files with X, Y.
"""
import os
import gc
import mne
import numpy as np
import scipy.io as sio
from typing import List, Optional

class Dataset:
    
    def __init__(self, subject: str, cnt_file: str,
                 drop_channels: Optional[List[str]] = ['VEO', 'HEO',
                                                       'EKG', 'EMG',
                                                       'Trigger'],
                 type_target: Optional[str] = "thinking_inds",
                 raw: Optional[str] = "rawextracted",
                 output: Optional[str] = "cleandata"):
        """Class for spliting KAra One

        Args:
            subject (str): Current subject
            cnt_file (str): Path to .cnt file
            drop_channels (Optional[List[str]]): [Chanels to remove from raw eeg data]. Defaults to ['VEO', 'HEO', 'EKG', 'EMG', 'Trigger'].
            type_target (Optional[str]): [Type of target to split]. Defaults to "thinking_inds".
            raw (Optional[str]): Path where is you raw data. Defaults to "rawextracted".
            output (Optiolal[str]: Path where will sve your data. Defaults to "cleandata".)
        """
        
        self.subject = subject
        self.path = os.path.join(raw, subject)
        self.path_output = os.path.join(output, f"{subject}.npz")
        self.type = type_target
        self.cnt_file = cnt_file
        self.epochs_index = sio.loadmat(os.path.join(self.path, "epoch_inds.mat"),
                                        variable_names=('clearing_inds',
                                                        'thinking_inds'))
        
        self.drop_channels = drop_channels
        
        targets = sio.loadmat(os.path.join(self.path, "all_features_simple.mat"))
        
        self.targets = targets['all_features'][0, 0]["prompts"][0]
        
        self._load_raw()
    
    def __repr__(self) -> str:
        
        print(f"Subject: {self.subject}, {self.path}, {self.path_output}")
    
    def _load_raw(self) -> None:
        """[Loads raw eeg data and drops channels]

        Args:
            drop_channels (Optional[List[str]]): [Chanels to remove from raw eeg data]. Defaults to ['VEO', 'HEO', 'EKG', 'EMG', 'Trigger'].

        Returns:
            None
        """

        raw = mne.io.read_raw_cnt(self.cnt_file, preload = True)
        
        self.raw = raw.drop_channels(self.drop_channels)
        
        self.raw = raw
          
    def _filter(self):
        """TODO"""
        pass
    
    def make_dataset(self) -> bool:
        """Makes dataset for current subject
        """
        
        X = list()
        
        channels = list()
                
        for word_index,_ in enumerate(self.targets):
            
            start_epoch = self.epochs_index[self.type][0][word_index][0][0]
            
            end_epoch = self.epochs_index[self.type][0][word_index][0][1]
            
            if len(channels):
                
                channels.clear()
                
                gc.collect()
            
            for channel_index, _ in enumerate(self.raw.ch_names):
                
                epoch = self.raw[channel_index][0][0][start_epoch : end_epoch]
                
                channels.append(epoch)
                
            X.append(channels)
        
        X = np.array(X)
        
        np.savez(self.path_output, X = X, Y = self.targets)
        
        del X
        del self.raw
        gc.collect()