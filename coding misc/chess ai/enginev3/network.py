import pandas as pd
import numpy as np
import re
import gc
import chess
import torch
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.nn.functional as F
from reformat import ChessDataset
