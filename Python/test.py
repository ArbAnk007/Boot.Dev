# # Binary Tree

# class Node(object):
#     def __init__(self, val=None):
#         self.val = val
#         self.left = None
#         self.right = None

# def wrapper(arr):
#     idx = -1
#     def build_tree(arr):
#         nonlocal idx
#         idx += 1
#         if idx < len(arr):
#             if(arr[idx] == -1):
#                 return None
            
#             new_node = Node(arr[idx])
#             new_node.left = build_tree(arr)
#             new_node.right = build_tree(arr)
#             return new_node
#     return build_tree(arr)

# nums = [2, 3, -1, -1, 1, 4, 3, -1, -1]
            

# tree = wrapper(nums)





















# def format_tree_string(bst_node, lines, level=0):
#     if bst_node != None:
#         format_tree_string(bst_node.left, lines, level + 1)
#         lines.append(" " * 4 * level + "> " + str(bst_node.val))
#         format_tree_string(bst_node.right, lines, level + 1)

# lines = []
# format_tree_string(tree, lines)
# print("\n".join(lines))