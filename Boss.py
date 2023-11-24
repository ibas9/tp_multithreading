from manager import QueueClient
from task import Task
import queue

class Boss(QueueClient):
    def __init__(self):
        super().__init__()

    def submit_tasks(self, num_tasks):
        for i in range(num_tasks):
            task = Task(identifier=i)  # Create a task
            self.tasks.put(task)  # Put the task in the queue
            print(f"Task {i} submitted.")  # Message after each task is submitted


    def collect_results(self):
        results = []
        for i in range(num_tasks):
            try:
                result = self.results.get()  # Get the result
                results.append(result)
                print(f"Result for task {i} collected.")

            except queue.Empty:
                print("Empty results queue, end of collection.")
                break  # Exit the loop if the results queue is empty
        return results


if __name__ == "__main__":
    boss = Boss()
    num_tasks = 10
    boss.submit_tasks(num_tasks)

    print("Tasks submitted, collection of results...")
    results = boss.collect_results()
    print(f"{len(results)} results collected.")