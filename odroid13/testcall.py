from subprocess import call

cmd1 = "cd /media/odroid/CORSAIR"
cmd2 = "ls"
cmd = cmd1 + '''
''' + cmd2

call(cmd, shell=True)
"""
cmd = '''
cd /media/odroid/CORSAIR

'''

call(cmd, shell=True)
"""
