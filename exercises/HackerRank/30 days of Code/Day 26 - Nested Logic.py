return_date = input()
expected_date = input()

return_day = int(return_date.split(" ")[0])
return_month = int(return_date.split(" ")[1])
return_year = int(return_date.split(" ")[2])

expected_day = int(expected_date.split(" ")[0])
expected_month = int(expected_date.split(" ")[1])
expected_year = int(expected_date.split(" ")[2])

fine = 0
if (return_year == expected_year):
    if (return_month == expected_month):
        if (return_day > expected_day):
            fine = 15 * (return_day - expected_day)
    elif (return_month > expected_month):
        fine = 500 * (return_month - expected_month)
elif (return_year > expected_year):
    fine = 10000

print(str(fine))