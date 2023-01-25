#%%
from scripts.utils import init_gdb, delete_scratch_files
import os
original_gdb, workspace, scratch_workspace = init_gdb()

delete_scratch_files(gdb = os.path.join(scratch_workspace))