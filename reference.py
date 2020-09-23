
with open('/Users/apple/Desktop/reference_list.txt') as f:
    for line in f:
        line = line.strip()
        if not (line.endswith(':') or line.startswith('The')):
            print(line)