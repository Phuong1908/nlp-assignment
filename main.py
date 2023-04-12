from models.parser import Token, Category, Tense, Parser,Prep_SEM, Verb_SEM
import pdb
from models.database import retrieve_result

CAU_1 = "=======CAU 1======== \n"
CAU_2 = "=======CAU 2======== \n"
CAU_3 = "=======CAU 3======== \n"
CAU_4 = "=======CAU 4======== \n"
CAU_5 = "=======CAU 5======== \n"
CAU_6 = "=======CAU 6======== \n"


def write_to_file(filename,my_strs):
    file = open(f"outputs/{filename}","a")
    file.writelines(my_strs) 
    file.close()

if __name__ == "__main__":
    text = "Xe bus nào đến thành phố Huế lúc 20:00HR"
    input_1 = [
        Token("Xe bus",Category.NOUN,None, 1),
        Token("nào", Category.QDET,None,2),
        Token("đến", Category.VERB, Verb_SEM.ARRIVE,3),
        Token("thành phố", Category.NOUN,None,4),
        Token("Huế", Category.PRO_LOC,None,5),
        Token("lúc", Category.PREP_TIME,None,6),
        Token("20:00HR", Category.PRO_TIME,None,7)
    ]
    # parser_1 = Parser(input_1)
    # parser_1.produce()
    # write_to_file("output_a.txt",[CAU_1, parser_1.map_to_GR(),'\n'])
    # write_to_file("output_b.txt",[CAU_1, parser_1.map_to_LF(), '\n']) 
    # write_to_file("output_c.txt",[CAU_1, parser_1.map_to_SP(), '\n']) 
    # write_to_file("output_d.txt",[CAU_1, retrieve_result(parser_1.sem_procedure), '\n']) 

    text_2 = "Thời gian xe bus B3 từ Đà Nẵng đến Huế"
    input_2 = [
        Token("Thời gian",Category.QDET,None,1),
        Token("xe bus", Category.NOUN,None,2),
        Token("B3", Category.PRO_BUS, None,3),
        Token("từ", Category.PREP_LOC,None,4),
        Token("Đà Nẵng", Category.PRO_LOC,None,5),
        Token("đến", Category.VERB,Verb_SEM.ARRIVE,6),
        Token("Huế", Category.PRO_LOC,None,7)
    ]
    # parser_2 = Parser(input_2)
    # parser_2.produce()
    # print(parser_2)
    # parser_2.map_to_GR()
    # parser_2.map_to_LF()
    # parser_2.map_to_SP()
    # print(retrieve_result(parser_2.sem_procedure))

    text_3 = "Xe bus nào đến thành phố Hồ Chí Minh"
    input_3 = [
        Token("Xe bus",Category.NOUN,None,1),
        Token("nào", Category.QDET,None,2),
        Token("đến", Category.VERB,Verb_SEM.DEPART ,3),
        Token("thành phố", Category.NOUN,None,4),
        Token("Hồ Chí Minh", Category.PRO_LOC,None,5)
    ]

    # parser_3 = Parser(input_3)
    # parser_3.produce()
    # write_to_file("output_a.txt",[CAU_3, parser_3.map_to_GR(),'\n'])
    # write_to_file("output_b.txt",[CAU_3, parser_3.map_to_LF(), '\n']) 
    # write_to_file("output_c.txt",[CAU_3, parser_3.map_to_SP(), '\n']) 
    # write_to_file("output_d.txt",[CAU_3, retrieve_result(parser_3.sem_procedure), '\n']) 


    text_4 = "Những xe bus nào đi đến Huế"
    input_4 = [
        Token("Những",Category.DET,None,1),
        Token("xe bus", Category.NOUN,None,2),
        Token("nào", Category.QDET, None,3),
        Token("đi", Category.VERB,Verb_SEM.ARRIVE,4),
        Token("đến", Category.PREP_LOC,Prep_SEM.TO,5),
        Token("thành phố", Category.NOUN,None,6),
        Token("Hồ Chí Minh", Category.PRO_LOC,None,7)
    ]
    parser_4 = Parser(input_4)
    parser_4.produce()
    write_to_file("output_a.txt",[CAU_4, parser_4.map_to_GR(),'\n'])
    write_to_file("output_b.txt",[CAU_4, parser_4.map_to_LF(), '\n']) 
    write_to_file("output_c.txt",[CAU_4, parser_4.map_to_SP(), '\n']) 
    write_to_file("output_d.txt",[CAU_4, retrieve_result(parser_4.sem_procedure), '\n']) 

    text_5 = "Những xe nào xuất phát từ thành phố Hồ Chí Minh"
    input_5 = [
        Token("Những",Category.DET,None,1),
        Token("xe", Category.NOUN,None,2),
        Token("nào", Category.QDET, None,3),
        Token("xuất phát", Category.VERB,Verb_SEM.DEPART,4),
        Token("từ", Category.PREP_LOC,Prep_SEM.FROM ,5),
        Token("thành phố", Category.NOUN,None,6),
        Token("Hồ Chí Minh", Category.PRO_LOC,None,7)
    ]
    parser_5 = Parser(input_5)
    parser_5.produce()
    write_to_file("output_a.txt",[CAU_5, parser_5.map_to_GR(),'\n'])
    write_to_file("output_b.txt",[CAU_5, parser_5.map_to_LF(), '\n']) 
    write_to_file("output_c.txt",[CAU_5, parser_5.map_to_SP(), '\n']) 
    write_to_file("output_d.txt",[CAU_5, retrieve_result(parser_5.sem_procedure), '\n']) 


    text_6 = "Những xe nào đi từ Đà nẵng đến thành phố Hồ Chí Minh"
    input_6 = [
        Token("Những",Category.DET,None,1),
        Token("xe", Category.NOUN,None,2),
        Token("nào", Category.QDET, None,3),
        Token("đi", Category.VERB, Verb_SEM.DEPART,4),
        Token("từ", Category.PREP_LOC, Prep_SEM.FROM,5),
        Token("Đà Nẵng", Category.PRO_LOC,None,6),
        Token("đến", Category.PREP_LOC,Prep_SEM.TO,7),
        Token("Hồ Chí Minh", Category.PRO_LOC,None,8)
    ]
    parser_6 = Parser(input_6)
    parser_6.produce()
    write_to_file("output_a.txt",[CAU_6, parser_6.map_to_GR(),'\n'])
    write_to_file("output_b.txt",[CAU_6, parser_6.map_to_LF(), '\n']) 
    write_to_file("output_c.txt",[CAU_6, parser_6.map_to_SP(), '\n']) 
    write_to_file("output_d.txt",[CAU_6, retrieve_result(parser_6.sem_procedure), '\n']) 


