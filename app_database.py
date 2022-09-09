import sqlite3
from migrations import total_migrations, unrun_migrations

class AppDataBase():

    def __init__(self, db_file="", _same_thread=False):
        self.db_file = db_file
        self.con = sqlite3.connect(self.db_file, check_same_thread=_same_thread)
        self.cur = self.con.cursor()


    def migrate(self):
        new_unrun = {}
        new_total = {}
        print(total_migrations)
        new_total.update(total_migrations)
        if len(unrun_migrations.keys()) > 0:
            for num, cmd in unrun_migrations.items():
                try:
                    print(f"{num} trying: {cmd}")
                    self.cur.execute(cmd)
                    new_total[str(num)] = cmd
                except:
                    print(f"{num} failed ERROR: {cmd}")
                    new_unrun[str(num)] = cmd
                    new_total[str(num)] = cmd
        else:
            for num, cmd in total_migrations.items():
                try:
                    print(f"{num} trying: {cmd}")
                    self.cur.execute(cmd)
                    new_total[str(num)] = cmd
                except:
                    print(f"{num} failed ERROR: {cmd}")
                    new_unrun[str(num)] = cmd
                    new_total[str(num)] = cmd
        self.con.commit()
        with open("migrations.py", "w") as f:
            f.write("total_migrations = {\n")
            for i in range(len(new_total)):
                if i != (len(new_total)-1):
                    f.write('''"{}": "{}",\n'''.format(i,new_total[str(i)]))
                else:
                    f.write('''"{}": "{}"'''.format(i,new_total[str(i)]))
            f.write("}")
                    
            f.write(f"\n\nunrun_migrations = {new_unrun}\n")
