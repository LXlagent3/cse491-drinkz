import sieve

count = 0
for i in sieve.next():
    print i
    count += 1
    if count >= 10:
        break
    
