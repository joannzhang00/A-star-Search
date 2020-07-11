
class PriorityQueue:
    def __init__(self):
        """Each element in the queue is a (key, element) tuple, where key
         is a distance, and element is the current node"""
        self.queue = []

    def __str__(self):
        result = ""
        for i in range(self.size()):
            (k, e) = self.queue[i]
            result += '(' + str(k) + ", " + e.getName() + "); "
            if i < self.size() - 1:
                result += ", "

        return result

    def size(self):
        return len(self.queue)

    def isEmpty(self):
        return len(self.queue) == 0

    def minKey(self):
        if not self.isEmpty():
            return self.queue[0][0]

        return None

    def removeMin(self):
        """Remove and return from the queue the element with the minimum key value"""
        return self.queue.pop(0)[1]

    def insertItem(self, key, element):
        if self.isEmpty():
            self.queue.append((key, element))
        else:
            if self.queue[-1][0] <= key:
                self.queue.append((key, element))
            else:
                insertPos = 0
                for i in range(self.size()):
                    if key <= self.queue[i][0]:
                        insertPos = i
                        break
                self.queue.insert(insertPos, (key, element))

    def contains(self, targetElement):
        for (k, e) in self.queue:
            if e.getName() == targetElement.getName():
                return True

        return False

    #update the key value of the target element
    def update(self, newKey, targetElement):
        index = 0
        for (k, e) in self.queue:
            if e.getName() == targetElement.getName():
                break
            index += 1

        if index < self.size():
            self.queue.pop(index)[-1]
            self.insertItem(newKey, targetElement)
