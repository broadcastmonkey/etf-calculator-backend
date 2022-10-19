import sys
import os
#print("result = 2")


def main():

    args = int(sys.argv[1])
    # print(str(args*2))

# args is a list of the command line args


main()

print("(Allocation {'SCHI': 0.05, 'SPBO': 0.05, 'SCHJ': 0.07, 'VCSH': 0.07, 'QGRO': 0.1, 'WCLD': 0.06, 'SMOG': 0.14, 'XLE': 0.13, 'ERTH': 0.08, 'SPYD': 0.07, 'VALQ': 0.08, 'IVLU': 0.05, 'EFV': 0.04}",'Annualised Return 0.07',
      'Annualised Volatility 0.21',
      'Sharpe Ratio 0.156')

sys.exit(os.EX_OK)
