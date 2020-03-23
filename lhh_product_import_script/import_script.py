import functools
import xmlrpc.client
from pymssql import connect


def sf(s):
    import code
    code.register()
    if type(s) != str or all(ord(c) < 128 for c in s):
        return s  # 如果全部是ASCII字符则不需要转换
    t = s.encode('mssql_latin1').decode('hkscs')
    return t


# MSSQL服务器配置
SERVER = '192.168.91.1'
UID = 'sa'
PWD = 'password'
DATABASE = 'LHH_live'

# xmlrpc配置
HOST = 'localhost'
PORT = 8069
DB = 'demo'
USER = PASS = 'admin'
ROOT = 'http://%s:%d/xmlrpc/' % (HOST, PORT)

conn = connect(SERVER, UID, PWD, DATABASE)
cursor = conn.cursor()

uid = xmlrpc.client.ServerProxy(ROOT + 'common').login(DB, USER, PASS)
call = functools.partial(xmlrpc.client.ServerProxy(
    ROOT + 'object').execute, DB, uid, PASS)

if __name__ == '__main__':
    with conn:
        with cursor:
            cursor.execute("""SELECT [No_]                     
                                    ,[Short English Description 1]  
                                    ,[English Description 2]        
                                    ,[Base Unit of Measure]         
                                    ,[Color Name]                   
                                    ,[Size]                         
                                    ,[Series Name]                  
                                    ,[Brand Name]				  
                                    ,[Category Level 1 Name]        
                                    ,[Category Level 2 Name]        
                                    ,[Category Level 3 Name]        
                                    ,[Category Level 4 Name]        
                                    ,[A1]
                                    ,[A2]
                                    ,[A3]
                                    ,[A4]
                                    ,[A5]
                                    ,[Chinese Description 1]   
                                    ,[Chinese Description 2]      
                                    ,[Remarks]                      
                                    ,[Picture Link]
                            FROM [LHH_Live].[dbo].[LHH$Item]""")
            data = cursor.fetchall()
            for i in data:
                product_id = call('lhh.product', 'create', {'name': i[0],
                                                            's_eng_desc1': sf(i[1]),
                                                            'eng_desc2': sf(i[2]),
                                                            'uom': i[3],
                                                            'color': sf(i[4]),
                                                            'size': i[5],
                                                            'series': sf(i[6]),
                                                            'brand': sf(i[7]),
                                                            'cat_l1': sf(i[8]),
                                                            'cat_l2': sf(i[9]),
                                                            'cat_l3': sf(i[10]),
                                                            'cat_l4': sf(i[11]),
                                                            'a1': sf(i[12]),
                                                            'a2': sf(i[13]),
                                                            'a3': sf(i[14]),
                                                            'a4': sf(i[15]),
                                                            'a5': sf(i[16]),
                                                            'chn_desc1': sf(i[17]),
                                                            'chn_desc2': sf(i[18]),
                                                            'remarks': sf(i[19]),
                                                            'pic_link': i[20]})
                print(product_id, i[0])
