import sys
import getopt
import string
import Axiom

def main():
    axioms = list()
    un_ops = ['~']
    bi_ops = ['^']
    ops_def = dict()
    ops = list()
    print 'Welcome to Axiom Independence Checker'
    print 'Enter \'help\' for help'
    in_string = ''
    while not in_string == 'exit':
        try:
            in_string = raw_input('>')
            if string.lower(in_string) == 'help':
                print 'to add an axiom to the system:'
                print '     type command \'new axiom\''
                print '     type the desired axiom'
                print '     the axiom must use lower case characters and defined operators'
                print '     the default operators are \'~\'(not) and \'^\'(and)'
                print '     when all axioms have been entered type command \'back\''
                print ''
                print 'to add a new operator:'
                print '     type command \'new operator\''
                print '     follow on prompts to define the a new operator'
                print '     new operators must be one character long'
                print '     type \'back\' to return'
                print ''
                print 'to check axiom independence:'
                print '     type command \'check\''
                print '     enter the number of the axiom to check'
                print '     enter the number of objects to use to use in checking'
                print '     type \'back\' to return'
                print ''
                print 'to exit the program:'
                print '     type command \'exit\''
                print ''
                print 'Created by Matt Dallas'
                print 'Contact me with questions at dallam@rpi.edu'
                continue
                
            if string.lower(in_string) == 'new axiom':
                while not in_string == 'back':
                    in_string = raw_input('     Enter Axiom>')
                    if in_string == 'back':
                        continue
                    for x in list(in_string):
                        if not x in (list(string.ascii_lowercase) + un_ops + bi_ops + ops + ['(',')','[',']']):
                            print 'error: must be lowercase letters and defined operators'
                            continue
                    axioms.append(in_string)
            if string.lower(in_string) == 'new operator':
                while not in_string == 'back':
                    in_string = raw_input('     Enter Operator>')
                    if in_string == 'back':
                        continue
                    op = in_string
                    good = False
                    op_key = ''
                    while good == False:
                        in_string = raw_input('     (b)inary or (u)nary?>')
                        if in_string == 'b':
                            good = True
                            print ('     define the operator')
                            op_key = 'a' + op + 'b'
                        if in_string == 'u':
                            good = True
                            print ('     define the operator')
                            op_key = op + 'a'
                    in_string = raw_input('     '+ op_key +'=')
                    ops_def[op_key] = in_string
                    ops.append(op)
            if string.lower(in_string) == 'check':
                i = 1
                for a in axioms:
                    print (repr(i) + ' - ' + a)
                    i = i + 1
                while not in_string == 'back':
                    in_string = raw_input('     Check Which Axiom>')
                    if in_string == 'back':
                        continue
                    a_index = int(in_string) - 1
                    in_string = raw_input('     Number of Objects>')
                    if in_string == 'back':
                        continue
                    num = int(in_string)
                    AxiomSystem = Axiom.AxiomSystem(axioms,un_ops,bi_ops,ops_def,num,ops)
                    out = AxiomSystem.indipendence(a_index)
                    if len(out) == 0:
                        print 'no independence found'
                    else:
                        for x in out:
                            for a,b in x.iteritems():
                                print (a + ' = ' +  b)
        except (RuntimeError, TypeError, NameError):
            print 'error'
            continue
    sys.exit()

main()
