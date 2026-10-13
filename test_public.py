"""Visible examples, not the full grading suite. Run with unittest discovery."""
import unittest
from GameStatus_5120 import GameStatus
from multiAgents import minimax,negamax
from game_controller import GameController
import csp


class Leaf:
    def __init__(self,value,children=None,turn=True):
        self.value,self.children,self.turn_O=value,children,turn
    def is_terminal(self):return self.children is None
    def get_scores(self,terminal):return self.value
    def get_negamax_scores(self,terminal):return self.value
    def get_moves(self):return [(0,i) for i in range(len(self.children))]
    def get_new_state(self,move):return self.children[move[1]]


class PublicTests(unittest.TestCase):
    def test_triplet_does_not_end_game(self):
        s=GameStatus([[1,1,1],[0,0,0],[0,0,0]],False)
        self.assertIs(s.is_terminal(),False)
    def test_overlap_and_all_directions(self):
        s=GameStatus([[1]*4 for _ in range(4)])
        self.assertEqual(s.triplet_counts(),(24,0))
        self.assertEqual(s.get_scores(True),2400)
    def test_heuristic(self):
        s=GameStatus([[1,1,0],[0,0,0],[0,0,0]])
        # One open pair (10), two open columns (1 each), one diagonal singleton (1).
        self.assertEqual(s.get_scores(False),13)
    def test_moves_and_copy(self):
        s=GameStatus([[0]*3 for _ in range(3)],False)
        self.assertEqual(s.get_moves()[0],(0,0))
        child=s.get_new_state((2,1))
        self.assertEqual(child.board_state[2][1],-1)
        self.assertEqual(s.board_state[2][1],0)
        self.assertIs(child.turn_O,True)
    def test_occupied_move(self):
        s=GameStatus([[1,0,0],[0,0,0],[0,0,0]])
        with self.assertRaises(ValueError):s.get_new_state((0,0))
    def test_minimax_two_levels(self):
        tree=Leaf(99,[Leaf(88,[Leaf(3),Leaf(5)],False),Leaf(77,[Leaf(2),Leaf(9)],False)])
        self.assertEqual(minimax(tree,2,True),(3,(0,0)))
    def test_minimax_depth_zero(self):
        self.assertEqual(minimax(Leaf(7),0,False),(7,None))
    def test_negamax_leaf_perspective(self):
        self.assertEqual(negamax(Leaf(7,turn=False),0,-1),(-7,None))
    def test_first_tie(self):
        tree=Leaf(0,[Leaf(4),Leaf(4)])
        self.assertEqual(minimax(tree,1,True),(4,(0,0)))
    def test_human_x_starts(self):
        c=GameController(3,'X')
        self.assertTrue(c.human_move(0,0))
        self.assertEqual(c.state.board_state[0][0],-1)
        self.assertFalse(c.human_move(0,1))
    def test_knight_domains(self):
        self.assertEqual(csp.knight_domains(1,1),{'K0':[(0,0)]})
    def test_knight_attack(self):
        self.assertFalse(csp.knights_consistent({'K0':(0,0),'K1':(1,2)},3,2))
        self.assertTrue(csp.knights_consistent({},3,2))
    def test_vehicle_partial(self):
        self.assertFalse(csp.vehicles_consistent({'D':('JB',3),'C':('CGI',3)}))
        self.assertTrue(csp.vehicles_consistent({'B':('CGI',1),'E':('JB',1)}))
    def test_vehicle_unary_domain(self):
        self.assertEqual(csp.vehicle_domains()['D'],[('JB',3),('JB',4)])


if __name__=='__main__':unittest.main()
