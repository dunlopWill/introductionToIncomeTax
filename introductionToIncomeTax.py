
# Define variables
nonSavingsIncome = 40000 #Input non-savings income here (Example)
savingsIncome = 106 #Input savings income here (Example)
dividendIncome = 0 #Input dividend income (Example)

giftAidDonation = 0 #Input gift aid donation if any
electMCA = False #Election for married couples allowance made?
marriedCouplesAllowance = 8695 #Tax reducer available to married couples where one partner is born before 6th April 1935 and can be claimed by the partner with the higher net income
ceilingMCA = 28900 #MCA ceiling net income before reduce
miniumMCA = 3360 #MCA can't be reduced below this amount
transferMA = False #Note if elect MCA is true can't transfer MA
marriageAllowance = 1190 #2018/19 marriage allowance - if a partner has no tax liability or is only a bsic rate taxpaper, can transfer this amount of their personal allowance to their partner

standardPA = 11850 #Personal allowance for the tax year 2018/19
taxDeductedAtSource = 0 #e.g. PAYE

#Calculate net income
netIncome = nonSavingsIncome + savingsIncome + dividendIncome
print(f"Net income is: £{netIncome}")

#Calculate adjusted personal allowance
adjustedPA = 11850
ceilingPA = 100000 + standardPA * 2

if (netIncome <= 100000):
    adjustedPA = standardPA
elif (netIncome >= ceilingPA):
    adjustedPA = 0
else:
    adjustedPA = standardPA - (netIncome - 100000)/2
print(f"Adjusted personal allowance is: £{adjustedPA}")

#Calcualte taxable income by reducing each income type by the remaining adjusted personal allowance
taxableNSI = 0 #Taxable non-savings income
taxableSI = 0 #Taxable savings income
taxableDI = 0 #Taxable dividend income

if (nonSavingsIncome >= adjustedPA):
    taxableNSI = nonSavingsIncome - adjustedPA
    taxableSI = savingsIncome
    taxableDI = dividendIncome
else:
    taxableNSI = 0
    adjustedPA = adjustedPA - nonSavingsIncome
    if (savingsIncome >= adjustedPA):
        taxableSI = savingsIncome - adjustedPA
        taxableDI = dividendIncome
    else:
        taxableSI = 0
        adjustedPA = adjustedPA - savingsIncome
        if (dividendIncome >= adjustedPA):
            taxableDI = dividendIncome - adjustedPA
        else:
            taxableDI = 0

print(f"Taxable non-savings income is: £{taxableNSI}")
print(f"Taxable savings income is: £{taxableSI}")
print(f"Taxable dividend income is: £{taxableDI}")

taxableIncome = taxableNSI + taxableSI + taxableDI
print(f"Total taxable income is: £{taxableIncome}")

#Calculate income tax liability on taxable non-savings income
ceilingBRB = 34500 #Basic rate band ceiling for non-savings and savings income for the tax year 2018/19
ceilingHRB = 150000 #Higher rate band ceiling for non-savings and savings income for the tax year 2018/19

#Adjust bands for gift aid donation
if taxableIncome > ceilingBRB and taxableIncome < ceilingHRB:
    ceilingBRB = ceilingBRB + giftAidDonation * 100/80
elif taxableIncome > ceilingHRB:
    ceilingBRB = ceilingBRB + giftAidDonation * 100/80
    ceilingHRB = ceilingHRB + giftAidDonation * 100/80

liableNSI = 0

if (taxableNSI == 0):
    liableNSI = 0
elif (taxableNSI > 0 and taxableNSI <= ceilingBRB):
    liableNSI = taxableNSI * 0.2
elif (taxableNSI > ceilingBRB and taxableNSI <= ceilingHRB):
    liableNSI = ceilingBRB * 0.2 + (taxableNSI - ceilingBRB) * 0.4
else:
    liableNSI = ceilingBRB * 0.2 + (ceilingHRB - ceilingBRB) * 0.4 + (taxableNSI - ceilingHRB) * 0.45

print(f"Tax liability on taxable non-savings income is: £{liableNSI}")


#Keep track of how much taxableIncome has been taxed
cumulativeTaxed = 0
cumulativeTaxed = taxableNSI

#Establish starting rate band for taxable savings income
startingRateBand = 0 #Starting rate band (SRB) applies only to taxpayers with no more than £5000 of taxable non-savings income
if (taxableNSI <= 5000):
    startingRateBand = 5000 - taxableNSI
else:
    startingRateBand = 0

#Establish savings nil rate band for taxable savings income
savingsNRB = 0 #Savings nil rate band (NRB)
if (taxableIncome <= ceilingBRB): #If basic rate tax payer, savings NRB is £1000
    savingsNRB = 1000
elif (taxableIncome <= ceilingHRB): #If higher rate tax payer, savings NRB is £500
    savingsNRB = 500
