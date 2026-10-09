from collections import Counter

def is_subset(small, big):
    big = set(big)
    return all(item in big for item in small)

def first_unique(s):

    s = s.lower()
    counts = Counter(s)
    
    for ch in s:
        if counts[ch] == 1:
            return ch
    
    return None

def longest_palindrome(s):

    counts = Counter(s)
    length = 0
    odd_found = False

    for count in counts.values():
        is_odd = count % 2
        length += count - is_odd
        if is_odd:
            odd_found = True

    return length + 1 if odd_found else length

def is_anagram(s, t):
    return Counter(s) == Counter(t)