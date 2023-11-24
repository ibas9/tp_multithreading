from manager import QueueClient
import queue

class Minion(QueueClient):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            try:
                task = self.tasks.get()  # Get a task
                print("----------")
                print(f"Task {task.identifier} received.")
            except queue.Empty:
                print("Queue empty, Minion stops.")
                return  # Stop if the task queue is empty

            task.work()  # Execute the task
            print(f"Task {task.identifier} completed in {task.time:.4f} seconds.")
            #print(f"a: {task.a}")
            #print(f"b: {task.b}")
            self.results.put(task)  # Send the result to the results queue
            print(f"Result of Task {task.identifier} sent.")
            print("----------")


if __name__ == "__main__":
    minion = Minion()
    minion.run()
