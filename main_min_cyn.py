import os
import string
from pathlib import WindowsPath
import json


def open_annotations(wpath: WindowsPath, name: str):
    # CYNTHIA SPECIFIC
    if name == 'cynthia':
        json_list = [pos_json for pos_json in os.listdir(wpath) if pos_json.endswith('.json')]
        json_list_cropped = [e[9:] for e in json_list]
        json_list_cropped = [e[:-11] for e in json_list_cropped]
        json_cropped_int = [int(x) for x in json_list_cropped]
        json_cropped_int.sort()
        json_cropped_int = [str(x) for x in json_cropped_int]

        x = range(len(json_cropped_int))
        beth_file_names = []
        for i in x:
            beth_file_string = 'umrf_cyn_' + json_list_cropped[i] + '.umrfg.json'
            beth_file_names.append(beth_file_string)

        json_dicts = []
        for json_file in beth_file_names:
            with open('c:/Users/321785/PycharmProjects/URA_anno_eval_11_16/Cynthia/' + json_file, 'r') as f:
                json_string = f.read()
                json_dict = json.loads(json_string)
                json_dicts.append(json_dict)

    # SID SPECIFIC
    if name == 'minsoo':
        json_list = [pos_json for pos_json in os.listdir(wpath) if pos_json.endswith('.json')]
        json_list_cropped = [e[11:] for e in json_list]
        json_list_cropped = [e[:-18] for e in json_list_cropped]
        json_cropped_int = [int(x) for x in json_list_cropped]
        json_cropped_int.sort()
        # json_cropped_int = [str(x) for x in json_cropped_int]

        x = range(len(json_cropped_int))
        sid_file_names = []
        for i in x:
            sid_file_string = 'umrf_graph_' + str(json_cropped_int[i]) + '_Minsoo.umrfg.json'
            sid_file_names.append(sid_file_string)

        json_dicts = []
        for json_file in sid_file_names:
            with open('c:/Users/321785/PycharmProjects/URA_anno_eval_11_16/Minsoo/' + json_file, 'r') as f:
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
        correct = False
        sentence = sentence.lower()
        desc = json_anns[i]['umrf_actions'][0]['description'].lower().strip()
        sentence_nopunc = "".join(c for c in sentence if c not in ('!', '.', ':', ',')).lower()
        if desc in sentence:
            pruned_sentences.append(json_anns[i])
            correct = True
        elif desc in sentence_nopunc:
            pruned_sentences.append(json_anns[i])
            correct = True
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
    sentences = open_ann_file('c:/Users/321785/PycharmProjects/URA_anno_eval_11_16/group_2_annotation_list.txt')

    c_json_anns = open_annotations(WindowsPath('c:/Users/321785/PycharmProjects/URA_anno_eval_11_16/Cynthia'), 'cynthia')
    c_filtered_sentences = compare_against_ann_file(sentences, c_json_anns)

    m_json_anns = open_annotations(WindowsPath('c:/Users/321785/PycharmProjects/URA_anno_eval_11_16/Minsoo'), 'minsoo')
    m_filtered_sentences = compare_against_ann_file(sentences, m_json_anns)

    c, m = check_aligned(c_filtered_sentences, m_filtered_sentences)
    print(check_acc(c, m))
