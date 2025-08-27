import os, json

files = os.listdir('results')
output = ["Model\tOverall\tEasy\tHard\tShort\tMedium\tLong"]
compensated = False

for file in files:
    filename = os.path.join('results', file)
    try:
        pred_data = json.load(open(filename, encoding='utf-8'))
    except Exception as e:
        pred_data = [json.loads(line) for line in open(filename, encoding='utf-8')]
    easy, hard, short, medium, long = 0, 0, 0, 0, 0
    easy_acc, hard_acc, short_acc, medium_acc, long_acc = 0, 0, 0, 0, 0
    for pred in pred_data:
        acc = int(pred['judge'])
        if compensated and pred["pred"] == None:
            acc = 0.25
        if pred["difficulty"] == "easy":
            easy += 1
            easy_acc += acc
        else:
            hard += 1
            hard_acc += acc

        if pred['length'] == "short":
            short += 1
            short_acc += acc
        elif pred['length'] == "medium":
            medium += 1
            medium_acc += acc
        else:
            long += 1
            long_acc += acc

    name = '.'.join(file.split('.')[:-1])

    overall_acc = round(100*(easy_acc+hard_acc)/len(pred_data), 1) if len(pred_data) > 0 else 0
    easy_pct = round(100*easy_acc/easy, 1) if easy > 0 else 0
    hard_pct = round(100*hard_acc/hard, 1) if hard > 0 else 0
    short_pct = round(100*short_acc/short, 1) if short > 0 else 0
    medium_pct = round(100*medium_acc/medium, 1) if medium > 0 else 0
    long_pct = round(100*long_acc/long, 1) if long > 0 else 0

    output.append(f"{name}\t{overall_acc}\t{easy_pct}\t{hard_pct}\t{short_pct}\t{medium_pct}\t{long_pct}")
open('result.txt', 'w', encoding='utf-8').write('\n'.join(output))