else: #If additional rate tax payer, savings NRB is £0.
    savingsNRB = 0

#Reduce taxable savings income by SRB and NRB
if (taxableSI < startingRateBand + savingsNRB):
    cumulativeTaxed = cumulativeTaxed + taxableSI
    taxableSI = 0
else:
    taxableSI = taxableSI - startingRateBand - savingsNRB
    cumulativeTaxed = cumulativeTaxed + startingRateBand + savingsNRB

#Calculate savings income tax liablity
liableSI = 0;

if (taxableSI == 0): #...if taxable savings income is zero
    liableSI = 0
elif (cumulativeTaxed + taxableSI <= ceilingBRB): #...if adding taxable savings income is still within BRB
    liableSI = taxableSI * 0.2
elif (cumulativeTaxed + taxableSI <= ceilingHRB): #...if adding taxable income exceeds BRB but is still within HRB
    if (cumulativeTaxed <= ceilingBRB): #...if cumulativeTaxed is within BRB
        liableSI = (ceilingBRB - cumulativeTaxed) * 0.2 + (cumulativeTaxed + taxableSI - ceilingBRB) * 0.4
    else:
        liableSI = taxableSI * 0.4
elif (cumulativeTaxed + taxableSI > ceilingHRB): #...if adding taxable income exceeds HRB
    if (cumulativeTaxed <= ceilingBRB):
        liableSI = (ceilingBRB - cumulativeTaxed) * 0.2 + (ceilingHRB - ceilingBRB) * 0.4 + (cumulativeTaxed + taxableSI - ceilingHRB) * 0.45
    elif (cumulativeTaxed <= ceilingHRB):
        liableSI = (ceilingHRB - cumulativeTaxed) * 0.4 + (cumulativeTaxed + taxableSI - ceilingHRB) * 0.45
    else:
        liableSI = taxableSI * 0.45

print(f"Tax liability on taxable savings income is: £{liableSI}");

cumulativeTaxed = cumulativeTaxed + taxableSI

#Reduce taxable dividend income by NRB
dividendNRB = 2000; #Dividend nil rate band applies to all
if (taxableDI < dividendNRB):
    cumulativeTaxed = cumulativeTaxed + taxableDI
    taxableDI = 0
else:
    taxableDI = taxableDI - dividendNRB
    cumulativeTaxed = cumulativeTaxed + dividendNRB

#Calculate dividend income tax liability;
liableDI = 0

if (taxableDI == 0): #...if taxable savings income is zero
    liableDI = 0
elif (cumulativeTaxed + taxableDI <= ceilingBRB): #...if adding taxable savings income is still within BRB
    liableDI = taxableDI * 0.075
elif (cumulativeTaxed + taxableDI <= ceilingHRB): #...if adding taxable income exceeds BRB but is still within HRB
    if (cumulativeTaxed <= ceilingBRB): #...if cumulativeTaxed is within BRB
        liableDI = (ceilingBRB - cumulativeTaxed) * 0.075 + (cumulativeTaxed + taxableDI - ceilingBRB) * 0.325
    else:
        liableDI = taxableDI * 0.325
elif (cumulativeTaxed + taxableDI > ceilingHRB): #...if adding taxable income exceeds HRB
    if (cumulativeTaxed <= ceilingBRB):
        liableDI = (ceilingBRB - cumulativeTaxed) * 0.075 + (ceilingHRB - ceilingBRB) * 0.325 + (cumulativeTaxed + taxableDI - ceilingHRB) * 0.381
    elif (cumulativeTaxed <= ceilingHRB):
        liableDI = (ceilingHRB - cumulativeTaxed) * 0.325 + (cumulativeTaxed + taxableDI - ceilingHRB) * 0.381
    else:
        liableDI = taxableDI * 0.381

print(f"Tax liability on taxable dividend income is: £{liableDI}")

#Calculate total income tax liability
totalLiable = liableSI + liableNSI + liableDI

if electMCA == True: #Make adjustments for married couples allowance
    if netIncome > ceilingMCA: #When the relevant taxpayers net income exceeds this amount, any excess income
        marriedCouplesAllowance = marriedCouplesAllowance - (netIncome - ceilingMCA)/2
        if marriedCouplesAllowance < 3360:
            marriedCouplesAllowance = 3360 #MCA can't go below this amount
        totalLiable = totalLiable - marriedCouplesAllowance * 0.1

elif electMCA == False and transferMA == True: #Make adjustments for Marriage Allowance
    totalLiable = totalLiable - marriageAllowance * 0.2

print(f"Total income tax liability is: £{totalLiable}")

#Compute tax payable or repayable
taxPayable = totalLiable - taxDeductedAtSource
if taxPayable >= 0:
    print(f"Total income tax payable by the taxpayer is: £{taxPayable}")
else:
    print(f"Total income tax repayable by HMRC is: £{taxPayable*-1}")