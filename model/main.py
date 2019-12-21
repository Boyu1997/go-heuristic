from simulate import simulate
from train import train
from test import test

model_path = None
test_count = 100

simulation_count = 3000   # make initial random sample much bigger than onward training sample

for i in range(5):
    simulate(simulation_count=simulation_count, model_path=model_path, heuristic_model_iteration=i)
    train(heuristic_model_iteration=i)
    model_path = 'save/iteration-{:02d}-weights.hdf5'.format(i)
    test(model_path, test_count)

    # subsequent simulation number is smaller because of the longer simulation time
    simulation_count = 500
