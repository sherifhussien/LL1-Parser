import argparse

start_var = ''
grammar={}
first={}
follow={}
terminals=[]
valid = True

def parseRule(rule):
    rule = rule.strip('\n')
    temp = rule.split(':')

    global start_var
    key = temp[0].strip(' ')
    if(start_var==''):
        start_var = key 

    t = temp[1].split('|')
    grammar = [r.strip(' ').split(' ') for r in t]

    first = temp[2].strip(' ').split(' ')
    follow = temp[3].strip(' ').split(' ')

    return key, grammar, first, follow


def generate_table():
    table = {}
    global valid
    for key in grammar:
        for t in terminals:
            for rule in grammar[key]:
                temp = get_first(rule)
                if t in temp or ('epsilon' in temp and t in follow[key]):
                    if (key, t) not in table:
                        table[(key, t)] = rule
                    else:
                        valid = False
    return table


def get_first(rule):
    res = []

    for i in range(len(rule)):
        if rule[i] in terminals or rule[i] == 'epsilon':
            res.append(rule[i])
            break
        elif 'epsilon' not in first[rule[i]]:
            res+=first[rule[i]]
            break
        elif 'epsilon' in first[rule[i]] and i!=len(rule)-1:
            res+=first[rule[i]]
            res.remove('epsilon')
        elif 'epsilon' in first[rule[i]] and i==len(rule)-1:
            res+=first[rule[i]]

    return res
    

def parse_table(table):
    res = ''
    for key in grammar:
        for t in terminals:
            res+=key+' : '+t+ ' : '
            if (key, t) in table:
                for v in table[(key, t)]:
                    res+=v+' '
            res+='\n'    
    return res    


def parse_string(input):
    input = input.strip('\n')
    input = input.split(' ')
    input.append('$')
    return input


def belong(table, input):
    stack = []
    stack.append('$')
    stack.append(start_var)
    
    accept = True

    pointer = 0

    while stack!=[]:
        pop = stack.pop()
        
        if pop!='epsilon':
            if (pop in terminals and input[pointer]!=pop) or (pop not in terminals and (pop, input[pointer]) not in table) or (pointer>=len(input)):
                accept = False
                break
            elif pop not in terminals:
                for item in reversed(table[(pop, input[pointer])]):
                    stack.append(item)
            elif pop in terminals and input[pointer]==pop:
                pointer+=1
     
    if accept:
        return 'yes'
    else:
        return 'no'




if __name__ == '__main__':
    parser = argparse.ArgumentParser(add_help=True, description='Sample Commandline')

    parser.add_argument('--grammar', action="store", help="path of file to take as input to read grammar", nargs="?", metavar="dfa_file")
    parser.add_argument('--input', action="store", help="path of file to take as input to test strings on LL table", nargs="?", metavar="input_file")
    
    args = parser.parse_args()

    print(args.grammar)
    print(args.input)

    # get the file object
    output_file1 = open("task_6_1_result.txt", "w+")

    with open(args.grammar, "r") as file:
        rules = file.readlines()

        for rule in rules:
            key, gram, fi, fo = parseRule(rule)
            grammar[key] = gram
            first[key] = fi
            follow[key] = fo

        print(grammar)
        # print(first)
        # print(follow)

        for key in grammar:
            for arr in grammar[key]:
                for v in arr:
                    if v not in grammar and v not in terminals and v !='epsilon':
                        terminals.append(v)
        terminals.append('$')
        # print(terminals)

        table = generate_table()
        # print(table)

        if valid:
            output_file1.write(parse_table(table))
        else:
            output_file1.write('invalid LL(1) grammar')


        output_file2 = open("task_6_2_result.txt", "w+")

        with open(args.input, "r") as file:
            input = file.readlines()[0]
            # print(input)
            # print(parse_string(input))

            if(valid):
                output_file2.write(belong(table, parse_string(input)))
            else:
                output_file2.write('no')
