class Node:
    __slots__ = ['lang', 'start_index', 'end_index', 'next']
    def __init__(self, lang, start_index, end_index):
        self.lang = lang.lower()
        self.start_index = start_index
        self.end_index = end_index
        self.next = None

class LangListManager:
    def __init__(self):
        self.head = None

    def insert(self, lang, start_index, end_index):
        node = Node(lang, start_index, end_index)
        if not self.head or start_index < self.head.start_index:
            node.next = self.head
            self.head = node
        else:
            current = self.head
            while current.next and current.next.start_index < start_index:
                current = current.next
            node.next = current.next
            current.next = node

    def get_list_lang_text(self, text):
        current = self.head
        result = []
        while current:
            result.append((current.lang, text[current.start_index: current.end_index]))
            current = current.next
            
        return result
