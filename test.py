import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import iamend_ci as ci

exp=ci.Experimento(sys.argv[1])
print(exp.info)