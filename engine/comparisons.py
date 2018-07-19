from engine.comparison import Comparison
from engine.variables import Variables
from engine.arrays import Arrays

class Comparisons():
    def __init__(self):
        self.variables = Variables()
        self.comparison_list = []

        ## -- Place Comparisons below --
        # example: Comparison('1', 'var(a) < var(b)')

        ##
        ## First Binary Tree
        ##

        # Root comparisons
        root_node = Comparison('root', True)

        # Next Layer (Root underlying comparisons)
        first_node = Comparison('first', self.variables.b < self.variables.d)
        second_node = Comparison('second', (self.variables.d < self.variables.b < self.variables.e))
        third_node = Comparison('third', self.variables.b > self.variables.e)

        # Add nodes to Root node
        root_node.add_comparison(first_node)
        root_node.add_comparison(second_node)
        root_node.add_comparison(third_node)

        # End of first layer

        # Second layer (first_node layer)
        fifth_node = Comparison('fifth', self.variables.f4 > self.variables.g)
        six_node = Comparison('six', self.variables.g < self.variables.f3)
        seven_node = Comparison('seven', self.variables.g < self.variables.f2)
        eighth_node = Comparison('eighth', self.variables.g < self.variables.f1)
        nineth_node = Comparison('nineth', self.variables.g > self.variables.f1)

        # Add nodes first_node
        first_node.add_comparison(fifth_node)
        first_node.add_comparison(six_node)
        first_node.add_comparison(seven_node)
        first_node.add_comparison(eighth_node)
        first_node.add_comparison(nineth_node)

        # End of first_node nodes - lmao

        # Second set of nodes
        tenth_node = Comparison('tenth', self.variables.f4 > self.variables.g)
        eleventh_node = Comparison('eleventh', self.variables.g < self.variables.f3)
        twelve_node = Comparison('twelve', self.variables.g < self.variables.f2)
        thirteen_node = Comparison('thirteen', self.variables.g < self.variables.f1)
        fourteen_node = Comparison('fourteen', self.variables.g > self.variables.f1)

        # Add nodes first_node
        second_node.add_comparison(tenth_node)
        second_node.add_comparison(eleventh_node)
        second_node.add_comparison(twelve_node)
        second_node.add_comparison(thirteen_node)
        second_node.add_comparison(fourteen_node)

        # Third set of nodes
        fifteen_node = Comparison('fifteen', self.variables.f4 > self.variables.g)
        sixteen_node = Comparison('sixteen', self.variables.g < self.variables.f3)
        seventeen_node = Comparison('seventeen', self.variables.g < self.variables.f2)
        eighteen_node = Comparison('eighteen', self.variables.g < self.variables.f1)
        nineteen_node = Comparison('nineteen', self.variables.g > self.variables.f1)

        # Add nodes first_node
        third_node.add_comparison(fifteen_node)
        third_node.add_comparison(sixteen_node)
        third_node.add_comparison(seventeen_node)
        third_node.add_comparison(eighteen_node)
        third_node.add_comparison(nineteen_node)

        # End of third layer

        self.comparison_list.append(root_node)

    def get_new_values(self):
        self.variables = Variables()

