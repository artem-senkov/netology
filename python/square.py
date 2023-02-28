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
                

sside = input("Введите сторону квадрата в см. = ")
if (check_is_digit(sside)) == 1:
    sside = float(sside)
    print ("Площадь квадрата = " + str(sside ** 2) + " см кв.")

aside = input("Введите длину прямоугольника в см. = ")
if (check_is_digit(aside)) == 1:
    aside = float(aside)
    bside = input("Введите ширину прямоугольника в см. = ")
    if (check_is_digit(bside)) == 1:
        bside = float(bside)
        print ("Периметр прямоугольника = " + str((aside + bside) * 2) + " см.")
        print ("Площадь прямоугольника = " + str(aside * bside) + " см кв.")
