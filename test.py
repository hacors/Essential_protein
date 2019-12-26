from ogb.nodeproppred.dataset_dgl import DglNodePropPredDataset
dataset = DglNodePropPredDataset(name='ogbn-proteins')
num_tasks = dataset.num_tasks  # obtaining number of prediction tasks in a dataset

splitted_idx = dataset.get_idx_split()
train_idx, valid_idx, test_idx = splitted_idx["train"], splitted_idx["valid"], splitted_idx["test"]
# graph: dgl graph object, label: torch tensor of shape (num_nodes, num_tasks)
graph, label = dataset[0]
from ogb.nodeproppred import Evaluator

evaluator = Evaluator(name = 'ogbn-proteins')
print(evaluator.expected_input_format) 
print(evaluator.expected_output_format)
pass
