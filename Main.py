import re
import numpy as np

def problem1(NPs, s):
    regex = {
        "first":
        [

            (
                '(NP_\\w+ (, )?such as (NP_\\w+ ?(, )?(and |or )?)+)'
                # 'NP_\w+\s+(such\s+as)\s+(NP_\w+)\s+(and|or)\s+NP_\w+ '
            ),
            (
                # '(NP_\\w+ (, )?including (NP_\\w+ ?(, )?(and |or )?)+)'
                'NP_\w+\s+including\s+NP_\w+\s+'
            )
        ],
        "last":
        [
            (
                '((NP_\\w+ ?(, )?)+(and|or)? are NP_\\w+)'
            ),
            (
                '((NP_\\w+ ?(, )?)+(was a)? NP_\\w+)'
            ),
            (
                '((NP_\\w+ ?(, )?)+(was an)? NP_\\w+)'
            )
        ]
    }

    #remove special characters like question mark/comma/period is replaced with space and lower case.
    sen = re.sub(r'[^\w\s]', '', s.lower()) 
    NP_Set = []

    for np in NPs:
        if re.search(np,sen):
            k = re.search(np,sen).span()
            sen = sen.replace(sen[re.search(np,sen).span()[0]:re.search(np,sen).span()[1]],str('NP_' + re.search(np,sen).group().replace(' ','_')))
        NP_Set.append(np.replace(' ','_'))
 
    extract = []
    for key,val in regex.items():
        for pattern in val:
            matches = re.search(pattern, sen)
            if matches:
                matches_str = matches.group(0)
                nouns = [a for a in matches_str.split() if a.startswith("NP_")]
                if key == "first":
                    p = nouns[0]
                    c = nouns[1:]
                else:
                    p = nouns[-1]
                    c = nouns[0:-1]
                for i in range(len(c)):
                    pairs = (p.replace('NP_','').replace('_',' '),c[i].replace('NP_','').replace('_',' '))
                    extract.append(pairs)
    return set(extract)

# problems1 = [
# 	(
#         ['dogs', 'cats', 'mammals', 'living things'],
#       """All mammals, such as dogs and cats, eat to survive. Mammals are living things, aren't they?"""),
# 	(
#         ['animals', 'dogs', 'cats'], 
#         "Some animals, including cats, are considered. But it is NOT true that dogs are animals; I refuse to accept it."),
# 	(
#         ['hemingway', 'bibliophile', 'author', 'william faulkner', 'mark twain'], 
#         "Hemingway was an author of many classics. But also, Hemingway was a bibliophile, having read the works of every other famous American author, such as William Faulkner and Mark Twain.")
# 	] 
    
# for n,corp in enumerate(problems1): 
#     problem1(corp[0], corp[1])

def problem2(word1, word2):
    arr = np.array(np.ones((len(word1)+1)*(len(word2)+1))*np.inf).reshape((len(word1)+1),(len(word2)+1))
    arr[:,-1] = np.arange(len(word1),-1,-1)
    arr[-1,:] = np.arange(len(word2),-1,-1)
    for i in range(len(word1)-1,-1,-1):
        for j in range(len(word2)-1,-1,-1):
            if word1[i] == word2[j]:
                arr[i][j] = arr[i + 1][j + 1] # move to next index
            else:
                arr[i][j] = 1+ min(arr[i+1][j],#insertion
                                   arr[i][j+1],#deletion
                                   2+arr[i+1][j+1]) #replace

    return int(arr[0][0])
