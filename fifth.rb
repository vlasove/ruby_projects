x = 8
y = 12

if x < y or x == 9
    puts "Nope, #{x} less than #{y}."

end

puts("Enter your number: ")
num = gets.chomp().to_i

if num < x
    puts("Your num #{num} less than #{x}")
else
    puts("Your num #{num} more than #{x}")
end



def getDateWeek(day)
    nameOfDay = ""
    case day
    when 1
        nameOfDay = "Monday"
    when 2
        nameOfDay = "Tuesday"
    end


    return nameOfDay
    
end

puts(getDateWeek(1))


