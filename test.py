def repeatedSubstringPattern(s: str):
    '''
    given a string, return the pattern if this is a repeated substring, else None
    '''
    LPS = LSP(s)
    print(LPS)
    if len(s) == 1:
        return None
    if len(s) == 2 and s[0] == s[1]:
        return s[0]
    # if len(set(s)) == 1:
    #     return True
    i, j = 1, 0 
    length = 1
    # gcd = math.gcd(LPS[-1], len(s))
    # if LPS[-1] != 1 and LPS[-1] != 0 and (LPS[-1] // gcd + 1) == (len(s) // gcd):
    #     return True
    # return False 
    if LPS[-1] and LPS[-1] % (len(s) - LPS[-1]) == 0:
        return s[:len(s) - LPS[-1] + 1] 
    else: 
        return None

def LSP(pattern):
    # longest suffix prefix problem
    # return an array where arr[i] represents the longest length of the suffix prefix match
    A = [0] * len(pattern)

    i, prev = 1, 0
    while i < len(pattern):
        if pattern[i] == pattern[prev]:
            A[i] = prev + 1
            i += 1
            prev += 1
        elif prev == 0:
            A[i] = 0
            i += 1
        else:
            prev = A[prev - 1]
    return A


repeatedSubstringPattern("343434")
