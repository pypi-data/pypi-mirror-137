
# -*- coding: utf-8 -*-
import os , sys , codecs
import pdb
import re
import glob
#Program 1 | Library settings
import pathlib
import os
import pdb
import re

def swritructure_main(arg_1 = 'aaaaa.py'):

    print('sys.argv[1]:', str(arg_1))

    def from_file_list_export(start_file):
        # File extraction list with all directories below
        all_directory_list = []

        #Program 2 ｜ main procedure

        Folderpath = os.getcwd()#Specify the target folder


        #Program 3 | Functions for writing folders and files for each hierarchy
        def GetFolderFileNames(path, kaiso, all_directory_list_arg):
            # files = pathlib.Path(path).glob('*')#Get folders and files in that hierarchy
            files = os.listdir(path)#Get folders and files in that hierarchy
            all_directory_list_ch = []

            # Program 4 | Export folders and files one by one
            for file in files:
                output = file
                all_directory_list_ch.append(str(path) + '\\' + output)
                all_directory_list_ch.append(kaiso)
                all_directory_list_arg.append(all_directory_list_ch)
                all_directory_list_ch = []
                # In the case of Program 5 | Folder, call GetFolderFileNames (Program 6) for the folders and files in the hierarchy below it.
                #if not file[:3] == '.xml' or file[:3] == '.csv' or file[:3] == '.xml' or file[:3] == '.xml' or file[:3] == '.xml' or :
                if os.path.isdir(file) == True:

                    # print('file:',file)
                    GetFolderFileNames(path + "\\" + file, kaiso+1, all_directory_list_arg)
            return all_directory_list_arg

        all_directory_list = GetFolderFileNames(Folderpath, 0, all_directory_list)#GetFolderFileNamesCall (program 3)

        files = glob.glob("./*")

        for file in files:
            print(file)

        # Fill the list with the list of files in the current directory
        current_directory_files_list = os.listdir('./')


        ############################################################
        #!/usr/bin/python
        # -*- coding: utf-8 -*-
        # vim: fileencoding=utf-8

        grep_result = []
        def grep_method(search_dir, search_pattern):
            output_list = []
            DIR_NAME = search_dir
            SEARCH_WORD = search_pattern
            #FLAG_STDOUT = True
            write = sys.stdout.write
            for dirpath, dirs, files in os.walk(DIR_NAME):
                for fn in files:
                    path = os.path.join(dirpath, fn)
                    count = 0
                    enc = 'utf-8'
                    try:
                        for l in codecs.open(path, 'r', enc):
                            count = count + 1
                            if SEARCH_WORD in l:
                                output = ''
                                try:
                                    output = '"' + path + '","' + str(count) + '","' + SEARCH_WORD + '","' + l.replace('"',"'").replace('\r','').replace('\n','') + '"\r\n'
                                    # print('output:', output)
                                    output_list.append(str(path))
                                    output_list.append(str(count))
                                    output_list.append(SEARCH_WORD)
                                    output_list.append(str(l.replace('"',"'").replace('\r','').replace('\n','')))
                                    grep_result.append(output_list)
                                    output_list = []       
                                except:
                                    continue
                                # if FLAG_STDOUT == True:
                                #     write(output)
                                # out.write(output)
                                
                    except:
                        continue
            return grep_result

        #grep_result = grep_method('./', "getTopURLStatus(")

        # ['./testfolder\\testfolder2\\testfile2.txt', '2', 'ge


        # print('This is the start of the start file')

        # print('Fill the from_list list with the py file names that come after from')
        def make_from_list(arg_file):
            f = open(arg_file, 'r', encoding='utf-8')
            datalist = f.readlines()

            # Deleted the area surrounded by "" "" ""
            datalist = re.sub(r'\"\"\"(.*?)\"\"\"','',str(datalist))

            # Unification of line breaks
            datalist = datalist.replace('\\r\\n','\\r')
            datalist = datalist.replace('\\n','\\r')

            # Delete everything surrounded by # and \ r
            datalist = re.sub(r'#(.*?)\\r','',datalist)

            while_flag = True
            from_list = []
            from_list_ch = []
            datalist_from_import = datalist
            while(while_flag):
                # Extract the related py file name described in import from from
                try:
                    datalist_from_import = datalist_from_import.replace('from ','fffff')
                    datalist_from_import = datalist_from_import.replace(' import','iiiii')
                except:
                    print('from etc. None')
                try:
                    datalist_from_file = (re.search(r'fffff(.*?)iiiii', datalist_from_import))[0].replace('fffff','').replace('iiiii','')
                    # print(datalist_from_file)
                    datalist_import_file = (re.search(r'iiiii(.*?)\\r', datalist_from_import))[0].replace('fffff','').replace('iiiii','').replace('\\r','')
                    # print(datalist_import_file)
                    from_list_ch.append(datalist_from_file)
                    from_list_ch.append(datalist_import_file)
                    from_list.append(from_list_ch)
                    from_list_ch = []
                    datalist_from_import = datalist_from_import.replace('fffff' + datalist_from_file + 'iiiii', '')
                except:
                    print('-from- py file name -import- no longer exists')
                    while_flag = False
                    break
            f.close()
            return from_list

        from_file_list = make_from_list(start_file)

        return from_file_list

    start_file = arg_1 # Webscrape.py
    from_file_list = from_file_list_export(start_file)

    # (Pdb) from_file_list
    # [['createData', ' getTopURLStatus, getProfileInformation'], ['ccccccc', ' ttttttttt']]
    file_last = open('structure.txt', 'w')
    file_last.write('------------------------------------------------------------' + '\r\n')
    file_last.write(arg_1 + '\r\n')


    '''
    Webscrape.py(start file)
        |
        ∟ createDate.py(from information)
        |   |
        |   checkTorihiki(import information)
        |   |
        |   getProfileInformation(import information)
        |
        ∟ ccccccc.py(from information)
            |
            ttttttttt(import information)
    '''
    from_file_list_next = []

    file_last.write('     |' + '\r\n')
    if from_file_list != []:

        for num, n in enumerate(from_file_list):

            file_last.write('    ∟' + str(from_file_list[int(num)][0]) + '.py\r\n')
            # Webscrape.py(start file)
            #     |
            #     ∟ createDate.py(from information)
            if ',' in from_file_list[int(num)][1]:

                # When there is more than one import
                import_list = from_file_list[int(num)][1].split(',')
                for m in import_list:

                    # After importing into one
                    import_method = m.strip() # Eliminate front and back blanks

                    if int(num) + 1 > len(from_file_list):

                        # When the next from file does not exist
                        file_last.write('        |' + '\r\n')
                        file_last.write('        ' + str(import_method) + '()\r\n')

                    else:
                        # When there is the next from file
                        file_last.write('    |   |' + '\r\n')
                        file_last.write('    |   ' + str(import_method) + '()\r\n')

                        from_file_list_next = from_file_list_export(str(from_file_list[int(num)][0]) + '.py')

                        # str(from_file_list[int(num)][0]) + '.py' 's str(import_method) + '()' 's Read to the next method
                        with open('./' + str(from_file_list[int(num)][0]) + '.py', encoding='utf-8', errors='ignore') as f:

                            for line_ch in f:
                                # print(line_ch)
                                # If def comes at the beginning, it's coming to the next method, so skip it.
                                if (line_ch.strip())[:3] == 'def':
                                    continue                          
                                for num_ffln, from_file_list_next_ch in enumerate(from_file_list_next):
                                    
                                    if from_file_list_next_ch[1].strip() in line_ch:
                                        method_name = from_file_list_next_ch[1].strip()
                                        # There is a py file name in from in the corresponding line read
                                        #if from_file_list_next_ch[1].strip() + '(' in line_ch:
                                        # When there is something in front, there is a half-width space after the specified method name, and there is something after it
                                        if re.search(rf'\b(?=\w)(.*?){method_name}(.*?)\((.*?)(?!\w)', str(line_ch)):
                                            # print('Bingo！！！！！！！！！！')

                                            # In addition. Extracted from commas (because there were things up to parentheses)
                                            method_text = re.search(rf'\b(?=\w)(.*?){method_name}(.*?)\((.*?)(?!\w)', str(line_ch))

                                            if int(num_ffln) + 1 == len(from_file_list_next):
                                                # When the next from file does not exist
                                                file_last.write('    |    |  　|' + '\r\n')
                                                file_last.write('    |    |    ∟' + str(from_file_list_next_ch[0]) + '.py\r\n')
                                                file_last.write('    |    |    　         |' + '\r\n')
                                                file_last.write('    |    |               ' + str(method_name) + '()\r\n')
                                            else:
                                                # When there is the next from file
                                                file_last.write('    |    |  　|' + '\r\n')
                                                file_last.write('    |    |    ∟' + str(from_file_list_next_ch[0]) + '.py\r\n')
                                                file_last.write('    |    |  　|          |' + '\r\n')
                                                file_last.write('    |    |    |          ' + str(method_name) + '()\r\n')
            else:
                import_method = from_file_list[int(num)][1]
                # After importing into one
                import_method = m.strip() # Eliminate front and back blanks

                if int(num) + 1 > len(from_file_list):

                    # When the next from file does not exist
                    file_last.write('        |' + '\r\n')
                    file_last.write('        ' + str(import_method) + '()\r\n')

                else:
                    # When there is the next from file
                    file_last.write('    |   |' + '\r\n')
                    file_last.write('    |   ' + str(import_method) + '()\r\n')

                    from_file_list_next = from_file_list_export(str(from_file_list[int(num)][0]) + '.py')

                    with open('./' + str(from_file_list[int(num)][0]) + '.py', encoding='utf-8', errors='ignore') as f:

                        for line_ch in f:
                            # print(line_ch)
                            
                            for num_ffln, from_file_list_next_ch in enumerate(from_file_list_next):
                                
                                if from_file_list_next_ch[1].strip() in line_ch:
                                    method_name = from_file_list_next_ch[1].strip()
                                    print('from_file_list_next_ch[1].strip()■■■：', from_file_list_next_ch[1].strip())
                                    print('line_ch■■■:', line_ch)

                                    if re.search(rf'\b(?=\w)(.*?){method_name}(.*?)\((.*?)(?!\w)', str(line_ch)):
                                        # print('Bingo！！！！！！！！！！')

                                        # In addition. Extracted from commas (because there were things up to parentheses)
                                        method_text = re.search(rf'\b(?=\w)(.*?){method_name}(.*?)\((.*?)(?!\w)', str(line_ch))

                                        if int(num_ffln) + 1 == len(from_file_list_next):
                                            # When the next from file does not exist
                                            file_last.write('    |        ∟' + str(from_file_list_next_ch[0]) + '.py\r\n')
                                            file_last.write('            　         |' + '\r\n')
                                            file_last.write('                       ' + str(method_name) + '()\r\n')
                                        else:
                                            # When there is the next from file
                                            file_last.write('    |        ∟' + str(from_file_list_next_ch[0]) + '.py\r\n')
                                            file_last.write('    |      　|         |' + '\r\n')
                                            file_last.write('    |        |         ' + str(method_name) + '()\r\n')

                # When there is only one import
                import_method = from_file_list[int(num)][1].strip() # Eliminate front and back blanks
    
                if int(num) + 1 == len(from_file_list):
                    # When the next from file does not exist
                    file_last.write('        |' + '\r\n')
                    file_last.write('        ' + str(import_method) + '()\r\n')
                else:
                    # When there is the next from file
                    file_last.write('    |   |' + '\r\n')
                    file_last.write('    |   ' + str(import_method) + '()\r\n')

    file_last.close()
    print('◆◆◆◆◆◆Structured.txt is output. Please confirm.◆◆◆◆◆◆')

