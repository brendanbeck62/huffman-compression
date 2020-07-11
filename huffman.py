
def display_welcome():
    print ("Huffman Compresion Program")
    print ("**************************")

    my_string = input("Please enter a string to comress:")
    len_my_string = len(my_string)

    print("Your message is:")
    print(my_string)
    print("Your data is", len_my_string * 8, "bits long")
    return my_string



my_string = display_welcome()

# create a list of characters and their frequency and a list of characters in use
letters = []
only_letters = []
for letter in my_string:
    if letter not in letters:
        freq = my_string.count(letter)
        letters.append(freq)
        letters.append(letter)
        only_letters.append(letter)

# generate base-level nodes for the huffman_tree frequency and letter e.g. [7,"e"][12,"t"]...
nodes = []
while len(letters) > 0:
    nodes.append(letters[0:2])
    letters = letters[2:]
nodes.sort()
huffman_tree = []
huffman_tree.append(nodes)

# recursibely combine base nodes to create the huffman tree and allocates either a 0 or 1 to each
# pair of nodes prior to combining which will be later used to create the binary code for each letter
def combine(nodes):
    pos = 0
    newnode = []
    ## get two lowest nodes
    if len(nodes) > 1:
        nodes.sort()
        ## adds in the 0,1 for later use
        nodes[pos].append("0")
        nodes[pos+1].append("1")
        combined_node1 = (nodes[pos][0] + nodes[pos+1][0])
        combined_node2 = (nodes[pos][1] + nodes[pos+1][1])
        newnode.append(combined_node1)
        newnode.append(combined_node2)
        newnodes = []
        newnodes.append(newnode)
        newnodes = newnodes + nodes[2:]
        nodes = newnodes
        huffman_tree.append(nodes)
        combine(nodes)
    return huffman_tree

newnodes = combine(nodes)

# tree needs to be inverted - this gives a rough visualisation
huffman_tree.sort(reverse=True)
print ("Here is the Huffman Tree, showing the merged nodes and binary pathways")

# remove duplicate items in the huffman tree and create an array CHECKLIST with just the nodes
# the following code is ONLY for visualising and printing the tree array and does nothing for the algorithm
checklist = []
for level in huffman_tree:
    for node in level:
        if node not in checklist:
            checklist.append(node)
        else:
            level.remove(node)
count = 0
for level in huffman_tree:
    print ("Level", count, ":", level)
    count += 1

print ()

# build the binary codes for each character - easy cop out if there is only 1 type of character in the string
letter_binary = []
if len(only_letters) == 1:
    letter_code = [only_letters[0],"0"]
    letter_binary.append(letter_code * len(my_string))
else:
    for letter in only_letters:
        lettercode = ""
        for node in checklist:
            if len(node) > 2 and letter in node[1]:
                lettercode = lettercode + node[2]
        letter_code = [letter, lettercode]
        letter_binary.append(letter_code)

# output letters with binary codes
print ("Your binary codes are as follows:")
for letter in letter_binary:
    print (letter[0], letter[1])

# creates bitstring of the original message using the new codes you have generated for each letter
bitstring = ""
for character in my_string:
    for item in letter_binary:
        if character in item:
            bitstring = bitstring + item[1]

# convert the string to an actual binary digit
binary = ((bin(int(bitstring, base=2))))


def display_summary(my_string, binary, letter_binary):
    # summary of data compression
    uncompressed_file_size = len(my_string) * 7
    compressed_file_size = len(binary) - 2
    print ("Your original file size was", uncompressed_file_size, "bits.")
    print ("The compressed file is", compressed_file_size, "bits.")
    print ("This is as saving of ", uncompressed_file_size-compressed_file_size, "bits, with a compression ratio of", round(uncompressed_file_size/compressed_file_size,1), ": 1")

    # show the data compressed to a string of binary digits
    print ("Your message in binary is:")
    print (binary)

    # uncompress the data, using letter_binary array (basically a dictionary of letters and codes)
    # convert binary to string
    bitstring = str(binary[2:])
    uncompressed_string = ""
    code = ""
    for digit in bitstring:
        code = code + digit
        pos = 0
        for letter in letter_binary:
            if code == letter[1]:
                uncompressed_string = uncompressed_string + letter_binary[pos][0]
                code = ""
            pos += 1

    # output the uncompressed data
    print ("Your uncompressed message is:")
    print (uncompressed_string)

display_summary(my_string, binary, letter_binary)