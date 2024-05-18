class TrieNode:
    def __init__(self):
        self.child = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, words):
        n = self.root
        for char in words:
            if char not in n.child:
                n.child[char] = TrieNode()
            n = n.child[char]
        n.is_end = True

    def traverse_recursive(self, n, prefix):
        if n.is_end:
            print(prefix)
        for char, child_node in n.child.items():
            self.traverse_recursive(child_node, prefix + char)

    def traverse(self):
        return self.traverse_recursive(self.root, "")

    def delete_recursively(self, n, word, index):
        if index == len(word):
            if n.is_end:
                n.is_end = False
                return len(n.child) == 0
            return False

        char = word[index]
        if char not in n.child:
            return False
        should_del = self.delete_recursively(n.child[char], word, index + 1)
        if should_del:
            del n.child[char]
            return len(n.child) == 0 and not n.is_end
        return False

    def delete(self, word):
        return self.delete_recursively(self.root, word, 0)

    def autocomplete_helper(self, prefix, node, suggestions):
        if node.is_end:
            suggestions.append(prefix)
        for char, child_node in node.child.items():
            self.autocomplete_helper(prefix + char, child_node, suggestions)

    def autocomplete(self, prefix):
        suggestions = []
        node = self.root
        for char in prefix:
            if char not in node.child:
                return suggestions
            node = node.child[char]
            self.autocomplete_helper(prefix, node, suggestions)
        return suggestions

    def longest_prefix(self, word):
        node = self.root
        prefix = ""
        for char in word:
            if char in node.child:
                prefix += char
                node = node.child[char]
            else:
                break
        return prefix

    def searching(self,word):
        n = self.root
        for char in word:
            if char not in n.child:
                return False

            n = n.child[char]
        n.is_end = True


trie = Trie()
word = ['apple', "orange", "grapes", "ant", "gift"]
for i in word:
    trie.insert(i)
trie.delete("orange")

trie.traverse()
print(trie.longest_prefix("grapes"))

print(trie.autocomplete("apple"))
