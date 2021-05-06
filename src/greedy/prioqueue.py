import logging
from greedy.entry import Entry
import heapq
import itertools


class PrioQueue:
    def __init__(self) -> None:
        self.pq = []  # list of entries arranged in a heap
        self.entry_finder = {}  # mapping of tasks to entries
        self.REMOVED = "<removed-task>"  # placeholder for a removed task
        self.counter = itertools.count()  # unique sequence count

    def add_task(self, task: Entry, priority: int = 0) -> None:
        "Add a new task or update the priority of an existing task"
        if task in self.entry_finder:
            self.remove_task(task)
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heapq.heappush(self.pq, entry)

    def remove_task(self, task: Entry) -> None:
        "Mark an existing task as REMOVED.  Raise KeyError if not found."
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED

    def pop_task(self) -> Entry:
        "Remove and return the lowest priority task. Raise KeyError if empty."
        while self.pq:
            priority, count, task = heapq.heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return task
        raise KeyError("pop from an empty priority queue")

    def peekTop(self) -> None:
        i = 0
        while self.pq[i][2] == self.REMOVED:
            i = i + 1
        entry = self.pq[i]
        logging.debug("\t\t\t\t\t\t" +str(entry[2]))

    def peek(self, n_smallest: int) -> None:
        line1 = "index: "
        line2 = "cost:  "
        line3 = "label: "
        i = 0
        printed = 0
        while printed < n_smallest:
            if self.pq[i][2] != self.REMOVED:
                line1 = line1 + "\t" + str(i).zfill(4)
                entry = self.pq[i]
                line2 = line2 + "\t" + str(entry[0]).zfill(4)
                # print("{}\t{}".format(entry[2], type(entry[2])))
                line3 = line3 + "\t" + str(entry[2].node)
                printed = printed + 1
            i = i + 1
        print(line1)
        print(line2)
        print(line3)
        print()
