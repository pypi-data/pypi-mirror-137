import pickle
import numpy as np

from paramga.run import Runner


def demo_state():
    return {
        "foo": 10,
        "bar": 360,
    }

def demo_conf():
    return {
        "foo": {
            "type": "number",
            "min": 1,
            "max": 80,
            "step": 8,
        }
    }

def model(params, data):
    return np.array([d * params['foo'] for d in data])
def demo_model():
    def model(params, data):
        return np.array([d * params['foo'] for d in data])
    return model

def process_outputs(outputs):
    return outputs + 10

def demo_process_outputs():
    def process_outputs(outputs):
        return outputs + 10
    return process_outputs

def loss_function(output, params):
    return abs(params['bar'] - sum(output) + 40)

def demo_loss_function():
    def loss_function(output, params):
        return abs(params['bar'] - sum(output) + 40)
    return loss_function

def demo_data():
    return [1, 2, 3, 3]

def demo_best_params():
    return {
        "foo": 40,
        "bar": 360,
    }

class TestRunner:



    def _default_instance(self, **kwargs):
        default_args = dict(
            param_base=demo_state(),
            mutation_conf=demo_conf(),
            func=model,
            loss_func=loss_function,
            input_data=demo_data(),
            process_outputs=process_outputs,
            population=8,
            max_iterations=100,
            tolerance=0.05,
        )
        return Runner(**{**default_args, **kwargs})

    def test_can_pickle_runner_state(self):
        runner = self._default_instance()
        pickle.dumps(runner.iteration_state)


    def test_can_pickle_runner(self):
        runner = self._default_instance()
        pickle.dumps(runner)