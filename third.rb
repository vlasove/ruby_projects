arr = Array[1,2,3,4, true, "Hi all", 28.3]
puts(arr)


names = Array["Alex","Evgen","Bob"]
names[1] = "Schl"
puts(names[1])

list = Array.new

list[0] = 'Kek'
list[7] = 90
puts(list)
puts(list.length())
puts(list[2].class)
puts(list.reverse())
puts(list.include?(nil))


#Dictionaries

countries = {"Russia"=> "Moscow", "Ukraine" => "Lol", "Num"=>10}
puts(countries["Russia"])

