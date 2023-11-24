import time
import numpy as np
import json


class Task:
    def __init__(self, identifier, size=None):
        self.identifier = identifier
        # choosee the size of the problem
        self.size = size or np.random.randint(300, 3_000)
        # Generate the input of the problem
        self.a = np.random.rand(self.size, self.size)
        self.b = np.random.rand(self.size)
        # prepare room for the results
        self.x = np.zeros((self.size))
        self.time = 0

    def work(self):
        start = time.perf_counter()
        self.x = np.linalg.solve(self.a, self.b)
        self.time = time.perf_counter() - start

    def to_json(self) -> str:
        return json.dumps({
            'identifier': self.identifier,
            'size': self.size,
            'a': self.a.tolist(),
            'b': self.b.tolist(),
            'x': self.x.tolist(),
            'time': self.time
        })

    @classmethod
    def from_json(cls, text: str) -> "Task":
        data = json.loads(text)
        task = cls(data['identifier'], data['size'])
        task.a = np.array(data['a'])
        task.b = np.array(data['b'])
        task.x = np.array(data['x'])
        task.time = data['time']
        return task

    def __eq__(self, other: "Task") -> bool or str:
        if self.identifier != other.identifier:
            return False, "identifier"
        if self.size != other.size:
            return False, "size"
        if not np.array_equal(self.a, other.a):
            return False, "a"
        if not np.array_equal(self.b, other.b):
            return False, "b"
        if not np.array_equal(self.x, other.x):
            return False, "x"
        if self.time != other.time:
            return False, "time"
        return True, None

#Test unitaire
def test_task_equality():
    a = Task("task1")

    a_json = a.to_json()
    print("Instance sérialisée en JSON.")

    b = Task.from_json(a_json)
    print("Instance désérialisée.")

    equal, diff_attr = a == b
    if equal:
        print("Test réussi : Les deux instances sont égales.")
    else:
        print(f"Test échoué : Différence détectée dans l'attribut '{diff_attr}'.")


test_task_equality()
