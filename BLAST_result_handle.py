import xml.etree.ElementTree as ET
import pdb
import string
import argparse
import os 
import time

#pdb.set_trace()

# Parse customized input parameters
parser = argparse.ArgumentParser(description='Input Identity(%) by your own.')
parser.add_argument('--Identity', type=float, default=0.0, help='Identity percent')
args = parser.parse_args()

Identity_condition = args.Identity


# import '.xml' to python
res = ET.parse('blast_outfmt5.xml').getroot()


# get all your sequence data into 'lst_Iteration'
lst_Iteration = res.findall('BlastOutput_iterations/Iteration')
print '# The number of "Iteration" (#yourRNA): ', len(lst_Iteration)


for iteration in lst_Iteration:
    # get info about your sequences
    iteration_iterNum = iteration.find('Iteration_iter-num').text
    iteration_queryID = iteration.find('Iteration_query-def').text
    Iteration_queryLen = iteration.find('Iteration_query-len').text

    # get info about all 'Hit' (the index of subject)
    lst_Hits = iteration.findall('Iteration_hits/Hit')

    # for each matched subject, get info about alignments
    flg_printQueryID = False
    for hits in lst_Hits:
        flg = True
        Hit_len = hits.find('Hit_len').text
        lst_hsp = hits.findall('Hit_hsps/Hsp')
        name = hits.find('Hit_def').text
        AL = 0
        identity = 0
        for hsp in lst_hsp:                     
            align_len = hsp.find('Hsp_align-len').text     
            AL = AL + int(align_len)
            identity = identity + int(hsp.find('Hsp_identity').text)       
        Iden = 1.0*100*identity/AL


        # check for several conditions
        if Iden < Identity_condition:
            flg = False

        # if the 'iteration' satisfies all these conditions, then output the name of 'iteration'
        if flg == True:
            flg_printQueryID = True

            words = iteration_queryID.split(' ',1)
            queryID = words[0]
            print '[FOUND] The desired iteration name:',queryID
            print '|- Name of Hit:', name, ' | len(Hit):',Hit_len,' | ',len(lst_hsp),'alignments (hsp) matched subject.'
            print '  |-- Alignment length (AL, bp):',AL
            print '  |-- Identity (% of match):',Iden
            print '\n'

            with open('result.txt','a') as result_file:
                result_file.write('[FOUND] The desired iteration name: '+str(queryID) + '\n')
                result_file.write('|- Name of Hit: ' + str(name) + ' | len(Hit):' + str(Hit_len) + ' | ' + str(len(lst_hsp)) + 'alignments (hsp) matched subject.' + '\n')
                result_file.write('  |-- Alignment length (AL):' + str(AL) + '\n')
                result_file.write('  |-- Identity (% of match):' + str(Iden) + '\n')
                result_file.write('\n')
                result_file.close()

            break     

    if flg_printQueryID == True:   
        with open('SeqID.txt','a') as seqID_file:
            seqID_file.write(str(queryID) + '\t' + str(Iteration_queryLen) + '\t' + str(Iden) + '\n')
            seqID_file.close()
