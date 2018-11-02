from backend import *


part = ["111","PC4-19200S","Lenovo","SO-DIMM","8GB","8GB DDR4 2400 SoDIMM","FALSE","TRUE"]

conn = create_connection()

def test1():
    """Test adding parts to database"""
    add_part("mem", part)
    try:
        assert part_in_db(conn, "mem", "111") == True
        print("Add part: Passed!\n")
    except AssertionError as e:
        print("Add part:Failed!\n")
        print(str(e))

        
def test2():
    """Test removed parts from database"""
    remove_part("mem", "111")
    try:
        assert part_in_db(conn, "mem", "111") == False
        print("Remove part: Passed!\n")
    except AssertionError as e:
        print("Remove part: Failed!\n")
        print(str(e))

        
def test3():
    """Test import from csv"""
    import_from_csv(r".\import\TEST.csv")
    try:
        assert part_in_db(conn, "test", "123") == True
        assert part_in_db(conn, "test", "456") == True
        assert part_in_db(conn, "test", "789") == True
        remove_part("test", "123")
        remove_part("test", "456")
        remove_part("test", "789")
        assert part_in_db(conn, "test", "123") == False
        assert part_in_db(conn, "test", "456") == False
        assert part_in_db(conn, "test", "789") == False
        print("Import: Passed!\n")
    except AssertionError as e:
        print("Import: Failed!\n")
        print(str(e))

        
def test4():
    """Test checking listin of subs"""
    import_from_csv(r".\import\hdd.csv")
    part_needing_sub = ["111","Acer","SATA","500","1000","5400","SSHD","2.5","7","SATA III","","FALSE","TRUE"]
    sub = ["112","Acer","SATA","500","1000","5400","SSHD","2.5","7","SATA III","","FALSE","TRUE"]
    also_a_sub = ["113","CVO","SATA","500","1000","5400","SSHD","2.5","7","SATA III","","FALSE","TRUE"]
    not_a_sub = ["222","Acer","SATA","500","","5400","SSHD","2.5","7","SATA III","","TRUE","FALSE"]
    also_not_a_sub = ["223","Acer","SATA","","500","5400","SSD","2.5","7","SATA III","","FALSE","FALSE"]
    
    add_part("hdd", part_needing_sub)
    add_part("hdd", sub)
    add_part("hdd", also_a_sub)
    add_part("hdd", not_a_sub)
    add_part("hdd", also_not_a_sub)
    subs = list_subs("hdd", part_needing_sub[0])
    try:
        assert any(lst[1] == "112" for lst in subs) == True
        assert any(lst[1] == "113" for lst in subs) == True
        assert any(lst[1] == "222" for lst in subs) == False
        assert any(lst[1] == "223" for lst in subs) == False
        print("List subs: Passed!\n")
    except AssertionError as e:
        print("List subs: Failed!\n")
        print(str(e))


    
#test1()
#test2()
#test3()    
test4()

remove_table("hdd")
#remove_table("mem")
print("Table purged\n")

close_connection(conn)
