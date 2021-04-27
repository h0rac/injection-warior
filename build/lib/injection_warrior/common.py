import sys
from termcolor import colored
import json

class Common():
    def __init__(self):
        pass
    
    def _parse_template(self, payloads=[], **kwargs):

        if not isinstance(payloads, list):
            print(colored(
                "[-] Incorrect type for payloads, must be list", "red"))
            sys.exit(0)

        values = []
        temp = json.dumps(payloads)
        temp = temp.replace("[DELIMITER]", kwargs.get('delimiter') if  kwargs.get('delimiter') != None else '+')
        temp = temp.replace("[COMMENT]",kwargs.get('comment') if kwargs.get('comment') != None else '--')
        temp = temp.replace("[COMMA]", kwargs.get('comma') if kwargs.get('comma') != None else ',')
        temp = temp.replace("[QUOTE]", kwargs.get('quote') if kwargs.get('quote') != None else "'")
        temp = temp.replace("[NULL]", self._gen_nulls(
            nulls=kwargs.get('nulls') if kwargs.get('nulls') != None else 1,
            delimiter=kwargs.get('delimiter') if kwargs.get('delimiter') != None else '+', 
            oracle=kwargs.get('oracle') if kwargs.get('oracle') != None else False, 
            comment=kwargs.get('comment') if kwargs.get('comment') != None else '--'))
        temp = temp.replace("[TABLE_NAME]", kwargs.get('table_name') if  kwargs.get('table_name') else '')
        temp = temp.replace("[COLUMN_NAME_1]", kwargs.get('column_name_1') if kwargs.get('column_name_1') else '')
        temp = temp.replace("[COLUMN_NAME_2]", kwargs.get('column_name_2') if kwargs.get('column_name_2') else '')
        temp = temp.replace("[ITER]", str(kwargs.get('iterations')) if kwargs.get('iterations') != None else '1')
        temp = temp.replace("[CHAR]", str(kwargs.get('char') if kwargs.get('char') != None else ''))
        temp = temp.replace("[SLEEP]", str(kwargs.get('sleep') if kwargs.get('sleep') != None else 5))
        values = json.loads(temp)
        return values
    
    def _gen_nulls(self, nulls=1, delimiter="+", oracle=False, comma=",", comment="--"):
        payload = "{}NULL".format(comma) * nulls
        if oracle:
            payload = payload + delimiter+"FROM"+delimiter+"DUAL"+comment+delimiter
        else:
            payload = payload
            payload = payload.replace(comma, '', 1)
        return payload