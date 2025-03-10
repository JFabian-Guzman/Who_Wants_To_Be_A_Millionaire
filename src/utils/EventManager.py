class EventManager:
    def __init__(self):
        self.subscribers = dict()

    def subscribe(self, event_type: str, fn):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(fn)

    def unsubscribe(self, event_type: str):
        if event_type in self.subscribers:
            del self.subscribers[event_type]

    def notify(self, event_type: str, data = None):
        if event_type in self.subscribers:
            for fn in self.subscribers[event_type]:
                fn(data)

