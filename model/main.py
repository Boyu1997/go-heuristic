from simulate import simulate
from train import train

model_path = None
simulation_count = 1000   # make initial random sample much bigger than onward training sample

for i in range(3):
    simulate(simulation_count=simulation_count, model_path=model_path, heuristic_model_iteration=i)
    train(heuristic_model_iteration=i)
    model_path = 'save/iteration-{:02d}-weights.hdf5'.format(i)
    simulation_count = 50
