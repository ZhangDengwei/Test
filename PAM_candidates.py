# -*- coding: utf-8 -*-
"""
-------------------------------------------------
    File Name:      PAM_candidates
    Description:
    Author:         Dengwei Zhang
    Date:           2019/10/16
    E-mail:         scdzzdw@163.com
-------------------------------------------------
"""

import re
import argparse


def design_pam(file_in_1, file_in_2, file_out):
    with open(file_in_1, 'r') as fi_1, open(file_in_2, 'r') as fi_2, open(file_out, 'a') as fo:
        # get target sequence
        target_seq = ''
        for i in fi_1:
            target_seq += i.rstrip('\n').upper()
        target_seq_rc = target_seq.translate(str.maketrans('ATCG', 'TAGC'))[::-1]

        # get PAM sequence
        pam = {}
        for i in fi_2:
            try:
                items = i.rstrip('\n').split()
                name = items[0]
                rank = items[1]
                pam[name] = str(rank)
            except IndexError:
                raise Exception("There are some problems in the input PAM file!")

        # scan the potential PAMs on target sequence
        pam_candidates, pam_candidates_rc = [], []
        for k, j in pam.items():
            pattern = re.compile(k)
            k_pam = [(i.group(), i.start(), i.end()) for i in pattern.finditer(target_seq)]
            k_pam_rc = [(i.group(), i.start(), i.end()) for i in pattern.finditer(target_seq_rc)]
            pam_candidates.extend(k_pam)
            pam_candidates_rc.extend(k_pam_rc)

        # output result
        print('PAM\tRanking\tStart\tEnd\tStrand', file=fo)
        for i in sorted(pam_candidates, key=lambda k: k[1]):
            print(i[0], pam[i[0]], i[1], i[2], 'Top', sep='\t', file=fo)
        for i in sorted(pam_candidates_rc, key=lambda k: k[1]):
            print(i[0], pam[i[0]], '-' + str(i[1]), '-' + str(i[2]), 'Bottom', sep='\t', file=fo)


def main():
    parser = argparse.ArgumentParser(description='Extracting potential PAM sequence on particular target sequence.')
    parser.add_argument('--target', help='the file of target sequence', required=True)
    parser.add_argument('--pam', help='the tab-delimited file storing PAM ranking', required=True)
    parser.add_argument('--out', help='Output filename', required=True)

    args = parser.parse_args()

    design_pam(args.target, args.pam, args.out)


if __name__ == "__main__":
    main()









