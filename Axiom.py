import string
import itertools
Ualphabet = list(string.ascii_uppercase)
Lalphabet = list(string.ascii_lowercase)

class AxiomSystem:
    def __init__(self,axioms,un_operators,bi_operators,defined_ops,objects,extra_ops):

        self.operators = dict()
        self.operators[1] = un_operators
        self.operators[2] = bi_operators
        self.operators[3] = defined_ops
        self.axioms = axioms

        for a in self.axioms:
            a = a.lower()

        characters = list()
        for x in self.axioms:
            characters.extend(list(x))
        characterset = set(characters)
        for x in (self.operators[1]+self.operators[2]+['(',')','[',']']+extra_ops):
            if x in characterset:
                characterset.remove(x)

        self.atoms = characterset
        self.variables = Ualphabet[0:objects]

    def number_of_atoms(self,axiom):
        characters = list()
        characters.extend(list(atom))
        characterset = set(characters)
        for x in (self.operators[1]+self.operators[2]+['(',')','[',']']):
            characterset.remove(x)
        return len(characterset)
        
    
    def indipendence(self,axiom_num):
        mappings = self.maketable(self.atoms,self.variables)
        var_ops1 = self.variable_ops1(self.variables)
        var_ops2 = self.variable_ops2(self.variables)
        op1_maps = self.maketable(var_ops1,self.variables)
        op2_maps = self.maketable(var_ops2,self.variables)
        ops_def = self.ops_def_table(self.variables,mappings)

        count = 0.0
        next_print = 0.001
        
        for o1 in op1_maps:
            for o2 in op2_maps:
                count = count + 1.0
                percent = (count / (len(op1_maps) * len(op2_maps)))
                if percent > next_print:
                    print next_print
                    next_print = next_print + 0.001
                this_A = False
                other_A = True
                for i in range(len(self.axioms)):
                    axiom = self.axioms[i]
                    A = self.A_taut(o1,o2,ops_def,axiom,mappings)
                    if i == axiom_num:
                        this_A = A
                    else:
                        if A == False:
                            other_A = False
                            break
                if this_A == False and other_A == True:
                    return [o1 , o2]
        return list()
            

    def maketable(self,keys,variables):

        all_atom_maps = list()
        permutations = list()
        permutations = itertools.product(variables, repeat = len(keys))
        table = list()
        for perm in permutations:
            i = 0
            amap = dict()
            for atom in keys:
                amap[atom] = perm[i]
                i = i + 1
            table.append(amap)
        return table

    def variable_ops1(self,variables):
        ops_with_vars = list()
        for op1 in self.operators[1]:
            for var in variables:
                ops_with_vars.append(op1 + var)   
        return ops_with_vars

    def variable_ops2(self,variables):
        ops_with_vars = list()
        for op2 in self.operators[2]:
            for var1 in variables:
                for var2 in variables:
                    ops_with_vars.append(var1 + op2 + var2)     
        return ops_with_vars

    def ops_def_table(self,variables,atom_maps):
        ops_with_vars = dict()
        operator_def = self.operators[3]
        for x,y in operator_def.iteritems():
            for amap in atom_maps:
                op_key = x
                op_value = y
                for a,b in amap.iteritems():
                    op_key = string.replace(op_key, a, b)
                    op_value = string.replace(op_value, a, b)
                ops_with_vars[op_key] = op_value
        return ops_with_vars
    
    def solve(self,in_axiom,atom_map,op1_map,op2_map,ops_def,dermap):
        axiom = in_axiom[:]
        atoms = atom_map.keys()
        objects = self.variables
        for x, y in atom_map.iteritems():
            axiom = string.replace(axiom, x, y)
        if axiom in dermap:
            return dermap[axiom]
        copy_axiom = axiom[:]
        while len(axiom) > 1:
            prev = axiom
            for o in objects:
                o_in_p = ('(' + o + ')')
                o_in_b = ('[' + o + ']')
                axiom = string.replace(axiom, o_in_p, o)
                axiom = string.replace(axiom, o_in_b, o)
            for value_in,value_out in ops_def.iteritems():
                axiom = string.replace(axiom, value_in, value_out)
            for value_in,value_out in op1_map.iteritems():
                axiom = string.replace(axiom, value_in, value_out)
            for value_in,value_out in op2_map.iteritems():
                axiom = string.replace(axiom, value_in, value_out)
            if (prev == axiom):
                print axiom
                return 'error'
        dermap[copy_axiom] = axiom
        return axiom


    def A_taut(self,op1_map,op2_map,ops_def,axiom,mappings):
        ant = op1_map.values() + op1_map.values()
        if not 'A' in ant:
            return False
        dermap = dict()
        for m in mappings:
            a = self.solve(axiom,m,op1_map,op2_map,ops_def,dermap)
            if (a == 'error'):
                print 'ERROR'
                return 'error'
            if (not a == 'A'):
                return False
        return True
