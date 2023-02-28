def check_is_digit(input_str):
    while True:
        try:
            val = int(input_str)
 #           print("Input is an integer number.")
 #           print("Input number is: ", val)
            input_condition = 1
            if val > 0: 
                input_condition = 1
            else:
                input_condition = 0
                print(input_str +" Inputed number less than zero")
            break
        except ValueError:
            try:
                val = float(input_str)
 #               print("Input is an float number.")
 #               print("Input number is: ", val)
                if val > 0: 
                     input_condition = 1
                else:
                     input_condition = 0
                     print(input_str +" Inputed number less than zero")
                break
            except ValueError:
                print(input_str +" This is not a number. Please enter a valid number")
                input_condition = 0
                break
 # this function returns 1 for int and float > 0 and 0 for another input
    return input_condition
                

month_wage = input("Введите зарплату в месяц] = ")
if (check_is_digit(month_wage)) == 1:
    month_wage = float(month_wage)
    percent_ipot = input("Введите процент от ЗП который уходит на ипотеку (1-100) = ")
    if (check_is_digit(percent_ipot)) == 1:
        percent_ipot = float(percent_ipot)
        percent_life = input("Введите процент от ЗП который уходит на питание и жизнь (1-100) = ")
        if (check_is_digit(percent_life)) == 1:
            percent_life = float(percent_life)
            if (percent_life + percent_ipot) <= 100:
                ipot_month = month_wage / 100 * percent_ipot
                life_month = month_wage / 100 * percent_life
                print("Затраты в мес:")
                print("Ипотека в мес " + (str(ipot_month)))
                print("Жиза в мес " + (str(life_month)))
                print("Остаток в мес " + (str(month_wage - ipot_month - life_month)))
                print("Затраты в год:")
                print("Ипотека в год " + (str(ipot_month * 12)))
                print("Жиза в год " + (str(life_month * 12)))
                print("Накопления в год " + (str(month_wage * 12 - ipot_month * 12 - life_month * 12)))
            else: print("Вы тратите больше чем зарабатываете - пройдите курс финансовой грамотности")