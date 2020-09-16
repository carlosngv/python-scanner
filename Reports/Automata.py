from graphviz import Digraph

class Automata():
    def __init__(self, transitions, name):
        self.name = name
        self.transitions = transitions
        self.transition_list = []
        self.edges_list = []

    def graph(self):
        dot = Digraph(format='png', name = self.name)
        dot.attr(rankdir='LR', size='8,5')
        dic = {}
        # Keeping non repeted transitions.
        print("TRANS:", len(self.transitions))
        for transition in self.transitions:
            if transition not in self.transition_list:
                self.transition_list.append(transition)
        dot.attr('node', shape='circle')
        print("NUM:",len(self.transition_list))
        # Initialize nodes
        for transition in self.transition_list:
            if transition.get_status() == 'final':
                dot.node(str(transition.get_destiny()), peripheries='2')
            else:
                dot.node(str(transition.get_state()))
        for transition in self.transition_list:
            dot.edge(str(transition.get_state()), str(transition.get_destiny()), label=str(transition.get_value()))
        dot.render('../graphs/'+self.name, view=True)