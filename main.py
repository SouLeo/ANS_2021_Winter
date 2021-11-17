import os
import string
from pathlib import WindowsPath
import json


def open_annotations(wpath: WindowsPath, name: str):
    # BETHANY SPECIFIC
    if name == 'bethany':
        json_list = [pos_json for pos_json in os.listdir(wpath) if pos_json.endswith('.json')]
        json_list_cropped = [e[19:] for e in json_list]
        json_list_cropped = [e[:-11] for e in json_list_cropped]
        json_cropped_int = [int(x) for x in json_list_cropped]
        json_cropped_int.sort()
        json_cropped_int = [str(x) for x in json_cropped_int]

        x = range(len(json_cropped_int))
        beth_file_names = []
        for i in x:
            beth_file_string = 'bethany_umrf_graph_' + json_cropped_int[i] + '.umrfg.json'
            beth_file_names.append(beth_file_string)

        json_dicts = []
        for json_file in beth_file_names:
            with open('c:/Users/321785/PycharmProjects/URA_anno_eval_11_16/Bethany/' + json_file, 'r') as f:
                json_string = f.read()
                json_dict = json.loads(json_string)
                json_dicts.append(json_dict)

    # SID SPECIFIC
    if name == 'sid':
        json_list = [pos_json for pos_json in os.listdir(wpath) if pos_json.endswith('.json')]
        json_list_cropped = [e[11:] for e in json_list]
        json_list_cropped = [e[:-11] for e in json_list_cropped]
        json_cropped_int = [int(x) for x in json_list_cropped]
        json_cropped_int.sort()
        json_cropped_int = [str(x) for x in json_cropped_int]

        x = range(len(json_cropped_int))
        sid_file_names = []
        for i in x:
            sid_file_string = 'umrf_graph_' + json_cropped_int[i] + '.umrfg.json'
            sid_file_names.append(sid_file_string)

        json_dicts = []
        for json_file in sid_file_names:
            with open('c:/Users/321785/PycharmProjects/URA_anno_eval_11_16/Sid/' + json_file, 'r') as f:
                json_string = f.read()
                json_dict = json.loads(json_string)
                json_dicts.append(json_dict)
    return json_dicts


def open_ann_file(file_path: str):
    with open(file_path) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    return lines


def compare_against_ann_file(ann_sentences: list, json_anns: dict):
    i = 0
    pruned_sentences = []
    len_json_anns = len(json_anns)
    ann_sentences = ann_sentences[0:len_json_anns]
    for sentence in ann_sentences:
        desc = json_anns[i]['umrf_actions'][0]['description']
        sentence_nopunc = "".join(c for c in sentence if c not in ('!', '.', ':', ','))
        if desc in sentence:
            pruned_sentences.append(json_anns[i])
        elif desc in sentence_nopunc:
            pruned_sentences.append(json_anns[i])
        else:
            x = range(i, len(json_anns))
            for j in x:
                desc = json_anns[j]['umrf_actions'][0]['description']
                if desc in sentence:
                    pruned_sentences.append(json_anns[j])
                    break
        i = i + 1
    return pruned_sentences


def check_aligned(ann_1: list, ann_2: list):
    del ann_1[4]  # del elements because sid didn't do these annotations.
    del ann_1[13]
    del ann_1[56]
    del ann_1[70]
    del ann_1[114]
    del ann_1[138]
    if len(ann_1) == len(ann_2):
        print(':)')
    else:
        if len(ann_1) < len(ann_2):
            ann_2 = ann_2[:len(ann_1)]
        else:
            ann_1 = ann_1[:len(ann_2):]

    x = range(0, len(ann_1))
    is_aligned = []
    for i in x:
        sentence_nopunc_1 = "".join(c for c in ann_1[i]['umrf_actions'][0]['description'] if c not in ('!', '.', ':', ','))
        sentence_nopunc_2 = "".join(c for c in ann_2[i]['graph_description'] if c not in ('!', '.', ':', ','))
        if sentence_nopunc_1 in sentence_nopunc_2:
            is_aligned.append(1)
        else:
            is_aligned.append(0)

    return ann_1, ann_2


def check_acc(ann_1: list, ann_2: list):
    x = range(0, len(ann_1))
    acc = []
    sum = 0
    for i in x:
        b_actions = ann_1[i]['umrf_actions']
        s_actions = ann_2[i]['umrf_actions']
        if len(b_actions) == len(s_actions):
            y = range(0, len(b_actions))
            for j in y:
                if b_actions[j]['package_name'] == s_actions[j]['package_name']:
                    acc.append(1)
                    sum = 1 + sum
                else:
                    acc.append(0)
    accuracy = sum/len(acc)
    return accuracy



if __name__ == '__main__':
    sentences = open_ann_file('c:/Users/321785/PycharmProjects/URA_anno_eval_11_16/group_1_annotation_list.txt')

    b_json_anns = open_annotations(WindowsPath('c:/Users/321785/PycharmProjects/URA_anno_eval_11_16/Bethany'), 'bethany')
    b_filtered_sentences = compare_against_ann_file(sentences, b_json_anns)

    s_json_anns = open_annotations(WindowsPath('c:/Users/321785/PycharmProjects/URA_anno_eval_11_16/Sid'), 'sid')
    s_filtered_sentences = compare_against_ann_file(sentences, s_json_anns)

    b, s = check_aligned(b_filtered_sentences, s_filtered_sentences)
    print(check_acc(b, s))
