import numpy as np
import uproot
root_file_name = "out_root2.root"

root_file = uproot.open(root_file_name)

print("Root Dosyasıdaki Tree İsimleri: ", root_file.keys())

root_tree = root_file[root_file.keys()[0]]

branch_data = root_tree.arrays(root_tree.keys()[0],library = "np")

leaf_data = branch_data.get(list(branch_data.keys())[0])

print("Leaf Data:", leaf_data)
print("Leaf Data Shape", leaf_data.shape)
