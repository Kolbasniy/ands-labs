from collections import deque
from dataclasses import dataclass
from typing import Optional, Sequence


@dataclass
class TreeNode:
    val: int = 0
    left: Optional["TreeNode"] = None
    right: Optional["TreeNode"] = None


def build_tree(values: Sequence[Optional[int]]) -> Optional[TreeNode]:
    if not values:
        return None

    root_value = values[0]
    if root_value is None:
        return None

    root = TreeNode(root_value)
    queue: deque[TreeNode] = deque([root])
    value_index = 1

    while queue and value_index < len(values):
        current = queue.popleft()

        left_value = values[value_index]
        if left_value is not None:
            left_node = TreeNode(left_value)
            current.left = left_node
            queue.append(left_node)
        value_index += 1

        if value_index < len(values):
            right_value = values[value_index]
        else:
            right_value = None
        if right_value is not None:
            right_node = TreeNode(right_value)
            current.right = right_node
            queue.append(right_node)
        value_index += 1

    return root


class SolutionA:
    def is_symmetric(self, root: Optional[TreeNode]) -> bool:
        if root is None:
            return True

        nodes_to_compare = deque([(root.left, root.right)])
        while nodes_to_compare:
            left_node, right_node = nodes_to_compare.popleft()

            if left_node is None and right_node is None:
                continue
            if left_node is None or right_node is None:
                return False
            if left_node.val != right_node.val:
                return False

            nodes_to_compare.append((left_node.left, right_node.right))
            nodes_to_compare.append((left_node.right, right_node.left))

        return True


class SolutionB:
    def diameter_of_binary_tree(self, root: Optional[TreeNode]) -> int:
        diameter = 0

        def depth(node: Optional[TreeNode]) -> int:
            nonlocal diameter
            if node is None:
                return 0

            left_depth = depth(node.left)
            right_depth = depth(node.right)
            diameter = max(diameter, left_depth + right_depth)
            return max(left_depth, right_depth) + 1

        depth(root)
        return diameter


class SolutionC:
    def is_cousins(self, root: Optional[TreeNode], x: int, y: int) -> bool:
        if root is None or x == y:
            return False

        queue: deque[tuple[TreeNode, Optional[TreeNode]]] = deque([(root, None)])
        while queue:
            level_size = len(queue)
            parents: dict[int, Optional[TreeNode]] = {}

            for _ in range(level_size):
                node, parent = queue.popleft()
                if node.val == x:
                    parents[x] = parent
                if node.val == y:
                    parents[y] = parent

                if node.left is not None:
                    queue.append((node.left, node))
                if node.right is not None:
                    queue.append((node.right, node))

            if x in parents or y in parents:
                return x in parents and y in parents and parents[x] is not parents[y]

        return False


def main() -> None:
    tree1 = build_tree([1, 2, 2, 3, 4, 4, 3])
    print(SolutionA().is_symmetric(tree1))

    tree2 = build_tree([1, 2, 2, None, 3, None, 3])
    print(SolutionA().is_symmetric(tree2))

    tree3 = build_tree([1, 2, 3, 4, 5])
    print(SolutionB().diameter_of_binary_tree(tree3))

    tree4 = build_tree([1, 2])
    print(SolutionB().diameter_of_binary_tree(tree4))

    tree5 = build_tree([1, 2, 3, 4])
    print(SolutionC().is_cousins(tree5, 4, 3))

    tree6 = build_tree([1, 2, 3, None, 4, None, 5])
    print(SolutionC().is_cousins(tree6, 5, 4))


if __name__ == "__main__":
    main()
