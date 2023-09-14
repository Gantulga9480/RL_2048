from py2048.py2048 import Py2048, Board, UP, DOWN, LEFT, RIGHT
from treesearch.treesearch import Node, BredthFirstSearch


class GameNode(Node):

    def __init__(self,
                 state: Board,
                 parent: Node,
                 edge=None,
                 value: float = 0,
                 is_leaf: bool = False) -> None:
        super().__init__(parent, edge, value, is_leaf)
        self.state = state


class GameTree(BredthFirstSearch):

    def __init__(self, max_depth: int = 1) -> None:
        super().__init__(max_depth)
        self.actions = [UP, DOWN, LEFT, RIGHT]

    def expand(self, node: GameNode) -> bool:
        is_expanded = False
        # Try to expand tree by executing all possible actions
        for action in self.actions:
            # Copy parent node state to childe node
            childe_state = Board(node.state.size)
            childe_state.set_all(node.state)
            # Execute current action on childe node state and observe next state
            is_moved = childe_state.move(action)
            if is_moved:
                # if moved expand tree by inserting new node to current parent node
                self.append(GameNode(childe_state, node, action, childe_state.score, False))
                is_expanded = True
        # Must return boolean flag indicating tree expansion
        return is_expanded


class Py2048BFS(Py2048):

    def __init__(self, board_size, max_tree_depth) -> None:
        super().__init__(board_size)
        self.tree = GameTree(max_tree_depth)

    def loop(self):
        res = self.tree.search(GameNode(self.board, None, None, self.board.score, False))
        try:
            actions, score = res
            self.step(actions[0])
            self.tree.reset()
        except Exception:
            pass


if __name__ == '__main__':
    Py2048BFS(4, 6).loop_forever()
