import sys

ACCURACY_REPORT = 'accuracy of test results'

results = {}

for attempt_number, log in enumerate(sys.argv[1:]):
    attempt_number += 1
    with open(log, 'r', encoding='utf8') as f:
        query_number = 0
        for line in f.readlines():
            if ACCURACY_REPORT in line:
                query_number += 1
                result = float(line.split()[-1])

                if attempt_number not in results:
                    results[attempt_number] = []

                results[attempt_number].append(result if result >= 0 else 0)

for query_number in range(len(results[1])):
    res = []
    for attempt_number in results.keys():
        res.append(results[attempt_number][query_number])

    res.append(sum(res) / len(res))
    print(','.join(map(str, res)))
